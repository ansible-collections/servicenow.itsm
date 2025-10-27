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
  - If you supply O(query) or O(sysparm_query), the plugin will remove any reference to ORDEREDBY and sys_updated_on
    in the query so that it can add its own.

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
  timezone:
    description:
      - The timezone that the O(updated_since) parameter is in.
      - All timestamps will be converted to UTC during processing, since that is the timezone that ServiceNow uses.
    required: false
    default: UTC
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
        timezone: America/New_York

  rules:
    - name: New record created
      condition: event.sys_id is defined
      action:
        debug:
"""

import asyncio
from typing import Any, Dict
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import logging
import re
import gc
import os

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


DATE_FORMAT_STRING = "%Y-%m-%d %H:%M:%S"


def get_tz_aware_datetime_from_string(
    date_string: str = None, date_string_timezone: str = "UTC"
):
    if date_string is None:
        # Truncate to whole seconds to match ServiceNow precision
        return datetime.now(timezone.utc).replace(microsecond=0)

    try:
        # ServiceNow returns second-precision strings (no microseconds)
        tz_naive_datetime = datetime.strptime(date_string, DATE_FORMAT_STRING)
    except ValueError:
        raise AnsibleParserError("Invalid date string: %s" % date_string)

    try:
        return tz_naive_datetime.replace(tzinfo=ZoneInfo(date_string_timezone))
    except ZoneInfoNotFoundError:
        raise AnsibleParserError("Invalid timezone string: %s" % date_string_timezone)


class QueryFormatter:
    def __init__(self):
        pass

    def format_and_clean_query_parameters(self, query=None, sysparm_query=None):
        """
        Take the query or sysparm_query parameter from the user and format it into a list query
        that can be used to query the table.
        We will remove any pre-existing sys_updated_on filter so that we can add our own, since that
        parameter will change as the plugin continues to run.
        """
        if sysparm_query is None:
            sysparm_query = ""

        if query is not None:
            try:
                sysparm_query = construct_sysparm_query_from_query(query)
            except ValueError as e:
                raise AnsibleParserError("Unable to parse query: %s" % e)

        # If the user specified a sys_updated_on or ORDERBY filter, we need to remove it from the query so that we can add our own.
        sysparm_query = re.sub(
            r"\^?N?Q?sys_updated_on[^\^]*(\^?)", r"\1", sysparm_query
        )
        sysparm_query = re.sub(r"\^?N?Q?ORDERBY[^\^]*(\^?)", r"\1", sysparm_query)

        if len(sysparm_query) > 0:
            sysparm_query += "^"
        sysparm_query += "ORDERBYsys_updated_on"

        return {
            "sysparm_query": sysparm_query,
            "sysparm_display_value": "false",  # Only return "raw", or UTC values. Display values are in the user's timezone, which varies.
        }

    def inject_sys_updated_on_filter(
        self,
        sysparm_query: str,
        sys_update_on_datetime: datetime,
        snow_timezone: ZoneInfo,
    ):
        """
        Add the newest_seen timestamp onto our list query. This ensures that we are always polling for new and unseen records.
        We use >= to include records with the same timestamp, which is important for handling multiple records updated simultaneously.
        """
        # Convert the latest polling start time to the user's timezone so we can use it in the query.
        sys_update_on_datetime_in_snow_tz = sys_update_on_datetime.astimezone(
            snow_timezone
        )
        sys_updated_on_date_str = sys_update_on_datetime_in_snow_tz.strftime("%Y-%m-%d")
        sys_updated_on_time_str = sys_update_on_datetime_in_snow_tz.strftime("%H:%M:%S")

        # Inject the sys_updated_on filter into the query, with new timestamp
        # Using >= ensures we capture records with the same timestamp
        query_string = "sys_updated_on>=javascript:gs.dateGenerate('%s', '%s')" % (
            sys_updated_on_date_str,
            sys_updated_on_time_str,
        )
        if "sys_updated_on>" in sysparm_query:
            sysparm_query = re.sub(r"sys_updated_on>=?.*", query_string, sysparm_query)
        else:
            sysparm_query += "^%s" % query_string

        return sysparm_query


class RecordsSource:
    def __init__(self, queue: asyncio.Queue, args: Dict[str, Any]):
        self.queue = queue
        self.instance_config = get_combined_instance_config(
            config_from_params=args.get("instance")
        )
        self.table_name = args.get("table")
        self.snow_client = client.Client(**self.instance_config)
        self.table_client = table.TableClient(self.snow_client, memory_efficient=True)
        self.query_formatter = QueryFormatter()
        self.list_query = self.query_formatter.format_and_clean_query_parameters(
            query=args.get("query"), sysparm_query=args.get("sysparm_query")
        )

        self.initial_polling_start_time = get_tz_aware_datetime_from_string(
            date_string=args.get("updated_since"),
            date_string_timezone=args.get("timezone"),
        )
        self.interval = int(args.get("interval", 5))
        self._latest_sys_updated_on_floor = None
        self.reported_records_last_poll: Dict[str, str] = dict()

        # Memory management attributes
        self._memory_threshold = 100 * 1024 * 1024  # 100MB threshold
        self._cleanup_interval = 3600  # 1 hour cleanup interval
        self._poll_count = 0
        self._max_tracking_records = (
            10000  # Limit tracking records to prevent memory bloat
        )

    def _get_memory_usage(self):
        """Get current memory usage in bytes"""
        try:
            import psutil

            process = psutil.Process(os.getpid())
            return process.memory_info().rss
        except ImportError:
            # psutil not available, return 0
            return 0

    def _cleanup_memory(self):
        """Perform memory cleanup operations"""
        logger.debug("Performing memory cleanup")

        # Force garbage collection
        gc.collect()

        # Clear old tracking records if we have too many
        if len(self.reported_records_last_poll) > self._max_tracking_records:
            # Keep only the most recent 50% of records
            sorted_items = sorted(
                self.reported_records_last_poll.items(),
                key=lambda x: x[1],
                reverse=True,
            )
            self.reported_records_last_poll = dict(
                sorted_items[: self._max_tracking_records // 2]
            )
            logger.debug(
                "Cleared old tracking records, kept %d most recent",
                len(self.reported_records_last_poll),
            )

        # Log memory usage
        memory_usage = self._get_memory_usage()
        if memory_usage > 0:
            logger.debug(
                "Memory usage after cleanup: %.2f MB", memory_usage / 1024 / 1024
            )

    def _should_cleanup_memory(self):
        """Check if memory cleanup should be performed"""
        self._poll_count += 1
        return (
            self._poll_count % 100 == 0  # Every 100 polls
            or self._get_memory_usage() > self._memory_threshold
        )

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - cleanup resources"""
        await self.close()

    async def close(self):
        """Cleanup resources"""
        try:
            if hasattr(self.snow_client, "close"):
                self.snow_client.close()
            logger.debug("EDA plugin resources cleaned up")
        except Exception as e:
            logger.warning("Error during EDA plugin cleanup: %s", e)

    # entrypoint for main logic
    async def start_polling(self):
        """
        Main entrypoint for the plugin. Start the polling loop and keep running until the plugin is stopped.
        """
        remote_snow_timezone = self.lookup_snow_user_timezone()
        logger.info("Remote ServiceNow user's timezone is '%s'", remote_snow_timezone)

        while True:
            logger.debug(
                "Starting poll iteration. The last time there was an update, there were %s records that were reported",
                len(self.reported_records_last_poll),
            )
            try:
                await self._poll_for_records(remote_snow_timezone)
            except Exception as e:
                logger.error("Error polling for records: %s", e)
                logger.info("Plugin will keep running")

            # Perform memory cleanup if needed
            if self._should_cleanup_memory():
                self._cleanup_memory()

            logger.info("Sleeping for %s seconds", self.interval)
            await asyncio.sleep(self.interval)
            logger.debug("Ending poll iteration")

    @property
    def latest_sys_updated_on_floor(self):
        """
        Return either the initial polling start time provided by the user, or the
        latest sys_updated_on timestamp of the last record processed.
        """
        return self._latest_sys_updated_on_floor or self.initial_polling_start_time

    async def _poll_for_records(self, remote_snow_timezone: ZoneInfo):
        """
        Poll for new records in the table since the polling_start_time. We update the list query
        with the latest timestamp seen, and then process any new records that are found.

        If we find any records, we update the latest_sys_updated_on_floor to the latest timestamp seen.
        """
        reported_records_this_poll: Dict[str, str] = dict()
        self.list_query["sysparm_query"] = (
            self.query_formatter.inject_sys_updated_on_filter(
                sysparm_query=self.list_query["sysparm_query"],
                sys_update_on_datetime=self.latest_sys_updated_on_floor,
                snow_timezone=remote_snow_timezone,
            )
        )
        logger.info(
            "Polling for records updated on or after %s (UTC)",
            self.latest_sys_updated_on_floor,
        )
        logger.debug("List query: %s", self.list_query)

        _last_record_processed = None
        _latest_timestamp = None
        record_count = 0

        # Use the regular method for now to maintain compatibility with tests
        # The memory management features are still active through the memory_efficient flag
        records_iter = self.table_client.list_records(self.table_name, self.list_query)

        for record in records_iter:
            logger.debug(
                "Processing record with sys_id %s and sys_updated_on %s",
                record["sys_id"],
                record["sys_updated_on"],
            )
            if self.should_record_be_sent_to_queue(record, reported_records_this_poll):
                await self.queue.put(record)
                _last_record_processed = record

                # Track the latest timestamp seen (not just the last processed record)
                record_timestamp = get_tz_aware_datetime_from_string(
                    record["sys_updated_on"]
                )
                if _latest_timestamp is None or record_timestamp > _latest_timestamp:
                    _latest_timestamp = record_timestamp

            record_count += 1

            # Periodic memory cleanup during processing
            if record_count % 1000 == 0:
                logger.debug(
                    "Processed %d records, performing memory cleanup", record_count
                )
                self._cleanup_memory()

        logger.debug("Ending poll for records")
        if _last_record_processed:
            # Update the timestamp to the latest timestamp seen (not just the last processed record)
            # This ensures we don't miss records with the same timestamp
            if _latest_timestamp:
                self._latest_sys_updated_on_floor = _latest_timestamp
            else:
                # Fallback to last processed record if no timestamp was tracked
                self._latest_sys_updated_on_floor = get_tz_aware_datetime_from_string(
                    _last_record_processed["sys_updated_on"]
                )
            logger.debug(
                "Increasing the next query sys_updated_on timestamp to %s",
                self._latest_sys_updated_on_floor,
            )

            # If we find any new records, we will be increasing the next query sys_updated_on timestamp and
            # need to remember which records we have seen so that we don't report them again.
            self.reported_records_last_poll = reported_records_this_poll
        else:
            # No records were processed, but we should still update the tracking
            # to prevent processing the same records again
            self.reported_records_last_poll = reported_records_this_poll

    def lookup_snow_user_timezone(self):
        """
        The SNOW user's timezone may be different from the local timezone of the machine running the plugin.
        We need to lookup this timezone so we can convert our UTC timestamp into this timezone for the
        table query.
        """
        # Use a temporary non-memory-efficient client for this lookup since we need a list result
        temp_client = table.TableClient(self.snow_client, memory_efficient=False)
        user_timezone_records = temp_client.list_records(
            table="sys_user",
            query={
                "sysparm_query": "user_name=javascript:gs.getUserName()",
                "sysparm_exclude_reference_link": "true",
            },
        )
        try:
            user_timezone_str = user_timezone_records[0]["time_zone"]
        except (KeyError, IndexError) as e:
            raise AnsibleParserError(
                "Unable to lookup user timezone in ServiceNow: %s" % e
            ) from e

        return ZoneInfo(user_timezone_str)

    def should_record_be_sent_to_queue(self, record, reported_records_this_poll):
        """
        Determine if a record should be sent to the queue.
        We ignore anything strictly older than our since timestamp, and we
        ignore anything that has already been reported in the immediately previous cycle.

        If it is a new record, we need to remember it for the next cycle (so that we don't report it again),
        and add it to the queue for EDA.

        Note: If a record is updated (new timestamp), it will be processed again, which is the
        desired behavior for Event Driven Ansible - we want to react to record changes.
        """
        # Ignore anything strictly older than our since timestamp.
        record_update_timestamp = record["sys_updated_on"]
        if (
            get_tz_aware_datetime_from_string(record_update_timestamp)
            < self.latest_sys_updated_on_floor
        ):
            logger.warning(
                "Record update timestamp %s is somehow older than the latest sys_updated_on floor %s",
                record_update_timestamp,
                self.latest_sys_updated_on_floor,
            )
            return False

        if self.has_record_been_reported(record, reported_records_this_poll):
            logger.debug(
                "Record %s has already been reported in the this cycle or the last cycle.",
                record["sys_id"],
            )
            return False

        # Not reported yet: remember it for this cycle and emit.
        logger.debug("Record %s is new and will be reported", record["sys_id"])
        reported_records_this_poll[record["sys_id"]] = record["sys_updated_on"]
        return True

    def has_record_been_reported(self, record, reported_records_this_poll):
        """
        Check if a record has already been reported in the current or previous poll cycle.
        Returns True if the record has been reported, False otherwise.
        """
        sys_id = record["sys_id"]
        updated_on = record["sys_updated_on"]

        # Check if we've already processed this record in the current poll
        if sys_id in reported_records_this_poll:
            logger.debug("Record %s already processed in current poll cycle", sys_id)
            return True

        # Check if we've processed this record in the previous poll
        # If the timestamp matches, it's the same version of the record
        if sys_id in self.reported_records_last_poll:
            last_reported_timestamp = self.reported_records_last_poll[sys_id]
            if updated_on == last_reported_timestamp:
                logger.debug(
                    "Record %s already processed in previous poll cycle with same timestamp %s",
                    sys_id,
                    updated_on,
                )
                return True
            else:
                logger.debug(
                    "Record %s was processed before but has new timestamp %s (was %s), will process again",
                    sys_id,
                    updated_on,
                    last_reported_timestamp,
                )

        # Record has not been reported yet
        logger.debug("Record %s is new and will be processed", sys_id)
        return False


# Entrypoint from ansible-rulebook
async def main(queue: asyncio.Queue, args: Dict[str, Any]):
    async with RecordsSource(queue, args) as records_source:
        try:
            await records_source.start_polling()
        except Exception as e:
            logger.error("Error occurred during polling: %s", e)
            raise e
