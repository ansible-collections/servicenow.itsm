# -*- coding: utf-8 -*-
# Copyright: (c) 2024, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest
from ansible_collections.servicenow.itsm.plugins.module_utils import errors
from ansible_collections.servicenow.itsm.plugins.modules import catalog_request_info
from ansible_collections.servicenow.itsm.tests.unit.plugins.common.utils import (
    set_module_args,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)

# Test constants
DEFAULT_INSTANCE = dict(host="my.host.name", username="user", password="pass")
SAMPLE_RECORDS = [
    dict(
        request_state="submitted",
        number="REQ0000001",
        sys_id="1234",
        short_description="Test request 1",
        requested_for="john.doe",
        requested_by="jane.smith",
        priority="2",
    ),
    dict(
        request_state="in_process",
        number="REQ0000002",
        sys_id="5678",
        short_description="Test request 2",
        requested_for="alice.wonder",
        requested_by="bob.builder",
        priority="1",
    ),
]


def create_test_module(create_module, **params):
    """Helper function to create module with common defaults."""
    base_params = dict(instance=DEFAULT_INSTANCE)
    base_params.update(params)
    return create_module(params=base_params)


class TestMain:
    def test_all_params(self, run_main):
        params = dict(
            instance=dict(
                host="https://my.host.name", username="user", password="pass"
            ),
            sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
            number="1",
            sysparm_query="short_descriptionLIKElaptop^request_state=submitted",
            query=[{"priority": "= 1"}],
            sysparm_display_value="true",
        )
        with set_module_args(args=params):
            success, result = run_main(catalog_request_info, params)

        assert success is False

    def test_query(self, run_main):
        params = dict(
            instance=dict(
                host="https://my.host.name", username="user", password="pass"
            ),
            query=[{"priority": "= 1"}],
        )
        with set_module_args(args=params):
            success, result = run_main(catalog_request_info, params)

        assert success is True

class TestRun:
    def test_run_query(self, create_module, table_client, mocker):
        module = create_module(
            params=dict(
                instance=dict(
                    host="https://my.host.name", username="user", password="pass"
                ),
                query=[
                    {"priority": "= 1"},
                    {"requested_for": "= john.doe"},
                    {"requested_by": "= jane.smith"},
                    {"assignment_group": "= IT Services"},
                ],
            )
        )
        mocker.patch("ansible_collections.servicenow.itsm.plugins.module_utils.table.find_user", return_value=dict(sys_id="1234"))
        mocker.patch("ansible_collections.servicenow.itsm.plugins.module_utils.table.find_assignment_group", return_value=dict(sys_id="5678"))
        table_client.list_records.return_value = SAMPLE_RECORDS

        records = catalog_request_info.run(module, table_client)
        table_client.list_records.assert_called_once_with(
            "sc_request",
            {'sysparm_query': 'priority=1^NQrequested_for=1234^NQrequested_by=1234^NQassignment_group=5678'}
        )
        assert records == SAMPLE_RECORDS

    def test_run_sysparm_query(self, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(
                    host="https://my.host.name", username="user", password="pass"
                ),
                sysparm_query="short_descriptionLIKElaptop^request_state=submitted",
            )
        )
        table_client.list_records.return_value = SAMPLE_RECORDS

        records = catalog_request_info.run(module, table_client)
        table_client.list_records.assert_called_once_with(
            "sc_request",
            {'sysparm_query': 'short_descriptionLIKElaptop^request_state=submitted'}
        )
        assert records == SAMPLE_RECORDS

    def test_run_other_params(self, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(
                    host="https://my.host.name", username="user", password="pass"
                ),
                sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
                number="1",
                sysparm_display_value="true",
            )
        )
        table_client.list_records.return_value = SAMPLE_RECORDS

        records = catalog_request_info.run(module, table_client)
        table_client.list_records.assert_called_once_with(
            "sc_request",
            {'sys_id': '01a9ec0d3790200044e0bfc8bcbe5dc3', 'number': '1', 'sysparm_display_value': 'true'}
        )
        assert records == SAMPLE_RECORDS

        table_client.list_records.reset_mock()
        module = create_module(
            params=dict(
                instance=dict(
                    host="https://my.host.name", username="user", password="pass"
                ),
                sysparm_display_value="true",
            )
        )
        table_client.list_records.return_value = SAMPLE_RECORDS

        records = catalog_request_info.run(module, table_client)
        table_client.list_records.assert_called_once_with(
            "sc_request",
            {'sysparm_display_value': 'true'}
        )
        assert records == SAMPLE_RECORDS

class TestRemapParams:
    def test_remap_params(self, mocker):
        query = [
            {"priority": "= 1"},
            {"requested_for": "= john.doe"},
            {"requested_by": "= jane.smith"},
            {"assignment_group": "= IT Services"},
        ]
        mocker.patch("ansible_collections.servicenow.itsm.plugins.module_utils.table.find_user", return_value=dict(sys_id="1234"))
        mocker.patch("ansible_collections.servicenow.itsm.plugins.module_utils.table.find_assignment_group", return_value=dict(sys_id="5678"))

        remapped_query = catalog_request_info.remap_params(query, mocker.MagicMock())
        assert remapped_query == [
            {"priority": "= 1"},
            {"requested_for": ("=", "1234")},
            {"requested_by": ("=", "1234")},
            {"assignment_group": ("=", "5678")},
        ]

class TestSysparmsQuery:
    def test_sysparms_query(self, mocker):
        query_param = {
            "query": [{"priority": "= 1"}],
        }
        mocker.patch("ansible_collections.servicenow.itsm.plugins.module_utils.query.parse_query", return_value=("", None))
        mocker.patch("ansible_collections.servicenow.itsm.plugins.modules.catalog_request_info.remap_params")
        mocker.patch("ansible_collections.servicenow.itsm.plugins.module_utils.query.map_query_values")
        mock_serialize = mocker.patch("ansible_collections.servicenow.itsm.plugins.module_utils.query.serialize_query")
        catalog_request_info.sysparms_query(query_param, mocker.MagicMock(), mocker.MagicMock())
        mock_serialize.assert_called_once()

    def test_sysparms_query_error(self, mocker):
        query_param = {
            "query": [{"priority": "= 1"}],
        }
        mocker.patch("ansible_collections.servicenow.itsm.plugins.module_utils.query.parse_query", return_value=('', "error"))
        with pytest.raises(errors.ServiceNowError):
            catalog_request_info.sysparms_query(query_param, mocker.MagicMock(), mocker.MagicMock())
