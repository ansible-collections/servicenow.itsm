from __future__ import absolute_import, division, print_function

__metaclass__ = type

import datetime
import pytest
import mock
from ansible_collections.servicenow.itsm.extensions.eda.plugins.event_source.records import (
    RecordsSource,
)


@pytest.fixture
def source():
    source = RecordsSource(
        mock.AsyncMock(),
        dict(
            table="change_request",
            instance=dict(
                host="http://my.host.name", username="user", password="pass"
            ),
            sysparm_query="foo",
        ),
    )
    source.updated_since = datetime.datetime(2025, 1, 1, 12, 0, 0)
    return source


class TestRecordsSource:
    @pytest.mark.asyncio
    async def test_poll_for_records(self, source):
        source.table_client.list_records = mock.Mock(
            return_value=[
                dict(sys_id="1", sys_updated_on="2024-01-01 12:00:00"),
                dict(sys_id="2", sys_updated_on="2025-02-01 12:00:00"),
                dict(sys_id="3", sys_updated_on="2025-02-02 12:00:00"),
            ]
        )
        source.process_record = mock.AsyncMock()
        await source._poll_for_records()
        assert source.process_record.call_count == 3

    @pytest.mark.asyncio
    async def test_process_record(self, source):
        source.has_record_been_reported = mock.Mock(return_value=True)

        # test a record that is older than the updated_since time
        record = dict(sys_id="123", sys_updated_on="2024-01-01 12:00:00")
        await source.process_record(record, dict())
        source.queue.put.assert_not_called()
        source.has_record_been_reported.assert_not_called()

        # test a record that has already been reported
        record = dict(sys_id="123", sys_updated_on="2025-02-01 12:00:00")
        await source.process_record(record, dict())
        source.queue.put.assert_not_called()
        source.has_record_been_reported.assert_called_once()

        # test a record that has not been reported
        record = dict(sys_id="123", sys_updated_on="2025-02-01 12:00:00")
        source.has_record_been_reported.return_value = False
        await source.process_record(record, dict())
        source.queue.put.assert_called_with(record)

    def test_has_record_been_reported(self, source):
        source.previously_reported_records = {
            "123": "2025-08-13 12:00:00",
        }
        assert source.has_record_been_reported(
            dict(sys_id="123", sys_updated_on="2025-08-13 12:00:00")
        )
        assert not source.has_record_been_reported(
            dict(sys_id="123", sys_updated_on="2025-08-13 12:00:01")
        )
        assert not source.has_record_been_reported(
            dict(sys_id="456", sys_updated_on="2025-08-13 12:00:00")
        )

    def test_parse_string_to_datetime(self, source):
        assert source.parse_string_to_datetime(
            "2025-08-13 12:00:00"
        ) == datetime.datetime(2025, 8, 13, 12, 0, 0)
        assert isinstance(source.parse_string_to_datetime(), datetime.datetime)

        with pytest.raises(ValueError, match="Invalid date string: 2025-08-13"):
            source.parse_string_to_datetime("2025-08-13")
