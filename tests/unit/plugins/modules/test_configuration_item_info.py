# -*- coding: utf-8 -*-
# # Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible_collections.servicenow.itsm.plugins.modules import configuration_item_info

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestMain:
    def test_minimal_set_of_params(self, run_main):
        params = dict(
            instance=dict(host="my.host.name", username="user", password="pass"),
        )
        success, result = run_main(configuration_item_info, params)

        assert success is True

    def test_all_params(self, run_main):
        params = dict(
            instance=dict(host="my.host.name", username="user", password="pass"),
            sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
            sys_class_name="cmdb_ci",
        )
        success, result = run_main(configuration_item_info, params)

        assert success is True

    def test_fail(self, run_main):
        success, result = run_main(configuration_item_info)

        assert success is False
        assert "instance" in result["msg"]


class TestRun:
    def test_run(self, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(host="my.host.name", username="user", password="pass"),
                sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
                sys_class_name="cmdb_ci",
            )
        )
        table_client.list_records.return_value = [dict(p=1), dict(q=2), dict(r=3)]

        records = configuration_item_info.run(module, table_client)

        table_client.list_records.assert_called_once_with(
            "cmdb_ci", dict(sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3")
        )
        assert records == [dict(p=1), dict(q=2), dict(r=3)]
