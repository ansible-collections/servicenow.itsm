# -*- coding: utf-8 -*-
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest
from ansible_collections.servicenow.itsm.plugins.module_utils import errors
from ansible_collections.servicenow.itsm.plugins.modules import catalog_request_task
from ansible_collections.servicenow.itsm.tests.unit.plugins.common.utils import (
    set_module_args,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)

# Test constants
DEFAULT_INSTANCE = dict(host="my.host.name", username="user", password="pass")
SAMPLE_RECORD = dict(
    state="open",
    number="SCTASK0000001",
    sys_id="1234",
    request="REQ0000001",
    short_description="Test task",
)


def create_test_module(create_module, state="present", **params):
    """Helper function to create module with common defaults."""
    base_params = dict(instance=DEFAULT_INSTANCE, state=state)
    base_params.update(params)
    return create_module(params=base_params)


class TestEnsureAbsent:
    def test_delete_existing_record(self, create_module, table_client):
        module = create_test_module(
            create_module, state="absent", sys_id="1234", number="SCTASK0000001"
        )
        table_client.get_record.return_value = SAMPLE_RECORD

        changed, record, diff = catalog_request_task.ensure_absent(module, table_client)

        table_client.delete_record.assert_called_once()
        assert changed is True
        assert record == SAMPLE_RECORD
        assert diff == dict(before=SAMPLE_RECORD, after=None)

    def test_delete_nonexistent_record(self, create_module, table_client):
        module = create_test_module(create_module, state="absent", sys_id="1234")
        table_client.get_record.return_value = None

        changed, record, diff = catalog_request_task.ensure_absent(module, table_client)

        table_client.delete_record.assert_not_called()
        assert changed is False
        assert record is None
        assert diff == dict(before=None, after=None)


class TestLookupRequestSysId:
    def test_lookup_with_sys_id(self, table_client):
        request_sys_id = "1234567890abcdef1234567890abcdef"
        expected_record = {"sys_id": request_sys_id, "number": "REQ0000001"}
        table_client.get_record.return_value = expected_record

        result = catalog_request_task._lookup_request_sys_id(
            request_sys_id, table_client
        )

        table_client.get_record.assert_called_once_with(
            "sc_request", {"sys_id": request_sys_id}, must_exist=True
        )
        assert result == expected_record

    def test_lookup_with_number(self, table_client):
        request_number = "REQ0000001"
        expected_record = {"sys_id": "1234", "number": request_number}
        table_client.get_record.return_value = expected_record

        result = catalog_request_task._lookup_request_sys_id(
            request_number, table_client
        )

        table_client.get_record.assert_called_once_with(
            "sc_request", {"number": request_number}, must_exist=True
        )
        assert result == expected_record

    def test_lookup_with_short_hex_string_as_number(self, table_client):
        # Test that short hex strings are treated as numbers, not sys_ids
        request_number = "abc123"  # 6 chars, not 32
        expected_record = {"sys_id": "1234", "number": request_number}
        table_client.get_record.return_value = expected_record

        result = catalog_request_task._lookup_request_sys_id(
            request_number, table_client
        )

        table_client.get_record.assert_called_once_with(
            "sc_request", {"number": request_number}, must_exist=True
        )
        assert result == expected_record


class TestBuildPayload:
    def test_build_payload_with_task_state(self, create_module, table_client):
        module = create_test_module(
            create_module,
            task_state="work_in_progress",
            short_description="Test task",
        )

        result = catalog_request_task.build_payload(module, table_client)

        assert result["state"] == "work_in_progress"
        assert result["short_description"] == "Test task"

    def test_build_payload_with_request_sys_id(self, create_module, table_client):
        request_sys_id = "1234567890abcdef1234567890abcdef"
        module = create_test_module(
            create_module,
            request=request_sys_id,
            short_description="Test task",
        )
        table_client.get_record.return_value = {
            "sys_id": request_sys_id,
            "number": "REQ0000001",
        }

        result = catalog_request_task.build_payload(module, table_client)

        table_client.get_record.assert_called_once_with(
            "sc_request", {"sys_id": request_sys_id}, must_exist=True
        )
        assert result["request"] == request_sys_id
        assert result["short_description"] == "Test task"

    def test_build_payload_with_request_number(self, create_module, table_client):
        request_number = "REQ0000001"
        request_sys_id = "req_sys_id_1234"
        module = create_test_module(
            create_module,
            request=request_number,
            short_description="Test task",
        )
        table_client.get_record.return_value = {
            "sys_id": request_sys_id,
            "number": request_number,
        }

        result = catalog_request_task.build_payload(module, table_client)

        table_client.get_record.assert_called_once_with(
            "sc_request", {"number": request_number}, must_exist=True
        )
        assert result["request"] == request_sys_id
        assert result["short_description"] == "Test task"

    def test_build_payload_with_user_lookups(self, create_module, table_client):
        module = create_test_module(
            create_module,
            requested_for="john.doe",
            requested_by="jane.smith",
            assigned_to="admin",
            short_description="Test task",
        )
        # Mock user lookups
        table_client.get_record.side_effect = [
            {"sys_id": "user1_sys_id"},  # requested_for
            {"sys_id": "user2_sys_id"},  # requested_by
            {"sys_id": "user3_sys_id"},  # assigned_to
        ]

        result = catalog_request_task.build_payload(module, table_client)

        expected_calls = [
            (("sys_user", {"user_name": "john.doe"}), {"must_exist": True}),
            (("sys_user", {"user_name": "jane.smith"}), {"must_exist": True}),
            (("sys_user", {"user_name": "admin"}), {"must_exist": True}),
        ]

        assert table_client.get_record.call_count == 3
        for i, (call_args, call_kwargs) in enumerate(expected_calls):
            assert table_client.get_record.call_args_list[i] == (call_args, call_kwargs)

        assert result["requested_for"] == "user1_sys_id"
        assert result["requested_by"] == "user2_sys_id"
        assert result["assigned_to"] == "user3_sys_id"
        assert result["short_description"] == "Test task"

    def test_build_payload_with_assignment_group(self, create_module, table_client):
        module = create_test_module(
            create_module,
            assignment_group="IT Support",
            short_description="Test task",
        )
        table_client.get_record.return_value = {"sys_id": "group_sys_id"}

        result = catalog_request_task.build_payload(module, table_client)

        table_client.get_record.assert_called_once_with(
            "sys_user_group", {"name": "IT Support"}, must_exist=True
        )
        assert result["assignment_group"] == "group_sys_id"
        assert result["short_description"] == "Test task"

    @pytest.mark.parametrize(
        "field,value",
        [
            ("short_description", "Test task"),
            ("description", "Detailed description"),
            ("priority", "1"),
            ("urgency", "2"),
            ("impact", "3"),
            ("comments", "Some comments"),
            ("work_notes", "Work notes"),
            ("due_date", "2024-01-15"),
            ("close_notes", "Closing notes"),
            ("order", 10),
            ("approval", "approved"),
            ("delivery_plan", "Plan A"),
            ("delivery_task", "Task B"),
        ],
    )
    def test_build_payload_direct_fields(
        self, create_module, table_client, field, value
    ):
        module = create_test_module(create_module, **{field: value})

        result = catalog_request_task.build_payload(module, table_client)

        assert result[field] == value

    def test_build_payload_with_other_fields(self, create_module, table_client):
        module = create_test_module(
            create_module,
            short_description="Test task",
            other=dict(
                special_instructions="Handle with care",
                vendor="Dell",
            ),
        )

        result = catalog_request_task.build_payload(module, table_client)

        assert result["short_description"] == "Test task"
        assert result["special_instructions"] == "Handle with care"
        assert result["vendor"] == "Dell"

    def test_build_payload_minimal(self, create_module, table_client):
        module = create_test_module(create_module, short_description="Minimal task")

        result = catalog_request_task.build_payload(module, table_client)

        assert result == {"short_description": "Minimal task"}

    def test_build_payload_all_fields(self, create_module, table_client):
        module = create_test_module(
            create_module,
            task_state="open",
            request="REQ0000001",
            requested_for="john.doe",
            requested_by="jane.smith",
            assignment_group="IT Support",
            assigned_to="admin",
            priority="2",
            urgency="2",
            impact="3",
            short_description="Complete task",
            description="Full description",
            comments="Task comments",
            work_notes="Task work notes",
            due_date="2024-01-30",
            close_notes="Task closure",
            order=5,
            approval="approved",
            delivery_plan="Standard plan",
            delivery_task="DEL001",
        )
        # Mock all lookups
        table_client.get_record.side_effect = [
            {"sys_id": "req_sys_id"},  # request
            {"sys_id": "user1_sys_id"},  # requested_for
            {"sys_id": "user2_sys_id"},  # requested_by
            {"sys_id": "user3_sys_id"},  # assigned_to
            {"sys_id": "group_sys_id"},  # assignment_group
        ]

        result = catalog_request_task.build_payload(module, table_client)

        expected_fields = {
            "state": "open",
            "request": "req_sys_id",
            "requested_for": "user1_sys_id",
            "requested_by": "user2_sys_id",
            "assigned_to": "user3_sys_id",
            "assignment_group": "group_sys_id",
            "priority": "2",
            "urgency": "2",
            "impact": "3",
            "short_description": "Complete task",
            "description": "Full description",
            "comments": "Task comments",
            "work_notes": "Task work notes",
            "due_date": "2024-01-30",
            "close_notes": "Task closure",
            "order": 5,
            "approval": "approved",
            "delivery_plan": "Standard plan",
            "delivery_task": "DEL001",
        }

        for field, value in expected_fields.items():
            assert result[field] == value


class TestEnsurePresent:
    def test_create_new_record(self, create_module, table_client):
        module = create_test_module(
            create_module,
            task_state="open",
            short_description="Test task",
            priority="2",
        )
        new_record = dict(SAMPLE_RECORD, priority="2", short_description="Test task")
        table_client.create_record.return_value = new_record

        changed, record, diff = catalog_request_task.ensure_present(
            module, table_client
        )

        table_client.create_record.assert_called_once()
        assert changed is True
        assert record == new_record
        assert diff["before"] is None
        assert diff["after"] == new_record

    def test_update_existing_record(self, create_module, table_client):
        module = create_test_module(
            create_module,
            number="SCTASK0000001",
            task_state="work_in_progress",  # Different from existing
            short_description="Updated task",
            priority="1",
        )
        existing_record = dict(
            SAMPLE_RECORD, priority="2", short_description="Old task", state="open"
        )
        updated_record = dict(
            SAMPLE_RECORD,
            state="work_in_progress",
            priority="1",
            short_description="Updated task",
        )

        table_client.get_record.return_value = existing_record
        table_client.update_record.return_value = updated_record

        changed, record, diff = catalog_request_task.ensure_present(
            module, table_client
        )

        table_client.update_record.assert_called_once()
        assert changed is True
        assert record == updated_record
        assert diff["before"] == existing_record
        assert diff["after"] == updated_record

    def test_no_change_needed(self, create_module, table_client):
        module = create_test_module(
            create_module,
            number="SCTASK0000001",
            short_description="Test task",
        )
        existing_record = dict(SAMPLE_RECORD, short_description="Test task")
        table_client.get_record.return_value = existing_record

        changed, record, diff = catalog_request_task.ensure_present(
            module, table_client
        )

        table_client.update_record.assert_not_called()
        assert changed is False
        assert record == existing_record
        assert diff["before"] == existing_record
        assert diff["after"] == existing_record


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
        module = create_test_module(create_module, state=state, number="SCTASK0000001")
        mock_func = mocker.patch.object(
            catalog_request_task, expected_function, return_value=(True, {}, {})
        )

        catalog_request_task.run(module, table_client)

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
            short_description="Test task",
            **{user_field: "nonexistent.user"}
        )
        table_client.get_record.side_effect = errors.ServiceNowError(error_message)

        with pytest.raises(errors.ServiceNowError, match=error_message):
            catalog_request_task.build_payload(module, table_client)

    def test_group_lookup_error(self, create_module, table_client):
        module = create_test_module(
            create_module,
            short_description="Test task",
            assignment_group="nonexistent group",
        )
        table_client.get_record.side_effect = errors.ServiceNowError("Group not found")

        with pytest.raises(errors.ServiceNowError, match="Group not found"):
            catalog_request_task.build_payload(module, table_client)

    def test_request_lookup_error(self, create_module, table_client):
        module = create_test_module(
            create_module,
            short_description="Test task",
            request="nonexistent_request",
        )
        table_client.get_record.side_effect = errors.ServiceNowError(
            "Request not found"
        )

        with pytest.raises(errors.ServiceNowError, match="Request not found"):
            catalog_request_task.build_payload(module, table_client)


class TestMain:
    def test_missing_required_fields_for_absent_state(self, run_main):
        params = dict(
            instance=DEFAULT_INSTANCE,
            state="absent",
            # Missing required sys_id or number
        )
        with set_module_args(args=params):
            success, result = run_main(catalog_request_task, params)

        assert success is False
        assert "missing" in result["msg"].lower()

    def test_minimal_set_of_params(self, run_main):
        params = dict(
            instance=DEFAULT_INSTANCE,
            state="present",
            short_description="Test task",
        )
        with set_module_args(args=params):
            success, result = run_main(catalog_request_task, params)

        assert success is True

    def test_all_params_present_state(self, run_main):
        params = dict(
            instance=DEFAULT_INSTANCE,
            state="present",
            sys_id="1234",
            number="SCTASK0000001",
            task_state="open",
            request="REQ0000001",
            short_description="Test task",
            description="Detailed description",
            priority="2",
            urgency="3",
            impact="2",
            requested_for="john.doe",
            requested_by="jane.smith",
            assignment_group="IT Support",
            assigned_to="admin",
            comments="Task comments",
            work_notes="Work notes",
            due_date="2024-01-15",
            close_notes="Closure notes",
            order=10,
            approval="approved",
            delivery_plan="Standard",
            delivery_task="DEL001",
        )
        with set_module_args(args=params):
            success, result = run_main(catalog_request_task, params)

        assert success is True

    def test_absent_state_with_sys_id(self, run_main):
        params = dict(
            instance=DEFAULT_INSTANCE,
            state="absent",
            sys_id="1234",
        )
        with set_module_args(args=params):
            success, result = run_main(catalog_request_task, params)

        assert success is True

    def test_absent_state_with_number(self, run_main):
        params = dict(
            instance=DEFAULT_INSTANCE,
            state="absent",
            number="SCTASK0000001",
        )
        with set_module_args(args=params):
            success, result = run_main(catalog_request_task, params)

        assert success is True

    def test_with_other_params(self, run_main):
        params = dict(
            instance=DEFAULT_INSTANCE,
            state="present",
            short_description="Test task",
            other=dict(
                special_instructions="Handle with care",
                vendor="Dell",
                location="Data Center 1",
            ),
        )
        with set_module_args(args=params):
            success, result = run_main(catalog_request_task, params)

        assert success is True

    def test_task_state_choices(self, run_main):
        valid_states = [
            "pending",
            "open",
            "work_in_progress",
            "closed_complete",
            "closed_incomplete",
            "closed_skipped",
        ]

        for task_state in valid_states:
            params = dict(
                instance=DEFAULT_INSTANCE,
                state="present",
                task_state=task_state,
                short_description="Test task",
            )
            with set_module_args(args=params):
                success, result = run_main(catalog_request_task, params)

            assert success is True

    @pytest.mark.parametrize(
        "choice_field,valid_choices",
        [
            ("priority", ["1", "2", "3", "4", "5"]),
            ("urgency", ["1", "2", "3"]),
            ("impact", ["1", "2", "3"]),
            ("approval", ["requested", "approved", "rejected", "not requested"]),
        ],
    )
    def test_choice_field_validation(self, run_main, choice_field, valid_choices):
        for choice in valid_choices:
            params = dict(
                instance=DEFAULT_INSTANCE,
                state="present",
                short_description="Test task",
                **{choice_field: choice}
            )
            with set_module_args(args=params):
                success, result = run_main(catalog_request_task, params)

            assert success is True

    def test_order_integer_field(self, run_main):
        params = dict(
            instance=DEFAULT_INSTANCE,
            state="present",
            short_description="Test task",
            order=42,
        )
        with set_module_args(args=params):
            success, result = run_main(catalog_request_task, params)

        assert success is True
