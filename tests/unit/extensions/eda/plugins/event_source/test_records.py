from __future__ import absolute_import, division, print_function

__metaclass__ = type

from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import pytest
from unittest.mock import patch, AsyncMock, Mock
from ansible.errors import AnsibleParserError
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../.."))

from extensions.eda.plugins.event_source.records import (
    RecordsSource,
    get_tz_aware_datetime_from_string,
    QueryFormatter,
)


def test_get_tz_aware_datetime_from_string():
    assert get_tz_aware_datetime_from_string("2025-08-13 12:00:00") == datetime(
        2025, 8, 13, 12, 0, 0, tzinfo=timezone.utc
    )
    assert isinstance(get_tz_aware_datetime_from_string(), datetime)

    assert get_tz_aware_datetime_from_string(
        "2025-08-13 12:00:00", "America/New_York"
    ) == datetime(2025, 8, 13, 12, 0, 0, tzinfo=ZoneInfo("America/New_York"))


def test_get_tz_aware_datetime_from_string_errors():
    with pytest.raises(AnsibleParserError, match="Invalid date string: 2025-08-13"):
        get_tz_aware_datetime_from_string("2025-08-13")

    with pytest.raises(
        AnsibleParserError, match="Invalid timezone string: Invalid/Timezone"
    ):
        get_tz_aware_datetime_from_string("2025-08-13 12:00:00", "Invalid/Timezone")


class TestQueryFormatter:
    @patch(
        "extensions.eda.plugins.event_source.records.construct_sysparm_query_from_query"
    )
    def test_format_and_clean_query_parameters_query(
        self, construct_sysparm_query_from_query
    ):
        construct_sysparm_query_from_query.return_value = "foo"
        query_formatter = QueryFormatter()
        assert query_formatter.format_and_clean_query_parameters(query="foo") == {
            "sysparm_query": "foo^ORDERBYsys_updated_on",
            "sysparm_display_value": "false",
        }

    @pytest.mark.parametrize(
        "sysparm_query, expected",
        [
            ("foo", "foo^ORDERBYsys_updated_on"),
            (None, "ORDERBYsys_updated_on"),
            ("sys_updated_on>2025-01-01 12:00:00", "ORDERBYsys_updated_on"),
            (
                "foo^sys_updated_on>2025-01-01 12:00:00^bar",
                "foo^bar^ORDERBYsys_updated_on",
            ),
            ("foo^ORDERBYbizz^bar", "foo^bar^ORDERBYsys_updated_on"),
        ],
    )
    def test_format_and_clean_query_parameters_sysparm(self, sysparm_query, expected):
        query_formatter = QueryFormatter()
        assert query_formatter.format_and_clean_query_parameters(
            sysparm_query=sysparm_query
        ) == {
            "sysparm_query": expected,
            "sysparm_display_value": "false",
        }

    @pytest.mark.parametrize(
        "sysparm_query, timestamp_field, order_by_field, expected",
        [
            ("foo", "sys_created_on", None, "foo^ORDERBYsys_created_on"),
            ("foo", "u_last_modified", "u_last_modified", "foo^ORDERBYu_last_modified"),
            ("foo", "custom_field", "other_field", "foo^ORDERBYother_field"),
            (None, "sys_created_on", None, "ORDERBYsys_created_on"),
        ],
    )
    def test_format_and_clean_query_parameters_custom_fields(
        self, sysparm_query, timestamp_field, order_by_field, expected
    ):
        query_formatter = QueryFormatter()
        assert query_formatter.format_and_clean_query_parameters(
            sysparm_query=sysparm_query,
            timestamp_field=timestamp_field,
            order_by_field=order_by_field,
        ) == {
            "sysparm_query": expected,
            "sysparm_display_value": "false",
        }

    @pytest.mark.parametrize(
        "sysparm_query, expected",
        [
            (
                "foo",
                "foo^sys_updated_on>=javascript:gs.dateGenerate('2025-01-01', '12:00:01')",
            ),
            (
                "foo^sys_updated_on>2026-01-01 12:00:00",
                "foo^sys_updated_on>=javascript:gs.dateGenerate('2025-01-01', '12:00:01')",
            ),
        ],
    )
    def test_inject_timestamp_filter_default(self, sysparm_query, expected):
        query_formatter = QueryFormatter()
        test_datetime = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        tz = timezone.utc
        assert (
            query_formatter.inject_timestamp_filter(
                sysparm_query=sysparm_query,
                timestamp_datetime=test_datetime,
                snow_timezone=tz,
                timestamp_field="sys_updated_on",
            )
            == expected
        )

    @pytest.mark.parametrize(
        "sysparm_query, timestamp_field, expected",
        [
            (
                "foo",
                "sys_created_on",
                "foo^sys_created_on>=javascript:gs.dateGenerate('2025-01-01', '12:00:01')",
            ),
            (
                "foo",
                "u_last_modified",
                "foo^u_last_modified>=javascript:gs.dateGenerate('2025-01-01', '12:00:01')",
            ),
            (
                "foo^u_last_modified>2026-01-01 12:00:00",
                "u_last_modified",
                "foo^u_last_modified>=javascript:gs.dateGenerate('2025-01-01', '12:00:01')",
            ),
        ],
    )
    def test_inject_timestamp_filter_custom_field(
        self, sysparm_query, timestamp_field, expected
    ):
        query_formatter = QueryFormatter()
        test_datetime = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        tz = timezone.utc
        assert (
            query_formatter.inject_timestamp_filter(
                sysparm_query=sysparm_query,
                timestamp_datetime=test_datetime,
                snow_timezone=tz,
                timestamp_field=timestamp_field,
            )
            == expected
        )


class TestRecordsSource:
    @pytest.fixture
    def source(self):
        source = RecordsSource(
            AsyncMock(),
            dict(
                table="change_request",
                instance=dict(
                    host="http://my.host.name", username="user", password="pass"
                ),
                sysparm_query="foo",
                remote_servicenow_timezone="America/New_York",
            ),
        )
        source.table_client = Mock()
        source.initial_polling_start_time = datetime(
            2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc
        )
        # Ensure remote_snow_timezone is set on the object
        if (
            not hasattr(source, "remote_snow_timezone")
            or source.remote_snow_timezone is None
        ):
            source.remote_snow_timezone = ZoneInfo("America/New_York")
        return source

    @pytest.fixture
    def custom_source(self):
        source = RecordsSource(
            AsyncMock(),
            dict(
                table="u_custom_table",
                instance=dict(
                    host="http://my.host.name", username="user", password="pass"
                ),
                sysparm_query="foo",
                timestamp_field="u_last_modified",
                order_by_field="u_last_modified",
                remote_servicenow_timezone="America/New_York",
            ),
        )
        source.table_client = Mock()
        source.initial_polling_start_time = datetime(
            2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc
        )
        # Ensure remote_snow_timezone is set on the object
        if (
            not hasattr(source, "remote_snow_timezone")
            or source.remote_snow_timezone is None
        ):
            source.remote_snow_timezone = ZoneInfo("America/New_York")
        return source

    def test_latest_timestamp_floor(self, source):
        assert source.latest_timestamp_floor == datetime(
            2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc
        )
        source._latest_timestamp_floor = datetime(
            2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc
        )
        assert source.latest_timestamp_floor == datetime(
            2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc
        )

    def test_timestamp_field_configuration(self, custom_source):
        assert custom_source.timestamp_field == "u_last_modified"
        assert custom_source.order_by_field == "u_last_modified"

    def test_default_timestamp_field(self, source):
        assert source.timestamp_field == "sys_updated_on"
        assert source.order_by_field == "sys_updated_on"

    @patch("extensions.eda.plugins.event_source.records.table.TableClient")
    def test_lookup_snow_user_timezone(self, mock_table_client, source):
        # Mock the temporary client
        mock_temp_client = Mock()
        mock_temp_client.list_records.return_value = [
            dict(time_zone="America/New_York", user_name="test_user")
        ]
        mock_table_client.return_value = mock_temp_client

        assert source.lookup_snow_user_timezone() == ZoneInfo("America/New_York")

        # Test error case
        mock_temp_client.list_records.return_value = [dict()]
        with pytest.raises(
            AnsibleParserError, match="Unable to lookup user timezone in ServiceNow:"
        ):
            source.lookup_snow_user_timezone()

    def test_should_record_be_sent_to_queue_old_record(self, source):
        test_record = dict(sys_id="123", sys_updated_on="1900-08-13 12:00:00")
        assert source.should_record_be_sent_to_queue(test_record, dict()) is False

    def test_should_record_be_sent_to_queue_new_record(self, source):
        test_record = dict(sys_id="123", sys_updated_on="2026-08-13 12:00:00")
        reported_records = dict()
        assert (
            source.should_record_be_sent_to_queue(test_record, reported_records) is True
        )
        assert "123" in reported_records

    def test_should_record_be_sent_to_queue_reported_record(self, source):
        source.has_record_been_reported = Mock(return_value=True)
        test_record = dict(sys_id="123", sys_updated_on="2026-08-13 12:00:00")
        assert source.should_record_be_sent_to_queue(test_record, dict()) is False

    def test_should_record_be_sent_to_queue_missing_timestamp_field(self, source):
        test_record = dict(sys_id="123")  # Missing sys_updated_on
        assert source.should_record_be_sent_to_queue(test_record, dict()) is False

    def test_should_record_be_sent_to_queue_custom_timestamp_field(self, custom_source):
        test_record = dict(sys_id="123", u_last_modified="2026-08-13 12:00:00")
        reported_records = dict()
        assert (
            custom_source.should_record_be_sent_to_queue(test_record, reported_records)
            is True
        )
        assert "123" in reported_records

    def test_should_record_be_sent_to_queue_custom_timestamp_missing_field(
        self, custom_source
    ):
        test_record = dict(
            sys_id="123", sys_updated_on="2026-08-13 12:00:00"
        )  # Wrong field
        assert (
            custom_source.should_record_be_sent_to_queue(test_record, dict()) is False
        )

    @pytest.mark.parametrize(
        "test_record, expected",
        [
            (dict(sys_id="123", sys_updated_on="2026-08-13 12:00:00"), True),
            (dict(sys_id="123", sys_updated_on="2026-08-13 12:00:01"), False),
            (dict(sys_id="456", sys_updated_on="2026-08-13 12:00:00"), True),
            (dict(sys_id="456", sys_updated_on="2026-08-13 12:00:01"), False),
            (dict(sys_id="789", sys_updated_on="2026-08-13 12:00:00"), False),
        ],
    )
    def test_has_record_been_reported(self, test_record, expected, source):
        reported_records_this_poll = {
            "123": "2026-08-13 12:00:00",
        }
        source.reported_records_last_poll = {
            "456": "2026-08-13 12:00:00",
        }
        assert (
            source.has_record_been_reported(test_record, reported_records_this_poll)
            is expected
        )

    def test_has_record_been_reported_missing_timestamp_field(self, source):
        test_record = dict(sys_id="123")  # Missing sys_updated_on
        reported_records_this_poll = {}
        assert (
            source.has_record_been_reported(test_record, reported_records_this_poll)
            is False
        )

    def test_has_record_been_reported_custom_timestamp_field(self, custom_source):
        test_record = dict(sys_id="123", u_last_modified="2026-08-13 12:00:00")
        reported_records_this_poll = {
            "123": "2026-08-13 12:00:00",
        }
        custom_source.reported_records_last_poll = {}
        assert (
            custom_source.has_record_been_reported(
                test_record, reported_records_this_poll
            )
            is True
        )

    @pytest.mark.asyncio
    async def test_poll_for_records(self, source):
        source.table_client.list_records.return_value = [
            dict(sys_id="123", sys_updated_on="2026-08-13 12:00:00"),
            dict(sys_id="456", sys_updated_on="2026-08-13 12:00:00"),
            dict(sys_id="789", sys_updated_on="2026-08-13 12:00:00"),
        ]
        source.should_record_be_sent_to_queue = Mock(return_value=True)
        await source._poll_for_records()
        assert source.queue.put.call_count == 3

        source.table_client.list_records.return_value = []
        source.queue.put.reset_mock()
        source.should_record_be_sent_to_queue = Mock(return_value=False)
        await source._poll_for_records()
        assert source.queue.put.call_count == 0

    @pytest.mark.asyncio
    async def test_poll_for_records_custom_timestamp_field(self, custom_source):
        custom_source.table_client.list_records.return_value = [
            dict(sys_id="123", u_last_modified="2026-08-13 12:00:00"),
            dict(sys_id="456", u_last_modified="2026-08-13 12:00:00"),
        ]
        custom_source.should_record_be_sent_to_queue = Mock(return_value=True)
        await custom_source._poll_for_records()
        assert custom_source.queue.put.call_count == 2

    @pytest.mark.asyncio
    async def test_poll_for_records_missing_timestamp_field(self, source):
        source.table_client.list_records.return_value = [
            dict(sys_id="123"),  # Missing sys_updated_on
            dict(sys_id="456", sys_updated_on="2026-08-13 12:00:00"),
        ]
        # Don't mock should_record_be_sent_to_queue - let it use the real logic
        await source._poll_for_records()
        # Should only process the record with the timestamp field
        assert source.queue.put.call_count == 1
