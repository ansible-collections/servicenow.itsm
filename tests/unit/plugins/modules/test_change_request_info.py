# -*- coding: utf-8 -*-
# # Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible_collections.servicenow.itsm.plugins.modules import change_request_info

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestRemapCaller:
    def test_remap_params(self, table_client):
        query = [
            {"type": ("=", "normal")},
            {"hold_reason": ("=", "Some reason")},
            {"requested_by": ("=", "some.user")},
            {"assignment_group": ("=", "Network")},
            {"template": ("=", "Some template")},
            {"impact": ("=", "low")},
        ]
        table_client.get_record.side_effect = [
            {"sys_id": "681ccaf9c0a8016400b98a06818d57c7"},
            {"sys_id": "d625dccec0a8016700a222a0f7900d06"},
            {"sys_id": "deb8544047810200e90d87e8dee490af"},
        ]

        result = change_request_info.remap_params(query, table_client)

        assert result == [
            {"chg_model": ("=", "normal")},
            {"on_hold_reason": ("=", "Some reason")},
            {"requested_by": ("=", "681ccaf9c0a8016400b98a06818d57c7")},
            {"assignment_group": ("=", "d625dccec0a8016700a222a0f7900d06")},
            {
                "std_change_producer_version": (
                    "=",
                    "deb8544047810200e90d87e8dee490af",
                )
            },
            {"impact": ("=", "low")},
        ]


class TestMain:
    def test_minimal_set_of_params(self, run_main):
        params = dict(
            instance=dict(host="my.host.name", username="user", password="pass"),
        )
        success, result = run_main(change_request_info, params)

        assert success is True

    def test_all_params(self, run_main):
        params = dict(
            instance=dict(host="my.host.name", username="user", password="pass"),
            sys_id="id",
            number="n",
        )
        success, result = run_main(change_request_info, params)

        assert success is True

    def test_fail(self, run_main):
        success, result = run_main(change_request_info)

        assert success is False
        assert "instance" in result["msg"]


class TestRun:
    def test_run(self, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(host="my.host.name", username="user", password="pass"),
                sys_id=None,
                number="n",
                query=None,
            )
        )
        table_client.list_records.return_value = [dict(p=1), dict(q=2), dict(r=3)]

        change_requests = change_request_info.run(module, table_client)

        table_client.list_records.assert_called_once_with(
            "change_request", dict(number="n")
        )
        assert change_requests == [dict(p=1), dict(q=2), dict(r=3)]
