# -*- coding: utf-8 -*-
# # Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys
import pytest

from ansible_collections.servicenow.itsm.plugins.modules import api_info
from ansible_collections.servicenow.itsm.plugins.module_utils import errors

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


@pytest.fixture
def missing_field(mocker):
    return "abc"


@pytest.fixture
def superset(mocker):
    return "abc"


class TestRemapCaller:
    def test_remap_params_direct(self, table_client):
        pass

    def test_remap_params_full(self, table_client):
        pass


class TestMain:
    def test_minimal_set_of_params(self, run_main):
        params = dict(
            instance=dict(host="https://my.host.name", username="user", password="pass"),
            resource="sys_user",
        )

        success, result = run_main(api_info, params)

        assert success is True

    def test_all_params(self, run_main):
        params = dict(
            instance=dict(host="https://my.host.name", username="user", password="pass"),
            resource="sys_user",
            sys_id="1234",
            query="upon_reject=cancel",
            display_value="false",
            exclude_reference_link="false",
            fields=["parent", "watch_list"],
            query_category="cat",
            query_no_domain="true",
            no_count="true"
        )

        success, result = run_main(api_info, params)

        assert success is True

    def test_fail(self, run_main):
        success, result = run_main(api_info)

        assert success is False


class TestRun:
    def test_run(self, create_module, table_client):
        params = dict(
            instance=dict(host="https://my.host.name", username="user", password="pass"),
            resource="sys_user",
            fields=["upon_reject", "state", "cmdb_ci"]
        )

        module = create_module(params=params)

        table_client.list_records.return_value = [
            dict(p=1, sys_id=1234),
            dict(q=2, sys_id=4321),
            dict(r=3, sys_id=1212),
        ]

        api_results = api_info.run(module, table_client)

        assert api_results == [dict(p=1, sys_id=1234), dict(q=2, sys_id=4321),dict(r=3, sys_id=1212),]
