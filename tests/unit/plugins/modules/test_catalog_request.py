# -*- coding: utf-8 -*-
# Copyright: (c) 2024, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest
from ansible_collections.servicenow.itsm.plugins.module_utils import errors
from ansible_collections.servicenow.itsm.plugins.modules import catalog_request


pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)

# Test constants
DEFAULT_INSTANCE = dict(host="my.host.name", username="user", password="pass")
SAMPLE_RECORD = dict(request_state="submitted", number="REQ0000001", sys_id="1234")


def create_test_module(create_module, state="present", **params):
    """Helper function to create module with common defaults."""
    base_params = dict(instance=DEFAULT_INSTANCE, state=state)
    base_params.update(params)
    return create_module(params=base_params)


class TestEnsureAbsent:
    def test_delete_existing_record(self, create_module, table_client):
        module = create_test_module(
            create_module, state="absent", sys_id="1234", number="REQ0000001"
        )
        table_client.get_record.return_value = SAMPLE_RECORD

        changed, record, diff = catalog_request.ensure_absent(module, table_client)

        table_client.delete_record.assert_called_once()
        assert changed is True
        assert record == SAMPLE_RECORD
        assert diff == dict(before=SAMPLE_RECORD, after=None)

    def test_delete_nonexistent_record(self, create_module, table_client):
        module = create_test_module(create_module, state="absent", sys_id="1234")
        table_client.get_record.return_value = None

        changed, record, diff = catalog_request.ensure_absent(module, table_client)

        table_client.delete_record.assert_not_called()
        assert changed is False
        assert record is None
        assert diff == dict(before=None, after=None)


class TestBuildPayload:
    def test_build_payload_with_lookups(self, create_module, table_client):
        module = create_test_module(
            create_module,
            request_state="submitted",
            requested_for="john.doe",
            requested_by="jane.smith",
            assignment_group="IT Support",
            assigned_to="admin",
            priority="2",
            short_description="Test request",
        )
        # Mock user and group lookups
        table_client.get_record.side_effect = [
            {"sys_id": "user1_sys_id"},  # requested_for
            {"sys_id": "user2_sys_id"},  # requested_by
            {"sys_id": "user3_sys_id"},  # assigned_to
            {"sys_id": "group_sys_id"},  # assignment_group
        ]

        result = catalog_request.build_payload(module, table_client)

        expected_fields = {
            "request_state": "submitted",
            "short_description": "Test request",
            "priority": "2",
            "requested_for": "user1_sys_id",
            "requested_by": "user2_sys_id",
            "assigned_to": "user3_sys_id",
            "assignment_group": "group_sys_id",
        }
        for field, value in expected_fields.items():
            assert result[field] == value

    @pytest.mark.parametrize(
        "field,value",
        [
            ("short_description", "Test request"),
            ("priority", "1"),
            ("urgency", "2"),
            ("impact", "3"),
            ("request_state", "draft"),
        ],
    )
    def test_build_payload_direct_fields(
        self, create_module, table_client, field, value
    ):
        module = create_test_module(create_module, **{field: value})

        result = catalog_request.build_payload(module, table_client)

        assert result[field] == value

    def test_build_payload_with_other_fields(self, create_module, table_client):
        module = create_test_module(
            create_module,
            short_description="Test request",
            other=dict(
                special_instructions="Handle with care",
                business_justification="Required for project",
            ),
        )

        result = catalog_request.build_payload(module, table_client)

        assert result["short_description"] == "Test request"
        assert result["special_instructions"] == "Handle with care"
        assert result["business_justification"] == "Required for project"

    def test_build_payload_minimal(self, create_module, table_client):
        module = create_test_module(create_module, short_description="Minimal request")

        result = catalog_request.build_payload(module, table_client)

        assert result == {"short_description": "Minimal request"}


class TestEnsurePresent:
    def test_create_new_record(self, create_module, table_client):
        module = create_test_module(
            create_module,
            request_state="submitted",
            short_description="Test request",
            priority="2",
        )
        new_record = dict(SAMPLE_RECORD, priority="2", short_description="Test request")
        table_client.create_record.return_value = new_record

        changed, record, diff = catalog_request.ensure_present(module, table_client)

        table_client.create_record.assert_called_once()
        assert changed is True
        assert record == new_record
        assert diff["before"] is None
        assert diff["after"] == new_record

    def test_update_existing_record(self, create_module, table_client):
        module = create_test_module(
            create_module,
            number="REQ0000001",
            request_state="in_process",  # Different from existing
            short_description="Updated request",
            priority="1",
        )
        existing_record = dict(
            SAMPLE_RECORD, priority="2", short_description="Old request"
        )
        updated_record = dict(
            SAMPLE_RECORD,
            request_state="in_process",
            priority="1",
            short_description="Updated request",
        )

        table_client.get_record.return_value = existing_record
        table_client.update_record.return_value = updated_record

        changed, record, diff = catalog_request.ensure_present(module, table_client)

        table_client.update_record.assert_called_once()
        assert changed is True
        assert record == updated_record
        assert diff["before"] == existing_record
        assert diff["after"] == updated_record


class TestRun:
    @pytest.mark.parametrize(
        "state,expected_function",
        [
            ("absent", "ensure_absent"),
            ("present", "ensure_present"),
        ],
    )
    def test_run_delegates_correctly(
        self, create_module, table_client, mocker, state, expected_function
    ):
        module = create_test_module(create_module, state=state, number="REQ0000001")
        mock_func = mocker.patch.object(
            catalog_request, expected_function, return_value=(True, {}, {})
        )

        catalog_request.run(module, table_client)

        mock_func.assert_called_once_with(module, table_client)


class TestErrorHandling:
    @pytest.mark.parametrize(
        "user_field,error_message",
        [
            ("requested_for", "User not found"),
            ("requested_by", "User not found"),
            ("assigned_to", "User not found"),
        ],
    )
    def test_user_lookup_errors(
        self, create_module, table_client, user_field, error_message
    ):
        module = create_test_module(
            create_module,
            short_description="Test request",
            **{user_field: "nonexistent.user"}
        )
        table_client.get_record.side_effect = errors.ServiceNowError(error_message)

        with pytest.raises(errors.ServiceNowError, match=error_message):
            catalog_request.build_payload(module, table_client)

    def test_group_lookup_error(self, create_module, table_client):
        module = create_test_module(
            create_module,
            short_description="Test request",
            assignment_group="nonexistent group",
        )
        table_client.get_record.side_effect = errors.ServiceNowError("Group not found")

        with pytest.raises(errors.ServiceNowError, match="Group not found"):
            catalog_request.build_payload(module, table_client)


class TestMain:
    def test_missing_required_fields_for_absent_state(self, run_main):
        success, result = run_main(
            catalog_request,
            dict(
                instance=DEFAULT_INSTANCE,
                state="absent",
                # Missing required sys_id or number
            ),
        )

        assert success is False
        assert "missing" in result["msg"].lower()
