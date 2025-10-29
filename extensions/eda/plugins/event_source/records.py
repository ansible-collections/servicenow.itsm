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

# Need to add the project root to the path so that we can import the module_utils.
# The EDA team may come up with a better solution for this in the future.
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import asyncio
import gc
import logging
import re
import resource
from datetime import datetime, timezone, timedelta
from typing import Any, Dict
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from ansible.errors import AnsibleParserError
from plugins.module_utils import client, table
from plugins.module_utils.instance_config import get_combined_instance_config
from plugins.module_utils.query import construct_sysparm_query_from_query


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
        self._cleanup_interval = 300  # 5 minutes cleanup interval (reduced from 1 hour)
        self._poll_count = 0
        self._max_tracking_records = 5000  # Reduced from 10000
        self._max_tracking_age_hours = 24  # Maximum age for tracking records
        self._last_cleanup_time = datetime.now(timezone.utc)
        self._memory_cleanup_count = 0

    def _get_memory_usage(self):
        """Get current memory usage in bytes using resource module"""
        try:
            # Get the current RSS (Resident Set Size) in bytes
            # resource.getrusage() returns memory usage in KB, so multiply by 1024
            memory_info = resource.getrusage(resource.RUSAGE_SELF)
            return memory_info.ru_maxrss * 1024  # Convert KB to bytes
        except Exception:
            # If resource module fails, return 0
            return 0

    def _cleanup_memory(self):
        """Perform memory cleanup operations"""
        self._memory_cleanup_count += 1
        logger.debug("Performing memory cleanup #%d", self._memory_cleanup_count)

        # Force garbage collection
        gc.collect()

        # Clear any cached response data in the client
        if hasattr(self.snow_client, "_client") and self.snow_client._client:
            # Clear any cached data in the underlying HTTP client
            if hasattr(self.snow_client._client, "clear_cache"):
                self.snow_client._client.clear_cache()

            # Clean up unused responses
            if hasattr(self.snow_client._client, "cleanup_unused_responses"):
                self.snow_client._client.cleanup_unused_responses()

        # Clean up table client responses
        if hasattr(self.table_client, "cleanup_responses"):
            self.table_client.cleanup_responses()

        # Refresh connections to prevent connection leaks
        if hasattr(self.snow_client, "_refresh_connection"):
            self.snow_client._refresh_connection()

        # Time-based cleanup: Remove records older than max_tracking_age_hours
        current_time = datetime.now(timezone.utc)
        cutoff_time = current_time - timedelta(hours=self._max_tracking_age_hours)

        # Count records to be removed
        records_to_remove = []
        for sys_id, timestamp_str in self.reported_records_last_poll.items():
            try:
                record_time = get_tz_aware_datetime_from_string(timestamp_str)
                if record_time < cutoff_time:
                    records_to_remove.append(sys_id)
            except Exception:
                # If timestamp parsing fails, remove the record
                records_to_remove.append(sys_id)

        # Remove old records
        for sys_id in records_to_remove:
            del self.reported_records_last_poll[sys_id]

        if records_to_remove:
            logger.debug(
                "Removed %d old tracking records (older than %d hours)",
                len(records_to_remove),
                self._max_tracking_age_hours,
            )

        # Count-based cleanup: If still too many records, keep only the most recent
        if len(self.reported_records_last_poll) > self._max_tracking_records:
            # Sort by timestamp and keep only the most recent records
            sorted_items = sorted(
                self.reported_records_last_poll.items(),
                key=lambda x: x[1],
                reverse=True,
            )
            # Keep 75% instead of 50% to reduce reprocessing
            keep_count = int(self._max_tracking_records * 0.75)
            self.reported_records_last_poll = dict(sorted_items[:keep_count])
            logger.debug(
                "Cleared excess tracking records, kept %d most recent",
                len(self.reported_records_last_poll),
            )

        # Log memory usage
        memory_usage = self._get_memory_usage()
        if memory_usage > 0:
            logger.debug(
                "Memory usage after cleanup: %.2f MB (tracking %d records)",
                memory_usage / 1024 / 1024,
                len(self.reported_records_last_poll),
            )

    def _should_cleanup_memory(self):
        """Check if memory cleanup should be performed"""
        self._poll_count += 1
        current_time = datetime.now(timezone.utc)

        # Time-based cleanup (every 5 minutes)
        time_since_last_cleanup = (
            current_time - self._last_cleanup_time
        ).total_seconds()
        if time_since_last_cleanup >= self._cleanup_interval:
            self._last_cleanup_time = current_time
            return True

        # Poll-based cleanup (every 50 polls instead of 100)
        if self._poll_count % 50 == 0:
            return True

        # Record count cleanup
        if len(self.reported_records_last_poll) > self._max_tracking_records:
            logger.warning(
                "Tracking %d records exceeds limit %d, triggering cleanup",
                len(self.reported_records_last_poll),
                self._max_tracking_records,
            )
            return True

        return False

    def _force_cleanup_all_caches(self):
        """Force cleanup of all cached data to prevent memory leaks"""
        logger.debug("Forcing cleanup of all cached data")

        # Clear tracking records
        self.reported_records_last_poll.clear()

        # Force garbage collection multiple times
        for _unused in range(3):
            gc.collect()

        # Clear client caches
        if hasattr(self.snow_client, "_client") and self.snow_client._client:
            if hasattr(self.snow_client._client, "clear_cache"):
                self.snow_client._client.clear_cache()

            # Clean up unused responses
            if hasattr(self.snow_client._client, "cleanup_unused_responses"):
                self.snow_client._client.cleanup_unused_responses()

        # Clean up table client responses
        if hasattr(self.table_client, "cleanup_responses"):
            self.table_client.cleanup_responses()

        # Refresh connections
        if hasattr(self.snow_client, "_refresh_connection"):
            self.snow_client._refresh_connection()

        logger.debug("All cached data cleared")

    def get_memory_stats(self):
        """Get current memory statistics for monitoring"""
        memory_usage = self._get_memory_usage()
        return {
            "memory_usage_mb": memory_usage / 1024 / 1024 if memory_usage > 0 else 0,
            "tracking_records_count": len(self.reported_records_last_poll),
            "max_tracking_records": self._max_tracking_records,
            "cleanup_count": self._memory_cleanup_count,
            "poll_count": self._poll_count,
        }

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
        logger.info("Poll sleep interval is %s seconds", self.interval)

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

            # Log memory statistics every 100 polls
            if self._poll_count % 100 == 0:
                stats = self.get_memory_stats()
                logger.info(
                    "Memory stats: %.2f MB, tracking %d/%d records, %d cleanups performed",
                    stats["memory_usage_mb"],
                    stats["tracking_records_count"],
                    stats["max_tracking_records"],
                    stats["cleanup_count"],
                )

            logger.debug("Sleeping for %s seconds", self.interval)
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
        logger.debug(
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

            # Periodic memory cleanup during processing (more frequent)
            if record_count % 200 == 0:  # More frequent cleanup
                logger.debug(
                    "Processed %d records, performing memory cleanup", record_count
                )
                self._cleanup_memory()

            # Force garbage collection every 50 records to prevent accumulation
            if record_count % 50 == 0:
                gc.collect()

            # Clean up client responses every 100 records
            if record_count % 100 == 0:
                if hasattr(self.snow_client, "_client") and self.snow_client._client:
                    if hasattr(self.snow_client._client, "cleanup_unused_responses"):
                        self.snow_client._client.cleanup_unused_responses()
                if hasattr(self.table_client, "cleanup_responses"):
                    self.table_client.cleanup_responses()

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
        # Only consider it reported if the timestamp matches (same version)
        if sys_id in reported_records_this_poll:
            if updated_on == reported_records_this_poll[sys_id]:
                logger.debug(
                    "Record %s already processed in current poll cycle", sys_id
                )
                return True
            else:
                logger.debug(
                    "Record %s was processed in current poll but has new timestamp %s (was %s), will process again",
                    sys_id,
                    updated_on,
                    reported_records_this_poll[sys_id],
                )

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
