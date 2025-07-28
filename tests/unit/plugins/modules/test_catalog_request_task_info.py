# -*- coding: utf-8 -*-
# Copyright: (c) 2024, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest
from ansible_collections.servicenow.itsm.plugins.module_utils import errors
from ansible_collections.servicenow.itsm.plugins.modules import (
    catalog_request_task_info,
)
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
        active=True,
        approval="not requested",
        assigned_to="john.doe",
        assignment_group="IT Support",
        close_notes="",
        comments="",
        delivery_plan="",
        delivery_task="",
        description="Install required software and configure user settings",
        due_date="",
        impact="3",
        number="SCTASK0000456",
        opened_at="2024-01-15 10:30:00",
        opened_by="jane.smith",
        order=10,
        priority="2",
        request="REQ0000123",
        requested_by="jane.smith",
        requested_for="john.doe",
        short_description="Configure new laptop",
        state="present",
        sys_created_by="jane.smith",
        sys_created_on="2024-01-15 10:30:00",
        sys_id="c36d93a37b1200001c9c9b5b8a9619a9",
        sys_updated_by="jane.smith",
        sys_updated_on="2024-01-15 10:30:00",
        task_state="open",
        urgency="2",
        work_notes="",
    ),
    dict(
        active=True,
        approval="approved",
        assigned_to="alice.wonder",
        assignment_group="Desktop Support",
        close_notes="Task completed successfully",
        comments="Customer satisfied",
        delivery_plan="",
        delivery_task="",
        description="Setup email client and configure security settings",
        due_date="2024-01-20 17:00:00",
        impact="2",
        number="SCTASK0000789",
        opened_at="2024-01-16 09:15:00",
        opened_by="bob.builder",
        order=20,
        priority="1",
        request="REQ0000456",
        requested_by="bob.builder",
        requested_for="alice.wonder",
        short_description="Setup new workstation",
        state="present",
        sys_created_by="bob.builder",
        sys_created_on="2024-01-16 09:15:00",
        sys_id="d47e84b48c2300002d7d9c6c9b9619b8",
        sys_updated_by="alice.wonder",
        sys_updated_on="2024-01-16 14:30:00",
        task_state="closed_complete",
        urgency="1",
        work_notes="Setup completed as requested",
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
            number="SCTASK0000001",
            sysparm_query="short_descriptionLIKElaptop^task_state=open",
            query=[{"priority": "= 2"}],
            sysparm_display_value="true",
        )
        with set_module_args(args=params):
            success, result = run_main(catalog_request_task_info, params)

        assert success is False

    def test_query(self, run_main):
        params = dict(
            instance=dict(
                host="https://my.host.name", username="user", password="pass"
            ),
            query=[{"priority": "= 2"}],
        )
        with set_module_args(args=params):
            success, result = run_main(catalog_request_task_info, params)

        assert success is True


class TestRun:
    def test_run_query(self, create_module, table_client, mocker):
        module = create_module(
            params=dict(
                instance=dict(
                    host="https://my.host.name", username="user", password="pass"
                ),
                query=[
                    {"priority": "= 2"},
                    {"requested_for": "= john.doe"},
                    {"requested_by": "= jane.smith"},
                    {"assignment_group": "= IT Support"},
                ],
            )
        )
        mocker.patch(
            "ansible_collections.servicenow.itsm.plugins.module_utils.table.find_user",
            return_value=dict(sys_id="1234"),
        )
        mocker.patch(
            "ansible_collections.servicenow.itsm.plugins.module_utils.table.find_assignment_group",
            return_value=dict(sys_id="5678"),
        )
        table_client.list_records.return_value = SAMPLE_RECORDS

        records = catalog_request_task_info.run(module, table_client)
        table_client.list_records.assert_called_once_with(
            "sc_task",
            {
                "sysparm_query": "priority=2^NQrequested_for=1234^NQrequested_by=1234^NQassignment_group=5678"
            },
        )
        assert records == SAMPLE_RECORDS

    def test_run_sysparm_query(self, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(
                    host="https://my.host.name", username="user", password="pass"
                ),
                sysparm_query="short_descriptionLIKElaptop^task_state=open",
            )
        )
        table_client.list_records.return_value = SAMPLE_RECORDS

        records = catalog_request_task_info.run(module, table_client)
        table_client.list_records.assert_called_once_with(
            "sc_task",
            {"sysparm_query": "short_descriptionLIKElaptop^task_state=open"},
        )
        assert records == SAMPLE_RECORDS

    def test_run_other_params(self, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(
                    host="https://my.host.name", username="user", password="pass"
                ),
                sys_id="01a9ec0d3790200044e0bfc8bcbe5dc3",
                number="SCTASK0000456",
                sysparm_display_value="true",
            )
        )
        table_client.list_records.return_value = SAMPLE_RECORDS

        records = catalog_request_task_info.run(module, table_client)
        table_client.list_records.assert_called_once_with(
            "sc_task",
            {
                "sys_id": "01a9ec0d3790200044e0bfc8bcbe5dc3",
                "number": "SCTASK0000456",
                "sysparm_display_value": "true",
            },
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

        records = catalog_request_task_info.run(module, table_client)
        table_client.list_records.assert_called_once_with(
            "sc_task", {"sysparm_display_value": "true"}
        )
        assert records == SAMPLE_RECORDS


class TestRemapParams:
    def test_remap_params(self, mocker):
        query = [
            {"priority": "= 2"},
            {"requested_for": "= john.doe"},
            {"requested_by": "= jane.smith"},
            {"assignment_group": "= IT Support"},
        ]
        mocker.patch(
            "ansible_collections.servicenow.itsm.plugins.module_utils.table.find_user",
            return_value=dict(sys_id="1234"),
        )
        mocker.patch(
            "ansible_collections.servicenow.itsm.plugins.module_utils.table.find_assignment_group",
            return_value=dict(sys_id="5678"),
        )

        remapped_query = catalog_request_task_info.remap_params(
            query, mocker.MagicMock()
        )
        assert remapped_query == [
            {"priority": "= 2"},
            {"requested_for": ("=", "1234")},
            {"requested_by": ("=", "1234")},
            {"assignment_group": ("=", "5678")},
        ]


class TestSysparmsQuery:
    def test_sysparms_query(self, mocker):
        query_param = {
            "query": [{"priority": "= 2"}],
        }
        mocker.patch(
            "ansible_collections.servicenow.itsm.plugins.module_utils.query.parse_query",
            return_value=("", None),
        )
        mocker.patch(
            "ansible_collections.servicenow.itsm.plugins.modules.catalog_request_task_info.remap_params"
        )
        mocker.patch(
            "ansible_collections.servicenow.itsm.plugins.module_utils.query.map_query_values"
        )
        mock_serialize = mocker.patch(
            "ansible_collections.servicenow.itsm.plugins.module_utils.query.serialize_query"
        )
        catalog_request_task_info.sysparms_query(
            query_param, mocker.MagicMock(), mocker.MagicMock()
        )
        mock_serialize.assert_called_once()

    def test_sysparms_query_error(self, mocker):
        query_param = {
            "query": [{"priority": "= 2"}],
        }
        mocker.patch(
            "ansible_collections.servicenow.itsm.plugins.module_utils.query.parse_query",
            return_value=("", "error"),
        )
        with pytest.raises(errors.ServiceNowError):
            catalog_request_task_info.sysparms_query(
                query_param, mocker.MagicMock(), mocker.MagicMock()
            )
