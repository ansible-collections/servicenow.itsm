# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible_collections.servicenow.itsm.plugins.module_utils import errors, table
from ansible_collections.servicenow.itsm.plugins.module_utils.client import Response

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestListRecords:
    def test_empty_response(self, client):
        client.get.return_value = Response(200, '{"result": []}')

        records = table.list_records(client, "my_table")

        assert [] == records
        client.get.assert_called_with("table/my_table", query=None)

    def test_non_empty_response(self, client):
        client.get.return_value = Response(
            200, '{"result": [{"a": 3, "b": {"link": "l", "value": "sys_id"}}]}'
        )

        records = table.list_records(client, "my_table")

        assert [dict(a=3, b="sys_id")] == records

    def test_query_passing(self, client):
        client.get.return_value = Response(200, '{"result": []}')

        table.list_records(client, "my_table", dict(a="b"))

        client.get.assert_called_with("table/my_table", query=dict(a="b"))


class TestGetRecord:
    def test_single_match(self, client):
        client.get.return_value = Response(
            200, '{"result": [{"a": 3, "b": {"link": "l", "value": "sys_id"}}]}'
        )

        record = table.get_record(client, "my_table", dict(our="query"))

        assert dict(a=3, b="sys_id") == record
        client.get.assert_called_with("table/my_table", query=dict(our="query"))

    def test_multiple_matches(self, client):
        client.get.return_value = Response(200, '{"result": [{"a": 3}, {"b": 4}]}')

        with pytest.raises(errors.ServiceNowError, match="2"):
            table.get_record(client, "my_table", dict(our="query"))

    def test_zero_matches(self, client):
        client.get.return_value = Response(200, '{"result": []}')

        assert table.get_record(client, "my_table", dict(our="query")) is None

    def test_zero_matches_fail(self, client):
        client.get.return_value = Response(200, '{"result": []}')

        with pytest.raises(errors.ServiceNowError, match="No"):
            table.get_record(client, "my_table", dict(our="query"), must_exist=True)


class TestCreateRecord:
    def test_normal_mode(self, client):
        client.post.return_value = Response(
            201, '{"result": {"a": 3, "b": {"link": "l", "value": "sys_id"}}}'
        )

        record = table.create_record(client, "my_table", dict(a=4), False)

        assert dict(a=3, b="sys_id") == record
        client.post.assert_called_with("table/my_table", dict(a=4))

    def test_check_mode(self, client):
        client.post.return_value = Response(
            201, '{"result": {"a": 3, "b": {"link": "l", "value": "sys_id"}}}'
        )

        record = table.create_record(client, "my_table", dict(a=4), True)

        assert dict(a=4) == record
        client.post.assert_not_called()


class TestUpdateRecord:
    def test_normal_mode(self, client):
        client.patch.return_value = Response(
            200, '{"result": {"a": 3, "b": {"link": "l", "value": "sys_id"}}}'
        )

        record = table.update_record(
            client, "my_table", dict(sys_id="id"), dict(a=4), False
        )

        assert dict(a=3, b="sys_id") == record
        client.patch.assert_called_with("table/my_table/id", dict(a=4))

    def test_check_mode(self, client):
        client.patch.return_value = Response(
            200, '{"result": {"a": 3, "b": {"link": "l", "value": "sys_id"}}}'
        )

        record = table.update_record(
            client, "my_table", dict(sys_id="id"), dict(a=4), True
        )

        assert dict(sys_id="id", a=4) == record
        client.patch.assert_not_called()


class TestDeleteRecord:
    def test_normal_mode(self, client):
        client.delete.return_value = Response(204, "")

        table.delete_record(client, "my_table", dict(sys_id="id"), False)

        client.delete.assert_called_with("table/my_table/id")

    def test_check_mode(self, client):
        client.delete.return_value = Response(204, "")

        table.delete_record(client, "my_table", dict(sys_id="id"), True)

        client.delete.assert_not_called()
