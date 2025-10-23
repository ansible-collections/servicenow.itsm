from __future__ import absolute_import, division, print_function

__metaclass__ = type

from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import pytest
from unittest.mock import patch, AsyncMock, Mock
from ansible.errors import AnsibleParserError
from ansible_collections.servicenow.itsm.extensions.eda.plugins.event_source.records import (
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
        "ansible_collections.servicenow.itsm.extensions.eda.plugins.event_source.records.construct_sysparm_query_from_query"
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
        "sysparm_query, expected",
        [
            (
                "foo",
                "foo^sys_updated_on>=javascript:gs.dateGenerate('2025-01-01', '12:00:00')",
            ),
            (
                "foo^sys_updated_on>2026-01-01 12:00:00",
                "foo^sys_updated_on>=javascript:gs.dateGenerate('2025-01-01', '12:00:00')",
            ),
        ],
    )
    def test_inject_sys_updated_on_filter(self, sysparm_query, expected):
        query_formatter = QueryFormatter()
        test_datetime = datetime(2025, 1, 1, 12, 0, 0)
        tz = timezone.utc
        assert (
            query_formatter.inject_sys_updated_on_filter(
                sysparm_query=sysparm_query,
                sys_update_on_datetime=test_datetime,
                snow_timezone=tz,
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
            ),
        )
        source.table_client = Mock()
        source.initial_polling_start_time = datetime(
            2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc
        )
        return source

    def test_latest_sys_updated_on_floor(self, source):
        assert source.latest_sys_updated_on_floor == datetime(
            2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc
        )
        source._latest_sys_updated_on_floor = datetime(
            2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc
        )
        assert source.latest_sys_updated_on_floor == datetime(
            2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc
        )

    def test_lookup_snow_user_timezone(self, source):
        source.table_client.list_records.return_value = [
            dict(time_zone="America/New_York")
        ]
        assert source.lookup_snow_user_timezone() == ZoneInfo("America/New_York")

        source.table_client.list_records.return_value = [dict()]
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

    @pytest.mark.asyncio
    async def test_poll_for_records(self, source):
        source.table_client.list_records.return_value = [
            dict(sys_id="123", sys_updated_on="2026-08-13 12:00:00"),
            dict(sys_id="456", sys_updated_on="2026-08-13 12:00:00"),
            dict(sys_id="789", sys_updated_on="2026-08-13 12:00:00"),
        ]
        source.should_record_be_sent_to_queue = Mock(return_value=True)
        await source._poll_for_records(ZoneInfo("America/New_York"))
        assert source.queue.put.call_count == 3

        source.table_client.list_records.return_value = []
        source.queue.put.reset_mock()
        source.should_record_be_sent_to_queue = Mock(return_value=False)
        await source._poll_for_records(ZoneInfo("America/New_York"))
        assert source.queue.put.call_count == 0
