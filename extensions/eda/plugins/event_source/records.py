# -*- coding: utf-8 -*-
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
module: records
short_description: Event Driven Ansible source for ServiceNow records.
description:
  - Poll the ServiceNow API for any new records in a table, using them as a source for Event Driven Ansible.
  - This plugin can use the same environment variables as the rest of the ServiceNow collection to
    configure the instance connection.

author:
  - ServiceNow ITSM Collection Contributors (@ansible-collections)

extends_documentation_fragment:
  - servicenow.itsm.query
  - servicenow.itsm.instance

options:
  table:
    description:
      - ServiceNow table to query for new records.
    required: true
  interval:
    description:
      - THe number of seconds to wait before performing another query.
    required: false
    default: 5
  updated_since:
    description:
      - Specify the time that a record must be updated after to be considered new and captured by this plugin.
      - This value should be a date string in the format of "%Y-%m-%d %H:%M:%S".
      - If not specified, the plugin will use the current time as a default. This means any records updated
        after the plugin started will be captured.
    required: false
"""

EXAMPLES = r"""
- name: Watch for new records
  hosts: localhost
  sources:
    - name: Watch for updated change requests
      servicenow.itsm.records:
        instance:
          host: https://dev-012345.service-now.com
          username: ansible
          password: ansible
        table: change_request
        interval: 1
        updated_since: "2025-08-13 12:00:00"

  rules:
    - name: New record created
      condition: event.sys_id is defined
      action:
        debug:
"""

import asyncio
from typing import Any, Dict
import datetime
import logging
import re

# Need to add the project root to the path so that we can import the module_utils.
# The EDA team may come up with a better solution for this in the future.
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from plugins.module_utils.instance_config import get_combined_instance_config
from plugins.module_utils import client, table
from plugins.module_utils.query import construct_sysparm_query_from_query
from ansible.errors import AnsibleParserError


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RecordsSource:
    def __init__(self, queue: asyncio.Queue, args: Dict[str, Any]):
        self.queue = queue
        self.instance_config = get_combined_instance_config(
            config_from_params=args.get("instance")
        )

        self.table_name = args.get("table")
        self.updated_since = self.parse_string_to_datetime(args.get("updated_since"))
        self.interval = int(args.get("interval", 5))
        self._format_list_query(args)

        self.snow_client = client.Client(**self.instance_config)
        self.table_client = table.TableClient(self.snow_client)
        self.previously_reported_records: Dict[str, str] = dict()

    def _format_list_query(self, args):
        self.list_query = {"sysparm_query": args.get("sysparm_query") or ""}

        if args.get("query"):
            try:
                self.list_query["sysparm_query"] = construct_sysparm_query_from_query(args.get("query"))
            except ValueError as e:
                raise AnsibleParserError("Unable to parse query: %s" % e)

        # If the user specified a sys_updated_on filter, we need to remove it from the query so that we can add our own.
        updated_on_search = re.search(r"sys_updated_on.*(\^NQ)|sys_updated_on.*(\^)|sys_updated_on.*$", self.list_query["sysparm_query"])
        if updated_on_search:
            re.sub(r"sys_updated_on.*(\^NQ)|sys_updated_on.*(\^)|sys_updated_on.*$", '', self.list_query["sysparm_query"])

        # If the user defined some query, add an AND operator to the end before adding the timestamp filter
        if len(self.list_query["sysparm_query"]) > 0:
            self.list_query["sysparm_query"] += "^"

        self._add_update_time_to_list_query(self.updated_since)

    def _add_update_time_to_list_query(self, newest_seen):
        newest_seen_date_str = newest_seen.strftime("%Y-%m-%d")
        newest_seen_time_str = newest_seen.strftime("%H:%M:%S")
        query_string = "sys_updated_on>=javascript:gs.dateGenerate('%s', '%s')" % (newest_seen_date_str, newest_seen_time_str)
        if "sys_updated_on>=javascript" in self.list_query["sysparm_query"]:
            self.list_query["sysparm_query"] = re.sub(r"sys_updated_on.*", query_string, self.list_query["sysparm_query"])
        else:
            self.list_query["sysparm_query"] += query_string

    async def start_polling(self):
        while True:
            logger.debug("Staring poll iteration")
            logger.debug(f"{len(self.previously_reported_records)=}")
            try:
                await self._poll_for_records()
            except Exception as e:
                logger.error("Error polling for records: %s", e)
                logger.info("Plugin will keep running")
            logger.info("Sleeping for %s seconds", self.interval)
            await asyncio.sleep(self.interval)
            logger.debug("Ending poll iteration")

    async def _poll_for_records(self):
        # Mark the start of this poll. We'll advance the since timestamp (cursor)
        # at the end to a safe value: max(poll_start_floor, newest_seen_this_poll).
        poll_start = datetime.datetime.now()
        poll_start_floor = poll_start.replace(microsecond=0)

        reported_records: Dict[str, str] = dict()
        newest_seen = self.updated_since  # start from current since timestamp (cursor)
        self._add_update_time_to_list_query(newest_seen)
        logger.info(
            "Polling for new records in %s since %s",
            self.table_name,
            self.updated_since,
        )
        logger.debug(f"{self.list_query=}")

        for record in self.table_client.list_records(self.table_name, self.list_query):
            logger.debug("Processing record: %s", record)
            await self.process_record(record, reported_records)
            # Track the newest timestamp actually observed this cycle
            try:
                ts = self.parse_string_to_datetime(record["sys_updated_on"])
                if ts > newest_seen:
                    newest_seen = ts
            except Exception:
                # If a record has an unexpected timestamp format, ignore it for advancing the since timestamp
                pass
        logger.debug("Ending poll for records")

        self.previously_reported_records = reported_records

        # Compute next 'since' timestamp (lower bound/cursor for next poll):
        # - never in the future
        # - aligned to seconds
        # - monotonically non-decreasing
        next_since = max(newest_seen, poll_start_floor)
        if next_since > self.updated_since:
            logger.debug(
                "Advancing most recent timestamp observed: %s -> %s", self.updated_since, next_since
            )
            self.updated_since = next_since
        else:
            logger.debug(
                "Most recent timestamp observed is unchanged (next_since=%s <= updated_since=%s)",
                next_since,
                self.updated_since,
            )

    async def process_record(self, record, reported_records):
        # Ignore anything strictly older than our since timestamp.
        if self.parse_string_to_datetime(record["sys_updated_on"]) < self.updated_since:
            return

        if self.has_record_been_reported(record):
            # Already reported in the immediately previous cycle.
            return
        else:
            # Not reported yet: remember it for this cycle and emit.
            reported_records[record["sys_id"]] = record["sys_updated_on"]
            await self.queue.put(record)

    def has_record_been_reported(self, record):
        if record["sys_id"] in self.previously_reported_records:
            if (
                record["sys_updated_on"]
                == self.previously_reported_records[record["sys_id"]]
            ):
                return True
        return False

    def parse_string_to_datetime(self, date_string: str = None):
        format_string = "%Y-%m-%d %H:%M:%S"
        if date_string is None:
            # Truncate to whole seconds to match ServiceNow precision
            return datetime.datetime.now().replace(microsecond=0)

        try:
            # ServiceNow returns second-precision strings (no microseconds)
            return datetime.datetime.strptime(date_string, format_string)
        except ValueError:
            raise ValueError("Invalid date string: %s" % date_string)


# Entrypoint from ansible-rulebook
async def main(queue: asyncio.Queue, args: Dict[str, Any]):
    records_source = RecordsSource(queue, args)
    await records_source.start_polling()
