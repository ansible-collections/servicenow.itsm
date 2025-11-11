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
  - If O(remote_servicenow_timezone) is not set the plugin will query for a user-specific timezone then
    an explicit system-wide timezone in ServiceNow. If none of these three are set, the plugin will error out.
  - B(NOTE:) This approach is useful for small-scale event handling, but for large-scale event processing we
    recommend using a ServiceNow-side mechanism (such as, but not necssarily limtied to, a Spoke app or business
    rules). The only contetxt this plugin has are the record contents and (possibly) a timestamp. For large and
    busy environments, this places a significant burden on the action to ensure that data to be double-processed,
    and in addition it is difficult with this scheme to determine if events have been missed. Architecturally, these
    problems are easier to solve with the additional data available at the source.

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
    default: 60
  updated_since:
    description:
      - Specify the time that a record must be updated after to be considered new and captured by this plugin.
      - This value should be a date string in the format of "%Y-%m-%d %H:%M:%S".
      - If not specified, the plugin will use the current time as a default. This means any records updated
        after the plugin started will be captured.
    required: false
  remote_servicenow_timezone:
    description:
      - The timezone to use for ServiceNow timestamps.
      - If not set, the ServiceNow user record will be queried for an explicit timezone, which will then be used.
      - If neither this parameter nor an explicit user timezone are set in ServiceNow, the plugin will error out.
      - All timestamps will be converted to UTC during processing for time comparisons.
    required: false
  timezone:
    description:
      - The timezone that the O(updated_since) parameter is in, for local processing in EDA.
      - All timestamps will be converted to UTC during processing for time comparisons.
    required: false
    default: UTC
  timestamp_field:
    description:
      - The field name to use for timestamp-based filtering and deduplication.
      - Defaults to 'sys_updated_on' for standard ServiceNow tables.
      - For custom tables or tables without sys_updated_on, specify the appropriate timestamp field.
      - Common alternatives include 'sys_created_on', 'last_modified', or custom timestamp fields.
    required: false
    default: 'sys_updated_on'
  order_by_field:
    description:
      - The field name to use for ordering records.
      - Defaults to the same value as timestamp_field.
      - Should be a field that can be used for consistent ordering of records.
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
        timezone: America/New_York

    - name: Watch for custom table records
      servicenow.itsm.records:
        instance:
          host: https://dev-012345.service-now.com
          username: ansible
          password: ansible
        table: u_custom_table
        timestamp_field: u_last_modified
        order_by_field: u_last_modified
        interval: 5

    - name: Watch for records using sys_created_on
      servicenow.itsm.records:
        instance:
          host: https://dev-012345.service-now.com
          username: ansible
          password: ansible
        table: some_table_without_updated_on
        timestamp_field: sys_created_on
        interval: 10

  rules:
    - name: New record created
      condition: event.sys_id is defined
      action:
        debug:
"""

# Need to add the project root to the path so that we can import the module_utils.
# The EDA team may come up with a better solution for this in the future.
import os  # noqa: E402
import sys  # noqa: E402

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import asyncio  # noqa: E402
import gc  # noqa: E402
import logging  # noqa: E402
import re  # noqa: E402
import resource  # noqa: E402
from datetime import datetime, timezone, timedelta  # noqa: E402
from typing import Any, Dict  # noqa: E402
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError  # noqa: E402

from ansible.errors import AnsibleParserError, AnsibleError  # noqa: E402
from plugins.module_utils import client, table  # noqa: E402
from plugins.module_utils.instance_config import get_combined_instance_config  # noqa: E402
from plugins.module_utils.query import construct_sysparm_query_from_query  # noqa: E402


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

    def format_and_clean_query_parameters(
        self,
        query=None,
        sysparm_query=None,
        timestamp_field="sys_updated_on",
        order_by_field=None,
    ):
        """
        Take the query or sysparm_query parameter from the user and format it into a list query
        that can be used to query the table.
        We will remove any pre-existing timestamp field filter so that we can add our own, since that
        parameter will change as the plugin continues to run.
        """
        if order_by_field is None:
            order_by_field = timestamp_field

        if sysparm_query is None:
            sysparm_query = ""

        if query is not None:
            try:
                sysparm_query = construct_sysparm_query_from_query(query)
            except ValueError as e:
                raise AnsibleParserError("Unable to parse query: %s" % e)

        # If the user specified a timestamp field or ORDERBY filter, we need to remove it from the query so that we can add our own.
        # Escape special regex characters in the field name
        escaped_timestamp_field = re.escape(timestamp_field)
        escaped_order_by_field = re.escape(order_by_field)

        sysparm_query = re.sub(
            rf"\^?N?Q?{escaped_timestamp_field}[^\^]*(\^?)", r"\1", sysparm_query
        )
        sysparm_query = re.sub(r"\^?N?Q?ORDERBY[^\^]*(\^?)", r"\1", sysparm_query)

        if len(sysparm_query) > 0:
            sysparm_query += "^"
        sysparm_query += f"ORDERBY{order_by_field}"

        return {
            "sysparm_query": sysparm_query,
            "sysparm_display_value": "false",  # Only return "raw", or UTC values. Display values are in the user's timezone, which varies.
        }

    def inject_timestamp_filter(
        self,
        sysparm_query: str,
        timestamp_datetime: datetime,
        snow_timezone: ZoneInfo,
        timestamp_field: str,
    ):
        """
        Add the newest_seen timestamp onto our list query. This ensures that we are always polling for new and unseen records.
        We advance the timestamp by 1 second to avoid processing the same records multiple times.
        """
        # Convert the latest polling start time to the user's timezone so we can use it in the query.
        timestamp_datetime_in_snow_tz = timestamp_datetime.astimezone(snow_timezone)

        # Advance the timestamp by 1 second to avoid processing the same records
        advanced_datetime = timestamp_datetime_in_snow_tz + timedelta(seconds=1)

        timestamp_date_str = advanced_datetime.strftime("%Y-%m-%d")
        timestamp_time_str = advanced_datetime.strftime("%H:%M:%S")

        # Inject the timestamp filter into the query, with advanced timestamp
        # Using >= ensures we capture records with the advanced timestamp or newer
        query_string = f"{timestamp_field}>=javascript:gs.dateGenerate('{timestamp_date_str}', '{timestamp_time_str}')"

        # Escape special regex characters in the field name
        escaped_timestamp_field = re.escape(timestamp_field)
        if f"{timestamp_field}>" in sysparm_query:
            sysparm_query = re.sub(
                rf"{escaped_timestamp_field}>=?.*", query_string, sysparm_query
            )
        else:
            sysparm_query += f"^{query_string}"

        return sysparm_query


class RecordsSource:
    def __init__(self, queue: asyncio.Queue, args: Dict[str, Any]):
        self.queue = queue
        self.instance_config = get_combined_instance_config(
            config_from_params=args.get("instance")
        )
        self.table_name = args.get("table")
        self.timestamp_field = args.get("timestamp_field", "sys_updated_on")
        self.order_by_field = args.get("order_by_field", self.timestamp_field)
        self.snow_client = client.Client(**self.instance_config)
        self.table_client = table.TableClient(self.snow_client, memory_efficient=True)
        self.query_formatter = QueryFormatter()
        self.list_query = self.query_formatter.format_and_clean_query_parameters(
            query=args.get("query"),
            sysparm_query=args.get("sysparm_query"),
            timestamp_field=self.timestamp_field,
            order_by_field=self.order_by_field,
        )

        self.initial_polling_start_time = get_tz_aware_datetime_from_string(
            date_string=args.get("updated_since"),
            date_string_timezone=args.get("timezone"),
        )

        if args.get("remote_servicenow_timezone"):
            self.remote_snow_timezone = ZoneInfo(args.get("remote_servicenow_timezone"))
            logger.info(
                "remote_servicenow_timezone set by parameter to %s",
                args.get("remote_servicenow_timezone"),
            )
        else:
            self.remote_snow_timezone = None

        self.interval = int(args.get("interval", 60))
        self.timestamp_field = args.get("timestamp_field", "sys_updated_on")
        self.order_by_field = args.get("order_by_field", self.timestamp_field)
        self._latest_timestamp_floor = None
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
        if self.remote_snow_timezone is None:
            self.remote_snow_timezone = self.lookup_snow_user_timezone()
            logger.info(
                "Remote ServiceNow user's timezone set by ServiceNow lookup to '%s'",
                self.remote_snow_timezone,
            )

        logger.info("Poll sleep interval is %s seconds", self.interval)

        while True:
            logger.debug(
                "Starting poll iteration. The last time there was an update, there were %s records that were reported",
                len(self.reported_records_last_poll),
            )
            try:
                await self._poll_for_records()
            except Exception as e:
                logger.error("Error polling for records: %s", e)
                logger.info("Plugin will keep running")

            # Perform memory cleanup if needed
            if self._should_cleanup_memory():
                self._cleanup_memory()

            # Log memory statistics every 100 polls
            if self._poll_count % 100 == 0:
                stats = self.get_memory_stats()
                logger.debug(
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
    def latest_timestamp_floor(self):
        """
        Return either the initial polling start time provided by the user, or the
        latest timestamp of the last record processed.
        """
        return self._latest_timestamp_floor or self.initial_polling_start_time

    async def _poll_for_records(self):
        """
        Poll for new records in the table since the polling_start_time. We update the list query
        with the latest timestamp seen, and then process any new records that are found.

        If we find any records, we update the latest_sys_updated_on_floor to the latest timestamp seen.
        """
        reported_records_this_poll: Dict[str, str] = dict()
        self.list_query["sysparm_query"] = self.query_formatter.inject_timestamp_filter(
            sysparm_query=self.list_query["sysparm_query"],
            timestamp_datetime=self.latest_timestamp_floor,
            snow_timezone=self.remote_snow_timezone,
            timestamp_field=self.timestamp_field,
        )
        logger.debug(
            "Polling for records with %s on or after %s (UTC)",
            self.timestamp_field,
            self.latest_timestamp_floor,
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
                "Processing record with sys_id %s and %s %s",
                record["sys_id"],
                self.timestamp_field,
                record.get(self.timestamp_field, "N/A"),
            )
            if self.should_record_be_sent_to_queue(record, reported_records_this_poll):
                await self.queue.put(record)
                _last_record_processed = record

                # Track the latest timestamp seen (not just the last processed record)
                if self.timestamp_field in record:
                    record_timestamp = get_tz_aware_datetime_from_string(
                        record[self.timestamp_field]
                    )
                    if (
                        _latest_timestamp is None
                        or record_timestamp > _latest_timestamp
                    ):
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
                self._latest_timestamp_floor = _latest_timestamp
            elif self.timestamp_field in _last_record_processed:
                # Fallback to last processed record if no timestamp was tracked
                self._latest_timestamp_floor = get_tz_aware_datetime_from_string(
                    _last_record_processed[self.timestamp_field]
                )
            logger.debug(
                "Increasing the next query %s timestamp to %s",
                self.timestamp_field,
                self._latest_timestamp_floor,
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
        First checks for an explicit user timezone, then falls back to system default timezone.
        Raises AnsibleError if neither is set.
        """
        # Use a temporary non-memory-efficient client for this lookup since we need a list result
        temp_client = table.TableClient(self.snow_client, memory_efficient=False)

        # First, try to get the user's explicit timezone
        user_timezone_records = temp_client.list_records(
            table="sys_user",
            query={
                "sysparm_query": "user_name=javascript:gs.getUserName()",
                "sysparm_exclude_reference_link": "true",
            },
        )
        try:
            if not user_timezone_records:
                raise IndexError("No user record found")
            user_timezone_str = user_timezone_records[0].get("time_zone", "")
            servicenow_user_name = user_timezone_records[0].get("user_name", "unknown")

            # If user has explicit timezone set, use it
            if user_timezone_str and user_timezone_str != "":
                logger.info("ServiceNow user timezone is %s", user_timezone_str)
                try:
                    return ZoneInfo(user_timezone_str)
                except ZoneInfoNotFoundError as e:
                    raise AnsibleError(
                        "Invalid timezone '%s' set for user %s: %s"
                        % (user_timezone_str, servicenow_user_name, e)
                    ) from e
        except (KeyError, IndexError) as e:
            raise AnsibleParserError(
                "Unable to lookup user record in ServiceNow: %s" % e
            ) from e

        # User timezone is not set, try system default timezone
        logger.info(
            "User %s does not have explicit timezone set, checking system default",
            servicenow_user_name,
        )
        system_timezone_records = temp_client.list_records(
            table="sys_properties",
            query={
                "sysparm_query": "name=glide.sys.default.tz",
                "sysparm_exclude_reference_link": "true",
            },
        )
        try:
            if not system_timezone_records:
                # System property not found, fall through to final error
                pass
            else:
                system_timezone_str = system_timezone_records[0].get("value", "")

                if system_timezone_str and system_timezone_str != "":
                    logger.info(
                        "ServiceNow system default timezone is %s", system_timezone_str
                    )
                    try:
                        return ZoneInfo(system_timezone_str)
                    except ZoneInfoNotFoundError as e:
                        raise AnsibleError(
                            "Invalid system default timezone '%s': %s"
                            % (system_timezone_str, e)
                        ) from e
        except KeyError as e:
            raise AnsibleParserError(
                "Unable to lookup system timezone property in ServiceNow: %s" % e
            ) from e

        # Neither user nor system timezone is set
        raise AnsibleError(
            "ServiceNow timezone not set. Either set remote_servicenow_timezone parameter, "
            "set time_zone in user table for user %s, or set glide.sys.default.tz system property."
            % servicenow_user_name
        )

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
        # Check if the record has the required timestamp field
        if self.timestamp_field not in record:
            logger.warning(
                "Record %s does not have timestamp field %s, skipping",
                record["sys_id"],
                self.timestamp_field,
            )
            return False

        # Ignore anything strictly older than our since timestamp.
        record_update_timestamp = record[self.timestamp_field]
        if (
            get_tz_aware_datetime_from_string(record_update_timestamp)
            < self.latest_timestamp_floor
        ):
            logger.warning(
                "Record update timestamp %s is somehow older than the latest %s floor %s",
                record_update_timestamp,
                self.timestamp_field,
                self.latest_timestamp_floor,
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
        reported_records_this_poll[record["sys_id"]] = record[self.timestamp_field]
        return True

    def has_record_been_reported(self, record, reported_records_this_poll):
        """
        Check if a record has already been reported in the current or previous poll cycle.
        Returns True if the record has been reported, False otherwise.
        """
        sys_id = record["sys_id"]

        # Check if the record has the required timestamp field
        if self.timestamp_field not in record:
            return False

        updated_on = record[self.timestamp_field]

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
