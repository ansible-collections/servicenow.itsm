# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
# Copyright: (c) 2021, Ansible Project
# Copyright: (c) 2021, Abhijeet Kasurde <akasurde@redhat.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible_collections.servicenow.itsm.plugins.modules import table_info

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestMain:
    def test_minimal_set_of_params(self, run_main):
        params = dict(
            instance=dict(host="my.host.name", username="user", password="pass"),
        )
        success, result = run_main(table_info, params)

        assert success is True

    def test_all_params(self, run_main):
        params = dict(
            instance=dict(host="my.host.name", username="user", password="pass"),
            sysparm_fields=["name", "label"],
            sysparm_query="nameLIKEts_",
        )
        success, result = run_main(table_info, params)

        assert success is True

    def test_fail(self, run_main):
        success, result = run_main(table_info)

        assert success is False
        assert "instance" in result["msg"]


class TestRun:
    def test_run(self, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(host="my.host.name", username="user", password="pass"),
                sysparm_fields=["name", "label"],
                sysparm_query="nameLIKEts_",
            )
        )
        expected_data = [
            dict(label="Text Index for cmdb_ci_outage", name="ts_c_1_8"),
            dict(label="Text Index for sc_ic_category_request", name="ts_c_8_0"),
        ]
        table_client.list_records.return_value = expected_data

        tables = table_info.run(module, table_client)

        table_client.list_records.assert_called_once_with(
            "sys_db_object",
            dict(sysparm_query="nameLIKEts_", sysparm_fields="name,label"),
        )
        assert tables == expected_data
