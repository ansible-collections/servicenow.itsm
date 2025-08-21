# -*- coding: utf-8 -*-
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
module: records
short_description: Event Driven Ansible source for ServiceNow records.
description:
  - Poll the ServiceNow API for any new records in a table, using them as a source for Event Driven Ansible.

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
        instance: https://dev-012345.service-now.com
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


class RecordsSource:
    def __init__(self, queue: asyncio.Queue, args: Dict[str, Any]):
        self.queue = queue
        self.instance_config = get_combined_instance_config(
            config_from_params=args.get("instance")
        )

        self.table_name = args.get("table")
        self.list_query = self.format_list_query(args)
        self.interval = int(args.get("interval", 5))
        self.updated_since = self.parse_string_to_datetime(args.get("updated_since"))

        self.snow_client = client.Client(**self.instance_config)
        self.table_client = table.TableClient(self.snow_client)
        self.previously_reported_records = dict()

    def format_list_query(self, args):
        if args.get("sysparm_query"):
            return {"sysparm_query": args.get("sysparm_query")}

        if not args.get("query"):
            return None

        try:
            return {
                "sysparm_query": construct_sysparm_query_from_query(args.get("query"))
            }
        except ValueError as e:
            raise AnsibleParserError("Unable to parse query: %s" % e)

    async def start_polling(self):
        while True:
            await self._poll_for_records()
            logger.info("Sleeping for %s seconds", self.interval)
            await asyncio.sleep(self.interval)

    async def _poll_for_records(self):
        next_polling_time = datetime.datetime.now() + datetime.timedelta(
            seconds=self.interval
        )
        reported_records = dict()
        logger.info(
            "Polling for new records in %s since %s",
            self.table_name,
            self.updated_since,
        )
        for record in self.table_client.list_records(self.table_name, self.list_query):
            await self.process_record(record, reported_records)

        self.previously_reported_records = reported_records
        self.updated_since = next_polling_time

    async def process_record(self, record, reported_records):
        if self.parse_string_to_datetime(record["sys_updated_on"]) < self.updated_since:
            return

        if self.has_record_been_reported(record):
            # We already reported this record during the last polling interval, so we can skip it.
            return
        else:
            # We havent reported this record yet, so we need to store it in the reported_records dict
            # and send it to the queue.
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
            return datetime.datetime.now()

        try:
            return datetime.datetime.strptime(date_string, format_string)
        except ValueError:
            raise ValueError("Invalid date string: %s" % date_string)


# Entrypoint from ansible-rulebook
async def main(queue: asyncio.Queue, args: Dict[str, Any]):
    records_source = RecordsSource(queue, args)
    await records_source.start_polling()
