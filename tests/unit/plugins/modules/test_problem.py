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
            state="107", number="PRB0000001", sys_id="1234"
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

        result = problem.build_payload(module, table_client)

        assert result["assigned_to"] == "681ccaf9c0a8016400b98a06818d57c7"
        assert result["problem_state"] == "closed"
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

        result = problem.build_payload(module, table_client)

        assert "problem_state" not in result
        assert result["short_description"] == "Test problem"
        assert result["impact"] == "low"
        assert result["urgency"] == "low"
        assert result["user_input"] == "notes"


class TestValidateParams:
    @pytest.mark.parametrize(
        "params",
        [
            dict(state="new", short_description="a"),
            dict(state="assessment", short_description="a", assigned_to="a"),
            dict(
                state="analysis",
                short_description="a",
                assigned_to="a",
                cause_notes="a",
                fix_notes="a",
            ),
        ],
    )
    def test_valid_unresolved_state(self, params):
        problem.validate_params(dict(params, resolution_code=None))

    @pytest.mark.parametrize("state", ["resolved", "closed"])
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
        "state", ["new", "assessment", "analysis", "in_progress", "resolved", "closed"]
    )
    def test_invalid(self, state):
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
        with pytest.raises(errors.ServiceNowError, match="Missing"):
            problem.validate_params(params)


class TestEnsurePresent:
    def test_ensure_present_create_new(
        self, create_module, table_client, attachment_client
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
            ),
        )
        table_client.create_record.return_value = dict(
            state="101",
            number="PRB0000001",
            short_description="Test problem",
            impact="3",
            urgency="3",
            sys_id="1234",
        )
        attachment_client.upload_records.return_value = []

        result = problem.ensure_present(module, table_client, attachment_client)

        table_client.create_record.assert_called_once()
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
        self, create_module, table_client, attachment_client
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
            ),
        )
        table_client.get_record.return_value = dict(
            state="101",
            problem_state="101",
            number="PRB0000001",
            short_description="Test problem",
            sys_id="1234",
        )
        attachment_client.update_records.return_value = []
        attachment_client.list_records.return_value = []

        result = problem.ensure_present(module, table_client, attachment_client)

        table_client.get_record.assert_called_once()
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
        self, mocker, create_module, table_client, attachment_client
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
                assigned_to=None,
                resolution_code=None,
                fix_notes=None,
                cause_notes=None,
                close_notes=None,
                duplicate_of=None,
                attachments=None,
                other=None,
            ),
        )
        payload_mocker = mocker.patch.object(problem, "build_payload")
        payload_mocker.return_value = dict(
            state="assess",
            problem_state="assess",
            number="PRB0000001",
            short_description="Test problem",
            sys_id="1234",
        )
        table_client.get_record.return_value = dict(
            state="101",
            problem_state="101",
            number="PRB0000001",
            short_description="Test problem",
            sys_id="1234",
        )
        table_client.update_record.return_value = dict(
            state="102",
            problem_state="102",
            number="PRB0000001",
            short_description="Test problem",
            sys_id="1234",
        )
        attachment_client.update_records.return_value = []
        attachment_client.list_records.return_value = []

        result = problem.ensure_present(module, table_client, attachment_client)

        table_client.update_record.assert_called_once()
        assert result == (
            True,
            dict(
                state="assess",
                problem_state="assess",
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
                    state="assess",
                    problem_state="assess",
                    number="PRB0000001",
                    short_description="Test problem",
                    attachments=[],
                    sys_id="1234",
                ),
            ),
        )
