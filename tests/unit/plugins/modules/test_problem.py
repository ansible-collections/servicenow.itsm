# -*- coding: utf-8 -*-
# # Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible_collections.servicenow.itsm.plugins.modules import problem
from ansible_collections.servicenow.itsm.plugins.module_utils import errors
from ansible_collections.servicenow.itsm.plugins.module_utils.problem import (
    NEW, ASSESS, RCA, FIX, RESOLVED, CLOSED
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestEnsureAbsent:
    def test_delete_problem(self, create_module, table_client, attachment_client):
        module = create_module(
            params=dict(
                instance=dict(host="my.host.name", username="user", password="pass"),
                state="absent",
                number="PRB0000001",
                sys_id="1234",
            )
        )
        table_client.get_record.return_value = dict(
            state=CLOSED, number="PRB0000001", sys_id="1234"
        )

        result = problem.ensure_absent(module, table_client, attachment_client)

        table_client.delete_record.assert_called_once()
        assert result == (
            True,
            None,
            dict(
                before=dict(state="closed", number="PRB0000001", sys_id="1234"),
                after=None,
            ),
        )

    def test_delete_problem_not_present(
        self, create_module, table_client, attachment_client
    ):
        module = create_module(
            params=dict(
                instance=dict(host="my.host.name", username="user", password="pass"),
                state="absent",
                number=None,
                sys_id="1234",
            ),
        )
        table_client.get_record.return_value = None

        result = problem.ensure_absent(module, table_client, attachment_client)

        table_client.delete_record.assert_not_called()
        assert result == (False, None, dict(before=None, after=None))


class TestBuildPayload:
    def test_build_payload(self, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(host="my.host.name", username="user", password="pass"),
                state="closed",
                short_description="Test problem",
                description=None,
                impact="low",
                urgency="low",
                assigned_to="some user",
                resolution_code="duplicate",
                fix_notes=None,
                cause_notes=None,
                close_notes=None,
                duplicate_of="PRB0000010",
                other=None,
            ),
        )
        table_client.get_record.side_effect = [
            {"sys_id": "681ccaf9c0a8016400b98a06818d57c7"},
            {"sys_id": "6816f79cc0a8016401c5a33be04be441"},
        ]

        result = problem.build_payload(module.params, table_client)

        assert result["assigned_to"] == "681ccaf9c0a8016400b98a06818d57c7"
        assert result["state"] == "closed"
        assert result["short_description"] == "Test problem"
        assert result["impact"] == "low"
        assert result["urgency"] == "low"
        assert result["resolution_code"] == "duplicate"
        assert result["duplicate_of"] == "6816f79cc0a8016401c5a33be04be441"

    def test_build_payload_with_other_option(self, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(host="my.host.name", username="user", password="pass"),
                state=None,
                short_description="Test problem",
                description=None,
                impact="low",
                urgency="low",
                assigned_to=None,
                resolution_code=None,
                fix_notes=None,
                cause_notes=None,
                close_notes=None,
                duplicate_of=None,
                other=dict(user_input="notes"),
            ),
        )

        result = problem.build_payload(module.params, table_client)

        assert "problem_state" not in result
        assert result["short_description"] == "Test problem"
        assert result["impact"] == "low"
        assert result["urgency"] == "low"
        assert result["user_input"] == "notes"


class TestValidateParams:
    @pytest.mark.parametrize(
        "params",
        [
            dict(state=NEW, short_description="a"),
            dict(state=ASSESS, short_description="a", assigned_to="a"),
            dict(
                state=RCA,
                short_description="a",
                assigned_to="a",
                cause_notes="a",
                fix_notes="a",
            ),
        ],
    )
    def test_valid_unresolved_state(self, params):
        problem.validate_params(dict(params, resolution_code=None))

    @pytest.mark.parametrize("state", [RESOLVED, CLOSED])
    @pytest.mark.parametrize(
        "params",
        [
            dict(
                short_description="a",
                assigned_to="a",
                resolution_code="fix_applied",
                cause_notes="a",
                fix_notes="a",
            ),
            dict(
                short_description="a",
                assigned_to="a",
                resolution_code="risk_accepted",
                cause_notes="a",
                close_notes="a",
            ),
            dict(
                short_description="a",
                assigned_to="a",
                resolution_code="canceled",
                close_notes="a",
            ),
            dict(
                short_description="a",
                assigned_to="a",
                resolution_code="duplicate",
                duplicate_of="a",
            ),
        ],
    )
    def test_valid_resolved_state(self, state, params):
        problem.validate_params(dict(params, state=state))

    @pytest.mark.parametrize(
        "state", [NEW, ASSESS, RCA, FIX, RESOLVED, CLOSED]
    )
    def test_missing_short_description(self, state):
        params = dict(
            state=state,
            short_description=None,
            assigned_to=None,
            resolution_code=None,
            duplicate_of=None,
            close_notes=None,
            cause_notes=None,
            fix_notes=None,
        )
        with pytest.raises(errors.ServiceNowError, match="short_description"):
            problem.validate_params(params)

    @pytest.mark.parametrize(
        "state", [ASSESS, RCA, FIX, RESOLVED, CLOSED]
    )
    def test_missing_assigned_to(self, state):
        params = dict(
            state=state,
            short_description="short description",
            assigned_to=None,
            resolution_code=None,
            duplicate_of=None,
            close_notes=None,
            cause_notes=None,
            fix_notes=None,
        )
        with pytest.raises(errors.ServiceNowError, match="assigned_to"):
            problem.validate_params(params)

    @pytest.mark.parametrize(
        "state", [RESOLVED, CLOSED]
    )
    def test_missing_resolution_code(self, state):
        params = dict(
            state=state,
            short_description="short description",
            assigned_to="some user",
            resolution_code=None,
            duplicate_of=None,
            close_notes=None,
            cause_notes=None,
            fix_notes=None,
        )
        with pytest.raises(errors.ServiceNowError, match="resolution_code"):
            problem.validate_params(params)

    @pytest.mark.parametrize(
        "param", ["cause_notes", "fix_notes"],
    )
    def test_in_progress_missing_params(self, param):
        params = dict(
            state=FIX,
            short_description="short",
            assigned_to="me",
            resolution_code=None,
            cause_notes=None,
            fix_notes=None,
        )
        params.update({param: "some notes"})
        with pytest.raises(errors.ServiceNowError, match="Missing"):
            problem.validate_params(params)

    @pytest.mark.parametrize(
        "resolution_code,param",
        [
            ("fix_applied", "cause_notes"),
            ("fix_applied", "fix_notes"),
            ("risk_accepted", "cause_notes"),
            ("risk_accepted", "close_notes"),
            ("canceled", "cause_notes"),
            ("duplicate", "fix_notes"),
        ]
    )
    def test_resolution_code_missing_params(self, resolution_code, param):
        params = dict(
            resolution_code=resolution_code,
            state=None,
            cause_notes=None,
            fix_notes=None,
            close_notes=None,
            duplicate_of=None,
        )
        params.update({param: "some notes"})
        with pytest.raises(errors.ServiceNowError, match="Missing"):
            problem.validate_params(params)


class TestEnsurePresent:
    def test_ensure_present_create_new(
        self, create_module, table_client, attachment_client, problem_client
    ):
        module = create_module(
            params=dict(
                instance=dict(host="my.host.name", username="user", password="pass"),
                state="new",
                number=None,
                sys_id=None,
                short_description="Test problem",
                description=None,
                impact="low",
                urgency="low",
                assigned_to=None,
                resolution_code=None,
                fix_notes=None,
                cause_notes=None,
                close_notes=None,
                duplicate_of=None,
                attachments=None,
                other=None,
                base_api_path="/api/path",
            ),
        )
        table_client.create_record.return_value = dict(
            state=NEW,
            number="PRB0000001",
            short_description="Test problem",
            impact="3",
            urgency="3",
            sys_id="1234",
        )
        attachment_client.upload_records.return_value = []

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        table_client.create_record.assert_called_once()
        problem_client.update_record.assert_not_called()
        assert result == (
            True,
            dict(
                state="new",
                number="PRB0000001",
                short_description="Test problem",
                impact="low",
                urgency="low",
                sys_id="1234",
                attachments=[],
            ),
            dict(
                before=None,
                after=dict(
                    state="new",
                    number="PRB0000001",
                    short_description="Test problem",
                    impact="low",
                    urgency="low",
                    sys_id="1234",
                    attachments=[],
                ),
            ),
        )

    def test_ensure_present_nothing_to_do(
        self, create_module, table_client, attachment_client, problem_client
    ):
        module = create_module(
            params=dict(
                instance=dict(host="my.host.name", username="user", password="pass"),
                state="new",
                number="PRB0000001",
                sys_id=None,
                caller=None,
                short_description="Test problem",
                description=None,
                impact=None,
                urgency=None,
                assigned_to=None,
                resolution_code=None,
                fix_notes=None,
                cause_notes=None,
                close_notes=None,
                duplicate_of=None,
                attachments=None,
                other=None,
                base_api_path="/api/path",
            ),
        )
        table_client.get_record.return_value = dict(
            state=NEW,
            problem_state=NEW,
            number="PRB0000001",
            short_description="Test problem",
            sys_id="1234",
        )
        attachment_client.update_records.return_value = []
        attachment_client.list_records.return_value = []

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        table_client.get_record.assert_called_once()
        problem_client.update_record.assert_not_called()
        assert result == (
            False,
            dict(
                state="new",
                problem_state="new",
                number="PRB0000001",
                short_description="Test problem",
                attachments=[],
                sys_id="1234",
            ),
            dict(
                before=dict(
                    state="new",
                    problem_state="new",
                    number="PRB0000001",
                    short_description="Test problem",
                    attachments=[],
                    sys_id="1234",
                ),
                after=dict(
                    state="new",
                    problem_state="new",
                    number="PRB0000001",
                    short_description="Test problem",
                    attachments=[],
                    sys_id="1234",
                ),
            ),
        )

    def test_ensure_present_update(
        self, mocker, create_module, table_client, attachment_client, problem_client
    ):
        module = create_module(
            params=dict(
                instance=dict(host="my.host.name", username="user", password="pass"),
                state="assess",
                number="PRB0000001",
                sys_id=None,
                caller=None,
                short_description="Test problem",
                description=None,
                impact=None,
                urgency=None,
                assigned_to="123abc",
                resolution_code=None,
                fix_notes=None,
                cause_notes=None,
                close_notes=None,
                duplicate_of=None,
                attachments=None,
                other=None,
                base_api_path="/api/path",
            ),
        )
        payload_mocker = mocker.patch.object(problem, "build_payload")
        payload_mocker.return_value = dict(
            state=ASSESS,
            problem_state=ASSESS,
            number="PRB0000001",
            short_description="Test problem",
            sys_id="1234",
            assigned_to="123abc",
        )
        table_client.get_record.return_value = dict(
            state=NEW,
            problem_state=NEW,
            number="PRB0000001",
            short_description="Test problem",
            sys_id="1234",
            assigned_to="",
        )
        table_client.update_record.return_value = payload_mocker.return_value

        attachment_client.update_records.return_value = []
        attachment_client.list_records.return_value = []

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        table_client.update_record.assert_called_once()
        problem_client.update_record.assert_not_called()
        assert result == (
            True,
            dict(
                state="assess",
                problem_state="assess",
                number="PRB0000001",
                short_description="Test problem",
                attachments=[],
                sys_id="1234",
                assigned_to="123abc"
            ),
            dict(
                before=dict(
                    state="new",
                    problem_state="new",
                    number="PRB0000001",
                    short_description="Test problem",
                    attachments=[],
                    sys_id="1234",
                    assigned_to="",
                ),
                after=dict(
                    state="assess",
                    problem_state="assess",
                    number="PRB0000001",
                    short_description="Test problem",
                    attachments=[],
                    sys_id="1234",
                    assigned_to="123abc",
                ),
            ),
        )

    def test_ensure_present_update_with_problem_client(
        self, mocker, create_module, table_client, attachment_client, problem_client
    ):
        module = create_module(
            params=dict(
                instance=dict(host="my.host.name", username="user", password="pass"),
                state="assess",
                number="PRB0000001",
                sys_id=None,
                caller=None,
                short_description="Test problem",
                description=None,
                impact=None,
                urgency=None,
                assigned_to="123abc",
                resolution_code=None,
                fix_notes=None,
                cause_notes=None,
                close_notes=None,
                duplicate_of=None,
                attachments=None,
                other=None,
                base_api_path="/api/path",
            ),
        )
        payload_mocker = mocker.patch.object(problem, "build_payload")
        payload_mocker.return_value = dict(
            state=ASSESS,
            problem_state=ASSESS,
            number="PRB0000001",
            short_description="Test problem",
            sys_id="1234",
            assigned_to="123abc"
        )
        table_client.get_record.return_value = dict(
            state=NEW,
            problem_state=NEW,
            number="PRB0000001",
            short_description="Test problem",
            sys_id="1234",
            assigned_to="",
        )
        table_client.update_record.return_value = table_client.get_record.return_value

        attachment_client.update_records.return_value = []
        attachment_client.list_records.return_value = []

        problem_client.update_record.return_value = payload_mocker.return_value

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        table_client.update_record.assert_called_once()

        problem_client.update_record.assert_called_once_with(
            "PRB0000001",
            dict(
                state=ASSESS,
                problem_state=ASSESS,
                number="PRB0000001",
                short_description="Test problem",
                sys_id="1234",
                assigned_to="123abc"
            ),
        )

        assert result == (
            True,
            dict(
                state="assess",
                problem_state="assess",
                number="PRB0000001",
                short_description="Test problem",
                attachments=[],
                sys_id="1234",
                assigned_to="123abc"
            ),
            dict(
                before=dict(
                    state="new",
                    problem_state="new",
                    number="PRB0000001",
                    short_description="Test problem",
                    attachments=[],
                    sys_id="1234",
                    assigned_to="",
                ),
                after=dict(
                    state="assess",
                    problem_state="assess",
                    number="PRB0000001",
                    short_description="Test problem",
                    attachments=[],
                    sys_id="1234",
                    assigned_to="123abc",
                ),
            ),
        )


class TestProblemMapping:
    def test_state_mapping_create_new(
        self, create_module, table_client, problem_client, attachment_client
    ):
        module = create_module(
            params=dict(
                instance=dict(host="my.host.name", username="user", password="pass"),
                state="my-new",
                number=None,
                sys_id=None,
                caller=None,
                short_description="Test problem",
                description=None,
                impact=None,
                urgency=None,
                assigned_to=None,
                resolution_code=None,
                fix_notes=None,
                cause_notes=None,
                close_notes=None,
                duplicate_of=None,
                attachments=None,
                other=None,
                base_api_path="/api/path",
                problem_mapping=dict(
                    state={
                        NEW: "my-new",
                        ASSESS: "my-assess",
                        RCA: "rca",
                        FIX: "fix",
                        RESOLVED: "my-resolved",
                        CLOSED: "my-closed",
                    }
                )
            ),
        )

        table_client.create_record.return_value = dict(
            state=NEW,
            sys_id="123",
            short_description="Test problem",
            number="PRB0000001",
        )

        attachment_client.upload_records.return_value = []
        attachment_client.list_records.return_value = []

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        sn_payload = dict(
            state=NEW,
            short_description="Test problem",
        )
        table_client.create_record.assert_called_once_with(
            "problem", sn_payload, False
        )

        assert result == (
            True,
            dict(
                state="my-new",
                number="PRB0000001",
                short_description="Test problem",
                attachments=[],
                sys_id="123",
            ),
            dict(
                before=None,
                after=dict(
                    state="my-new",
                    number="PRB0000001",
                    short_description="Test problem",
                    attachments=[],
                    sys_id="123",
                ),
            ),
        )
