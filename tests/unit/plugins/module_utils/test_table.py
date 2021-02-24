# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible_collections.servicenow.itsm.plugins.module_utils import errors, table
from ansible_collections.servicenow.itsm.plugins.module_utils.client import Response

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestTableListRecords:
    def test_empty_response(self, client):
        client.get.return_value = Response(200, '{"result": []}')
        t = table.TableClient(client)

        records = t.list_records("my_table")

        assert [] == records
        client.get.assert_called_with(
            "table/my_table", query=dict(sysparm_exclude_reference_link="true")
        )

    def test_non_empty_response(self, client):
        client.get.return_value = Response(200, '{"result": [{"a": 3, "b": "sys_id"}]}')
        t = table.TableClient(client)

        records = t.list_records("my_table")

        assert [dict(a=3, b="sys_id")] == records

    def test_query_passing(self, client):
        client.get.return_value = Response(200, '{"result": []}')
        t = table.TableClient(client)

        t.list_records("my_table", dict(a="b"))

        client.get.assert_called_with(
            "table/my_table", query=dict(sysparm_exclude_reference_link="true", a="b")
        )


class TestTableGetRecord:
    def test_single_match(self, client):
        client.get.return_value = Response(200, '{"result": [{"a": 3, "b": "sys_id"}]}')
        t = table.TableClient(client)

        record = t.get_record("my_table", dict(our="query"))

        assert dict(a=3, b="sys_id") == record
        client.get.assert_called_with(
            "table/my_table",
            query=dict(sysparm_exclude_reference_link="true", our="query"),
        )

    def test_multiple_matches(self, client):
        client.get.return_value = Response(200, '{"result": [{"a": 3}, {"b": 4}]}')
        t = table.TableClient(client)

        with pytest.raises(errors.ServiceNowError, match="2"):
            t.get_record("my_table", dict(our="query"))

    def test_zero_matches(self, client):
        client.get.return_value = Response(200, '{"result": []}')
        t = table.TableClient(client)

        assert t.get_record("my_table", dict(our="query")) is None

    def test_zero_matches_fail(self, client):
        client.get.return_value = Response(200, '{"result": []}')
        t = table.TableClient(client)

        with pytest.raises(errors.ServiceNowError, match="No"):
            t.get_record("my_table", dict(our="query"), must_exist=True)


class TestTableCreateRecord:
    def test_normal_mode(self, client):
        client.post.return_value = Response(201, '{"result": {"a": 3, "b": "sys_id"}}')
        t = table.TableClient(client)

        record = t.create_record("my_table", dict(a=4), False)

        assert dict(a=3, b="sys_id") == record
        client.post.assert_called_with(
            "table/my_table",
            dict(a=4),
            query=dict(sysparm_exclude_reference_link="true"),
        )

    def test_check_mode(self, client):
        client.post.return_value = Response(201, '{"result": {"a": 3, "b": "sys_id"}}')
        t = table.TableClient(client)

        record = t.create_record("my_table", dict(a=4), True)

        assert dict(a=4) == record
        client.post.assert_not_called()


class TestTableUpdateRecord:
    def test_normal_mode(self, client):
        client.patch.return_value = Response(200, '{"result": {"a": 3, "b": "sys_id"}}')
        t = table.TableClient(client)

        record = t.update_record("my_table", dict(sys_id="id"), dict(a=4), False)

        assert dict(a=3, b="sys_id") == record
        client.patch.assert_called_with(
            "table/my_table/id",
            dict(a=4),
            query=dict(sysparm_exclude_reference_link="true"),
        )

    def test_check_mode(self, client):
        client.patch.return_value = Response(200, '{"result": {"a": 3, "b": "sys_id"}}')
        t = table.TableClient(client)

        record = t.update_record("my_table", dict(sys_id="id"), dict(a=4), True)

        assert dict(sys_id="id", a=4) == record
        client.patch.assert_not_called()


class TestTableDeleteRecord:
    def test_normal_mode(self, client):
        client.delete.return_value = Response(204, "")
        t = table.TableClient(client)

        t.delete_record("my_table", dict(sys_id="id"), False)

        client.delete.assert_called_with("table/my_table/id")

    def test_check_mode(self, client):
        client.delete.return_value = Response(204, "")
        t = table.TableClient(client)

        t.delete_record("my_table", dict(sys_id="id"), True)

        client.delete.assert_not_called()


class TestFindUser:
    def test_user_name_lookup(self, table_client):
        table_client.get_record.return_value = dict(sys_id="1234", user_name="test")

        user = table.find_user(table_client, "test")

        assert dict(sys_id="1234", user_name="test") == user
