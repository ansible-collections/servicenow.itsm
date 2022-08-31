# -*- coding: utf-8 -*-
# # Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from venv import create

__metaclass__ = type

import sys

import pytest

from ansible_collections.servicenow.itsm.plugins.modules import problem
from ansible_collections.servicenow.itsm.plugins.module_utils import errors
from ansible_collections.servicenow.itsm.plugins.module_utils.utils import get_mapper
from ansible_collections.servicenow.itsm.plugins.module_utils.problem import (
    NEW, ASSESS, PAYLOAD_FIELDS_MAPPING, RCA, FIX, RESOLVED, CLOSED
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

        mapper = get_mapper(module, "problem_mapping", PAYLOAD_FIELDS_MAPPING, implicit=True)
        sn_params = mapper.to_snow(module.params)

        result = problem.build_payload(sn_params, table_client)

        assert result["assigned_to"] == "681ccaf9c0a8016400b98a06818d57c7"
        assert result["state"] == CLOSED
        assert result["short_description"] == "Test problem"
        assert result["impact"] == "3"
        assert result["urgency"] == "3"
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

        mapper = get_mapper(module, "problem_mapping", PAYLOAD_FIELDS_MAPPING, implicit=True)
        sn_params = mapper.to_snow(module.params)

        result = problem.build_payload(sn_params, table_client)

        assert "problem_state" not in result
        assert result["short_description"] == "Test problem"
        assert result["impact"] == "3"
        assert result["urgency"] == "3"
        assert result["user_input"] == "notes"

    def test_build_payload_with_mapping(self, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(host="my.host.name", username="user", password="pass"),
                state="my-closed",
                short_description="Test problem",
                description=None,
                impact="lowest",
                urgency="low",
                assigned_to="some user",
                resolution_code="duplicate",
                fix_notes=None,
                cause_notes=None,
                close_notes=None,
                duplicate_of="PRB0000010",
                other=None,
                problem_mapping=dict(
                    state={
                        CLOSED: "my-closed",
                    },
                    impact={
                        "3": "lowest",
                    }
                ),
            ),
        )
        table_client.get_record.side_effect = [
            {"sys_id": "681ccaf9c0a8016400b98a06818d57c7"},
            {"sys_id": "6816f79cc0a8016401c5a33be04be441"},
        ]

        mapper = get_mapper(module, "problem_mapping", PAYLOAD_FIELDS_MAPPING, implicit=True)
        sn_params = mapper.to_snow(module.params)

        result = problem.build_payload(sn_params, table_client)

        assert result["assigned_to"] == "681ccaf9c0a8016400b98a06818d57c7"
        assert result["state"] == CLOSED
        assert result["short_description"] == "Test problem"
        assert result["impact"] == "3"
        assert result["urgency"] == "3"
        assert result["resolution_code"] == "duplicate"
        assert result["duplicate_of"] == "6816f79cc0a8016401c5a33be04be441"


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
    def create_empty_module_params(self):
        return dict(
            instance=dict(host="my.host.name", username="user", password="pass"),
            state=None,
            number=None,
            sys_id=None,
            caller=None,
            short_description=None,
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
            base_api_path=None,
            problem_mapping=None,
        )

    def get_state_mapping(self):
        return {
            NEW: "my-new",
            ASSESS: "my-assess",
            RCA: "rca",
            FIX: "fix",
            RESOLVED: "my-resolved",
            CLOSED: "my-closed",
        }

    def test_create_mapped_problem_state_new(
        self, create_module, table_client, problem_client, attachment_client
    ):
        module_params = self.create_empty_module_params()
        module_params.update(
            dict(
                state="my-new",
                short_description="Test problem",
                base_api_path="/api/path",
                problem_mapping=dict(
                    state=self.get_state_mapping(),
                ),
            )
        )
        module = create_module(params=module_params)

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

    def test_create_mapped_problem_state_assess(
        self, create_module, table_client, problem_client, attachment_client
    ):
        module_params = self.create_empty_module_params()
        module_params.update(
            dict(
                state="my-assess",
                short_description="Test problem",
                assigned_to="problem.admin",
                base_api_path="/api/path",
                problem_mapping=dict(
                    state=self.get_state_mapping(),
                ),
            )
        )
        module = create_module(params=module_params)

        table_client.create_record.return_value = dict(
            state=ASSESS,
            sys_id="123",
            short_description="Test problem",
            assigned_to="123456",
            number="PRB0000001",
        )

        table_client.get_record.side_effect = [
            {"sys_id": "123456"},
        ]

        attachment_client.upload_records.return_value = []
        attachment_client.list_records.return_value = []

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        table_client.create_record.assert_called_once_with(
            "problem",
            dict(
                state=ASSESS, short_description="Test problem",
                assigned_to="123456"
            ),
            False,
        )

        assert result == (
            True,
            dict(
                state="my-assess",
                number="PRB0000001",
                short_description="Test problem",
                assigned_to="123456",
                attachments=[],
                sys_id="123",
            ),
            dict(
                before=None,
                after=dict(
                    state="my-assess",
                    number="PRB0000001",
                    short_description="Test problem",
                    assigned_to="123456",
                    attachments=[],
                    sys_id="123",
                ),
            ),
        )

    def test_create_mapped_problem_state_rca(
        self, create_module, table_client, problem_client, attachment_client
    ):
        module_params = self.create_empty_module_params()
        module_params.update(
            dict(
                state="rca",
                short_description="Test problem",
                assigned_to="problem.admin",
                base_api_path="/api/path",
                problem_mapping=dict(
                    state=self.get_state_mapping(),
                ),
            )
        )
        module = create_module(params=module_params)

        table_client.create_record.return_value = dict(
            state=RCA,
            sys_id="123",
            short_description="Test problem",
            assigned_to="123456",
            number="PRB0000001",
        )

        table_client.get_record.side_effect = [
            {"sys_id": "123456"},
        ]

        attachment_client.upload_records.return_value = []
        attachment_client.list_records.return_value = []

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        table_client.create_record.assert_called_once_with(
            "problem",
            dict(
                state=RCA, short_description="Test problem",
                assigned_to="123456"
            ),
            False,
        )

        assert result == (
            True,
            dict(
                state="rca",
                number="PRB0000001",
                short_description="Test problem",
                assigned_to="123456",
                attachments=[],
                sys_id="123",
            ),
            dict(
                before=None,
                after=dict(
                    state="rca",
                    number="PRB0000001",
                    short_description="Test problem",
                    assigned_to="123456",
                    attachments=[],
                    sys_id="123",
                ),
            ),
        )

    def test_create_mapped_problem_state_fix(
        self, create_module, table_client, problem_client, attachment_client
    ):
        module_params = self.create_empty_module_params()
        module_params.update(
            dict(
                state="fix",
                short_description="Test problem",
                assigned_to="problem.admin",
                fix_notes="some fix notes",
                cause_notes="some cause notes",
                base_api_path="/api/path",
                problem_mapping=dict(
                    state=self.get_state_mapping(),
                ),
            )
        )
        module = create_module(params=module_params)

        table_client.create_record.return_value = dict(
            state=FIX,
            sys_id="123",
            short_description="Test problem",
            assigned_to="123456",
            number="PRB0000001",
            fix_notes="some fix notes",
            cause_notes="some cause notes",
        )

        table_client.get_record.side_effect = [
            {"sys_id": "123456"},
        ]

        attachment_client.upload_records.return_value = []
        attachment_client.list_records.return_value = []

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        table_client.create_record.assert_called_once_with(
            "problem",
            dict(
                state=FIX, short_description="Test problem",
                assigned_to="123456", fix_notes="some fix notes",
                cause_notes="some cause notes",
            ),
            False,
        )

        assert result == (
            True,
            dict(
                state="fix",
                number="PRB0000001",
                short_description="Test problem",
                assigned_to="123456",
                fix_notes="some fix notes",
                cause_notes="some cause notes",
                attachments=[],
                sys_id="123",
            ),
            dict(
                before=None,
                after=dict(
                    state="fix",
                    number="PRB0000001",
                    short_description="Test problem",
                    assigned_to="123456",
                    fix_notes="some fix notes",
                    cause_notes="some cause notes",
                    attachments=[],
                    sys_id="123",
                ),
            ),
        )

    def test_create_mapped_problem_state_resolved(
        self, create_module, table_client, problem_client, attachment_client
    ):
        module_params = self.create_empty_module_params()
        module_params.update(
            dict(
                state="my-resolved",
                short_description="Test problem",
                assigned_to="problem.admin",
                fix_notes="some fix notes",
                cause_notes="some cause notes",
                resolution_code="fix_applied",
                base_api_path="/api/path",
                problem_mapping=dict(
                    state=self.get_state_mapping(),
                ),
            )
        )
        module = create_module(params=module_params)

        table_client.create_record.return_value = dict(
            state=RESOLVED,
            sys_id="123",
            short_description="Test problem",
            assigned_to="123456",
            number="PRB0000001",
            fix_notes="some fix notes",
            cause_notes="some cause notes",
            resolution_code="fix_applied",
        )

        table_client.get_record.side_effect = [
            {"sys_id": "123456"},
        ]

        attachment_client.upload_records.return_value = []
        attachment_client.list_records.return_value = []

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        table_client.create_record.assert_called_once_with(
            "problem",
            dict(
                state=RESOLVED, short_description="Test problem",
                assigned_to="123456", fix_notes="some fix notes",
                cause_notes="some cause notes",
                resolution_code="fix_applied",
            ),
            False,
        )

        assert result == (
            True,
            dict(
                state="my-resolved",
                number="PRB0000001",
                short_description="Test problem",
                assigned_to="123456",
                fix_notes="some fix notes",
                cause_notes="some cause notes",
                resolution_code="fix_applied",
                attachments=[],
                sys_id="123",
            ),
            dict(
                before=None,
                after=dict(
                    state="my-resolved",
                    number="PRB0000001",
                    short_description="Test problem",
                    assigned_to="123456",
                    fix_notes="some fix notes",
                    cause_notes="some cause notes",
                    resolution_code="fix_applied",
                    attachments=[],
                    sys_id="123",
                ),
            ),
        )

    def test_create_mapped_problem_state_closed(
        self, create_module, table_client, problem_client, attachment_client
    ):
        module_params = self.create_empty_module_params()
        module_params.update(
            dict(
                state="my-closed",
                short_description="Test problem",
                assigned_to="problem.admin",
                fix_notes="some fix notes",
                cause_notes="some cause notes",
                resolution_code="fix_applied",
                base_api_path="/api/path",
                problem_mapping=dict(
                    state=self.get_state_mapping(),
                ),
            )
        )
        module = create_module(params=module_params)

        table_client.create_record.return_value = dict(
            state=CLOSED,
            sys_id="123",
            short_description="Test problem",
            assigned_to="123456",
            number="PRB0000001",
            fix_notes="some fix notes",
            cause_notes="some cause notes",
            resolution_code="fix_applied",
        )

        table_client.get_record.side_effect = [
            {"sys_id": "123456"},
        ]

        attachment_client.upload_records.return_value = []
        attachment_client.list_records.return_value = []

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        table_client.create_record.assert_called_once_with(
            "problem",
            dict(
                state=CLOSED, short_description="Test problem",
                assigned_to="123456", fix_notes="some fix notes",
                cause_notes="some cause notes",
                resolution_code="fix_applied",
            ),
            False,
        )

        assert result == (
            True,
            dict(
                state="my-closed",
                number="PRB0000001",
                short_description="Test problem",
                assigned_to="123456",
                fix_notes="some fix notes",
                cause_notes="some cause notes",
                resolution_code="fix_applied",
                attachments=[],
                sys_id="123",
            ),
            dict(
                before=None,
                after=dict(
                    state="my-closed",
                    number="PRB0000001",
                    short_description="Test problem",
                    assigned_to="123456",
                    fix_notes="some fix notes",
                    cause_notes="some cause notes",
                    resolution_code="fix_applied",
                    attachments=[],
                    sys_id="123",
                ),
            ),
        )

    def test_create_mapped_problem_state_non_mapped(self, create_module):
        module_params = self.create_empty_module_params()
        module_params.update(
            dict(
                state="closed",
                short_description="Test problem",
                assigned_to="problem.admin",
                fix_notes="some fix notes",
                cause_notes="some cause notes",
                resolution_code="fix_applied",
                base_api_path="/api/path",
                problem_mapping=dict(
                    state=self.get_state_mapping(),
                ),
            )
        )
        module = create_module(params=module_params)

        with pytest.raises(
            errors.ServiceNowError, match="does not use a value from the mapping"
        ):
            problem.ensure_present(module, None, None, None)

    def test_create_implicitly_mapped_problem_state(self, create_module, table_client, problem_client, attachment_client):
        module_params = self.create_empty_module_params()
        module_params.update(
            dict(
                state="assess",  # implicitly mapped
                short_description="Test problem",
                assigned_to="problem.admin",
                base_api_path="/api/path",
                problem_mapping=dict(
                    state={
                        NEW: "my-new"
                    },
                ),
            )
        )
        module = create_module(params=module_params)

        table_client.create_record.return_value = dict(
            state=ASSESS,
            sys_id="123",
            short_description="Test problem",
            assigned_to="123456",
        )

        table_client.get_record.side_effect = [
            {"sys_id": "123456"},
        ]

        attachment_client.upload_records.return_value = []
        attachment_client.list_records.return_value = []

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        table_client.create_record.assert_called_once_with(
            "problem",
            dict(
                state=ASSESS, short_description="Test problem",
                assigned_to="123456"
            ),
            False,
        )

        assert result == (
            True,
            dict(
                state="assess",
                short_description="Test problem",
                assigned_to="123456",
                attachments=[],
                sys_id="123",
            ),
            dict(
                before=None,
                after=dict(
                    state="assess",
                    short_description="Test problem",
                    assigned_to="123456",
                    attachments=[],
                    sys_id="123",
                ),
            ),
        )

    @pytest.mark.parametrize(
        "mapped_param,param_value",
        [
            ("state", "my-new"),
            ("state", "my-assess"),
            ("state", "rca"),
            ("state", "fix"),
            ("state", "my-resolved"),
            ("state", "my-closed"),
            ("state", "absent"),

            ("problem_state", "my-new"),
            ("problem_state", "my-assess"),
            ("problem_state", "rca"),
            ("problem_state", "fix"),
            ("problem_state", "my-resolved"),
            ("problem_state", "my-closed"),

            ("urgency", "one"),
            ("urgency", "two"),
            ("urgency", "three"),

            ("impact", "111"),
            ("impact", "222"),
            ("impact", "333"),
        ]
    )
    def test_validate_mapping(self, create_module, mapped_param, param_value):
        all_mappings = dict(
            state=self.get_state_mapping(),
            problem_state=self.get_state_mapping(),
            urgency={
                "1": "one",
                "2": "two",
                "3": "three",
            },
            impact={
                "1": "111",
                "2": "222",
                "3": "333",
            },
        )
        problem_mapping = {mapped_param: all_mappings[mapped_param]}

        module_params = self.create_empty_module_params()
        module_params.update(problem_mapping=problem_mapping)
        module_params.update({mapped_param: param_value})

        module = create_module(params=module_params)

        mapper = get_mapper(module, "problem_mapping", PAYLOAD_FIELDS_MAPPING, implicit=True)

        problem.validate_mapping(module_params, mapper)

    @pytest.mark.parametrize(
        "mapped_param,param_value",
        [
            ("state", "explicitly-mapped-new"),
            ("state", "assess"),
            ("state", "root_cause_analysis"),
            ("state", "fix_in_progress"),
            ("state", "resolved"),
            ("state", "closed"),
            ("state", "absent"),

            ("problem_state", "new"),
            ("problem_state", "explicitly-mapped-assess"),
            ("problem_state", "root_cause_analysis"),
            ("problem_state", "fix_in_progress"),
            ("problem_state", "resolved"),
            ("problem_state", "closed"),

            ("urgency", "not_too_urgent"),
            ("urgency", "medium"),
            ("urgency", "high"),

            ("impact", "low"),
            ("impact", "medium"),
            ("impact", "highly_impacted"),
        ]
    )
    def test_validate_mapping_implicit(self, create_module, mapped_param, param_value):
        all_mappings = dict(
            state={NEW: "explicitly-mapped-new"},
            problem_state={ASSESS: "explicitly-mapped-assess"},
            urgency={
                "3": "not_too_urgent",
            },
            impact={
                "1": "highly_impacted",
            },
        )
        problem_mapping = {mapped_param: all_mappings[mapped_param]}

        module_params = self.create_empty_module_params()
        module_params.update(problem_mapping=problem_mapping)
        module_params.update({mapped_param: param_value})

        module = create_module(params=module_params)

        mapper = get_mapper(module, "problem_mapping", PAYLOAD_FIELDS_MAPPING, implicit=True)

        problem.validate_mapping(module_params, mapper)

    def test_no_change_mapped_problem_state_new(
        self, create_module, table_client, problem_client, attachment_client
    ):
        module_params = self.create_empty_module_params()
        module_params.update(
            dict(
                number="PRB0000001",
                state="my-new",
                short_description="Test problem",
                base_api_path="/api/path",
                urgency="lowest",
                impact="normal",
                problem_mapping=dict(
                    state=self.get_state_mapping(),
                    urgency={"3": "lowest"},
                    impact={"2": "normal"},
                ),
            )
        )
        module = create_module(params=module_params)

        table_client.get_record.return_value = dict(
            state=NEW,
            sys_id="123",
            urgency="3",
            impact="2",
            short_description="Test problem",
            number="PRB0000001",
        )

        attachment_client.list_records.return_value = []

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        table_client.get_record.assert_called_once_with(
            "problem",
            dict(number="PRB0000001"),
            must_exist=True,
        )

        expected = dict(
            state="my-new",
            number="PRB0000001",
            short_description="Test problem",
            urgency="lowest",
            impact="normal",
            attachments=[],
            sys_id="123",
        )

        assert result == (
            False,
            expected,
            dict(
                before=expected,
                after=expected,
            ),
        )

    def test_no_change_mapped_problem_state_assess(
        self, create_module, table_client, problem_client, attachment_client
    ):
        module_params = self.create_empty_module_params()
        module_params.update(
            dict(
                number="PRB0000001",
                state="my-assess",
                short_description="Test problem",
                base_api_path="/api/path",
                urgency="high",
                impact="high",
                problem_mapping=dict(
                    state=self.get_state_mapping(),
                    urgency={"3": "lowest"},
                    impact={"2": "normal"},
                ),
            )
        )
        module = create_module(params=module_params)

        table_client.get_record.return_value = dict(
            state=ASSESS,
            sys_id="123",
            urgency="1",
            impact="1",
            short_description="Test problem",
            number="PRB0000001",
        )

        attachment_client.list_records.return_value = []

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        table_client.get_record.assert_called_once_with(
            "problem",
            dict(number="PRB0000001"),
            must_exist=True,
        )

        expected = dict(
            state="my-assess",
            number="PRB0000001",
            short_description="Test problem",
            urgency="high",
            impact="high",
            attachments=[],
            sys_id="123",
        )

        assert result == (
            False,
            expected,
            dict(
                before=expected,
                after=expected,
            ),
        )

    def test_no_change_mapped_problem_state_rca(
        self, create_module, table_client, problem_client, attachment_client
    ):
        module_params = self.create_empty_module_params()
        module_params.update(
            dict(
                number="PRB0000001",
                state="rca",
                short_description="Test problem",
                base_api_path="/api/path",
                urgency="high",
                impact="normal",
                problem_mapping=dict(
                    state=self.get_state_mapping(),
                    urgency={"3": "lowest"},
                    impact={"2": "normal"},
                ),
            )
        )
        module = create_module(params=module_params)

        table_client.get_record.return_value = dict(
            state=RCA,
            sys_id="123",
            urgency="1",
            impact="2",
            short_description="Test problem",
            number="PRB0000001",
        )

        attachment_client.list_records.return_value = []

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        table_client.get_record.assert_called_once_with(
            "problem",
            dict(number="PRB0000001"),
            must_exist=True,
        )

        expected = dict(
            state="rca",
            number="PRB0000001",
            short_description="Test problem",
            urgency="high",
            impact="normal",
            attachments=[],
            sys_id="123",
        )

        assert result == (
            False,
            expected,
            dict(
                before=expected,
                after=expected,
            ),
        )

    def test_no_change_mapped_problem_state_fix(
        self, create_module, table_client, problem_client, attachment_client
    ):
        module_params = self.create_empty_module_params()
        module_params.update(
            dict(
                number="PRB0000001",
                state="fix",
                short_description="Test problem",
                base_api_path="/api/path",
                fix_notes="some fix notes",
                cause_notes="some cause notes",
                problem_mapping=dict(
                    state=self.get_state_mapping(),
                ),
            )
        )
        module = create_module(params=module_params)

        table_client.get_record.return_value = dict(
            state=FIX,
            sys_id="123",
            fix_notes="some fix notes",
            cause_notes="some cause notes",
            short_description="Test problem",
            number="PRB0000001",
        )

        attachment_client.list_records.return_value = []

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        table_client.get_record.assert_called_once_with(
            "problem",
            dict(number="PRB0000001"),
            must_exist=True,
        )

        expected = dict(
            state="fix",
            number="PRB0000001",
            short_description="Test problem",
            fix_notes="some fix notes",
            cause_notes="some cause notes",
            attachments=[],
            sys_id="123",
        )

        assert result == (
            False,
            expected,
            dict(
                before=expected,
                after=expected,
            ),
        )

    def test_no_change_mapped_problem_state_resolved(
        self, create_module, table_client, problem_client, attachment_client
    ):
        module_params = self.create_empty_module_params()
        module_params.update(
            dict(
                number="PRB0000001",
                state="my-resolved",
                short_description="Test problem",
                base_api_path="/api/path",
                fix_notes="some fix notes",
                cause_notes="some cause notes",
                resolution_code="fix_applied",
                problem_mapping=dict(
                    state=self.get_state_mapping(),
                ),
            )
        )
        module = create_module(params=module_params)

        table_client.get_record.return_value = dict(
            state=RESOLVED,
            sys_id="123",
            fix_notes="some fix notes",
            cause_notes="some cause notes",
            short_description="Test problem",
            number="PRB0000001",
            resolution_code="fix_applied",
        )

        attachment_client.list_records.return_value = []

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        table_client.get_record.assert_called_once_with(
            "problem",
            dict(number="PRB0000001"),
            must_exist=True,
        )

        expected = dict(
            state="my-resolved",
            number="PRB0000001",
            short_description="Test problem",
            fix_notes="some fix notes",
            cause_notes="some cause notes",
            resolution_code="fix_applied",
            attachments=[],
            sys_id="123",
        )

        assert result == (
            False,
            expected,
            dict(
                before=expected,
                after=expected,
            ),
        )

    def test_no_change_mapped_problem_state_closed(
        self, create_module, table_client, problem_client, attachment_client
    ):
        module_params = self.create_empty_module_params()
        module_params.update(
            dict(
                number="PRB0000001",
                state="my-closed",
                short_description="Test problem",
                base_api_path="/api/path",
                fix_notes="some fix notes",
                cause_notes="some cause notes",
                resolution_code="fix_applied",
                problem_mapping=dict(
                    state=self.get_state_mapping(),
                ),
            )
        )
        module = create_module(params=module_params)

        table_client.get_record.return_value = dict(
            state=CLOSED,
            sys_id="123",
            fix_notes="some fix notes",
            cause_notes="some cause notes",
            short_description="Test problem",
            number="PRB0000001",
            resolution_code="fix_applied",
        )

        attachment_client.list_records.return_value = []

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        table_client.get_record.assert_called_once_with(
            "problem",
            dict(number="PRB0000001"),
            must_exist=True,
        )

        expected = dict(
            state="my-closed",
            number="PRB0000001",
            short_description="Test problem",
            fix_notes="some fix notes",
            cause_notes="some cause notes",
            resolution_code="fix_applied",
            attachments=[],
            sys_id="123",
        )

        assert result == (
            False,
            expected,
            dict(
                before=expected,
                after=expected,
            ),
        )

    def test_updated_mapped_problem_state_new(
        self, create_module, table_client, problem_client, attachment_client
    ):
        module_params = self.create_empty_module_params()
        module_params.update(
            dict(
                number="PRB0000001",
                state="my-new",
                short_description="Test problem",
                base_api_path="/api/path",
                urgency="lowest",
                impact="normal",
                problem_mapping=dict(
                    state=self.get_state_mapping(),
                    urgency={"3": "lowest"},
                    impact={"2": "normal"},
                ),
            )
        )
        module = create_module(params=module_params)

        table_client.get_record.return_value = dict(
            state=NEW,
            sys_id="123",
            short_description="Test problem",
            number="PRB0000001",
        )

        table_client.update_record.return_value = dict(
            number="PRB0000001",
            state=NEW,
            short_description="Test problem",
            urgency="3",
            impact="2",
            sys_id="123",
        )

        attachment_client.list_records.return_value = []
        attachment_client.update_records.return_value = []

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        table_client.get_record.assert_called_once_with(
            "problem",
            dict(number="PRB0000001"),
            must_exist=True,
        )

        expected = dict(
            state="my-new",
            number="PRB0000001",
            short_description="Test problem",
            urgency="lowest",
            impact="normal",
            attachments=[],
            sys_id="123",
        )

        assert result == (
            True,
            expected,
            dict(
                before=dict(
                    state="my-new",
                    number="PRB0000001",
                    short_description="Test problem",
                    attachments=[],
                    sys_id="123",
                ),
                after=expected,
            ),
        )

    def test_updated_mapped_problem_state_assess(
        self, create_module, table_client, problem_client, attachment_client
    ):
        module_params = self.create_empty_module_params()
        module_params.update(
            dict(
                number="PRB0000001",
                state="my-assess",
                assigned_to="problem.manager",
                base_api_path="/api/path",
                problem_mapping=dict(
                    state=self.get_state_mapping(),
                ),
            )
        )
        module = create_module(params=module_params)

        table_client.get_record.side_effect = [
            dict(sys_id="abc123"),  # assigned_to
            dict(
                state=NEW,
                sys_id="123",
                short_description="Test problem",
                number="PRB0000001",
                assigned_to="",
            ),
        ]

        table_client.update_record.return_value = dict(
            number="PRB0000001",
            state=ASSESS,
            short_description="Test problem",
            assigned_to="abc123",
            sys_id="123",
        )

        attachment_client.list_records.return_value = []
        attachment_client.update_records.return_value = []

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        expected = dict(
            state="my-assess",
            number="PRB0000001",
            short_description="Test problem",
            assigned_to="abc123",
            attachments=[],
            sys_id="123",
        )

        assert result == (
            True,
            expected,
            dict(
                before=dict(
                    state="my-new",
                    number="PRB0000001",
                    short_description="Test problem",
                    attachments=[],
                    sys_id="123",
                    assigned_to="",
                ),
                after=expected,
            ),
        )

    def test_updated_mapped_problem_state_rca(
        self, create_module, table_client, problem_client, attachment_client
    ):
        module_params = self.create_empty_module_params()
        module_params.update(
            dict(
                number="PRB0000001",
                state="rca",
                base_api_path="/api/path",
                problem_mapping=dict(
                    state=self.get_state_mapping(),
                ),
            )
        )
        module = create_module(params=module_params)

        table_client.get_record.side_effect = [
            dict(
                state=ASSESS,
                sys_id="123",
                short_description="Test problem",
                number="PRB0000001",
                assigned_to="abc123",
            ),
        ]

        table_client.update_record.return_value = dict(
            number="PRB0000001",
            state=RCA,
            short_description="Test problem",
            assigned_to="abc123",
            sys_id="123",
        )

        attachment_client.list_records.return_value = []
        attachment_client.update_records.return_value = []

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        expected = dict(
            state="rca",
            number="PRB0000001",
            short_description="Test problem",
            assigned_to="abc123",
            attachments=[],
            sys_id="123",
        )

        assert result == (
            True,
            expected,
            dict(
                before=dict(
                    state="my-assess",
                    number="PRB0000001",
                    short_description="Test problem",
                    attachments=[],
                    sys_id="123",
                    assigned_to="abc123",
                ),
                after=expected,
            ),
        )

    def test_updated_mapped_problem_state_fix(
        self, create_module, table_client, problem_client, attachment_client
    ):
        module_params = self.create_empty_module_params()
        module_params.update(
            dict(
                number="PRB0000001",
                state="fix",
                fix_notes="some fix notes",
                cause_notes="some cause notes",
                base_api_path="/api/path",
                problem_mapping=dict(
                    state=self.get_state_mapping(),
                ),
            )
        )
        module = create_module(params=module_params)

        table_client.get_record.side_effect = [
            dict(
                state=RCA,
                sys_id="123",
                short_description="Test problem",
                number="PRB0000001",
                assigned_to="abc123",
                fix_notes="",
                cause_notes="",
            ),
        ]

        table_client.update_record.return_value = dict(
            number="PRB0000001",
            state=FIX,
            short_description="Test problem",
            assigned_to="abc123",
            sys_id="123",
            fix_notes="some fix notes",
            cause_notes="some cause notes",
        )

        attachment_client.list_records.return_value = []
        attachment_client.update_records.return_value = []

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        expected = dict(
            state="fix",
            number="PRB0000001",
            short_description="Test problem",
            assigned_to="abc123",
            attachments=[],
            sys_id="123",
            fix_notes="some fix notes",
            cause_notes="some cause notes",
        )

        assert result == (
            True,
            expected,
            dict(
                before=dict(
                    state="rca",
                    number="PRB0000001",
                    short_description="Test problem",
                    attachments=[],
                    sys_id="123",
                    assigned_to="abc123",
                    fix_notes="",
                    cause_notes="",
                ),
                after=expected,
            ),
        )

    def test_updated_mapped_problem_state_resolved(
        self, create_module, table_client, problem_client, attachment_client
    ):
        module_params = self.create_empty_module_params()
        module_params.update(
            dict(
                number="PRB0000001",
                state="my-resolved",
                resolution_code="fix_applied",
                base_api_path="/api/path",
                problem_mapping=dict(
                    state=self.get_state_mapping(),
                ),
            )
        )
        module = create_module(params=module_params)

        table_client.get_record.side_effect = [
            dict(
                state=FIX,
                sys_id="123",
                short_description="Test problem",
                number="PRB0000001",
                assigned_to="abc123",
                fix_notes="some fix notes",
                cause_notes="some cause notes",
                resolution_code="",
            ),
        ]

        table_client.update_record.return_value = dict(
            number="PRB0000001",
            state=RESOLVED,
            short_description="Test problem",
            assigned_to="abc123",
            sys_id="123",
            fix_notes="some fix notes",
            cause_notes="some cause notes",
            resolution_code="fix_applied",
        )

        attachment_client.list_records.return_value = []
        attachment_client.update_records.return_value = []

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        expected = dict(
            state="my-resolved",
            number="PRB0000001",
            short_description="Test problem",
            assigned_to="abc123",
            attachments=[],
            sys_id="123",
            fix_notes="some fix notes",
            cause_notes="some cause notes",
            resolution_code="fix_applied",
        )

        assert result == (
            True,
            expected,
            dict(
                before=dict(
                    state="fix",
                    number="PRB0000001",
                    short_description="Test problem",
                    attachments=[],
                    sys_id="123",
                    assigned_to="abc123",
                    fix_notes="some fix notes",
                    cause_notes="some cause notes",
                    resolution_code=""
                ),
                after=expected,
            ),
        )

    def test_updated_mapped_problem_state_closed(
        self, create_module, table_client, problem_client, attachment_client
    ):
        module_params = self.create_empty_module_params()
        module_params.update(
            dict(
                number="PRB0000001",
                state="my-closed",
                base_api_path="/api/path",
                problem_mapping=dict(
                    state=self.get_state_mapping(),
                ),
            )
        )
        module = create_module(params=module_params)

        table_client.get_record.side_effect = [
            dict(
                state=RESOLVED,
                sys_id="123",
                short_description="Test problem",
                number="PRB0000001",
                assigned_to="abc123",
                fix_notes="some fix notes",
                cause_notes="some cause notes",
                resolution_code="fix_applied",
            ),
        ]

        table_client.update_record.return_value = dict(
            number="PRB0000001",
            state=CLOSED,
            short_description="Test problem",
            assigned_to="abc123",
            sys_id="123",
            fix_notes="some fix notes",
            cause_notes="some cause notes",
            resolution_code="fix_applied",
        )

        attachment_client.list_records.return_value = []
        attachment_client.update_records.return_value = []

        result = problem.ensure_present(
            module, problem_client, table_client, attachment_client
        )

        expected = dict(
            state="my-closed",
            number="PRB0000001",
            short_description="Test problem",
            assigned_to="abc123",
            attachments=[],
            sys_id="123",
            fix_notes="some fix notes",
            cause_notes="some cause notes",
            resolution_code="fix_applied",
        )

        assert result == (
            True,
            expected,
            dict(
                before=dict(
                    state="my-resolved",
                    number="PRB0000001",
                    short_description="Test problem",
                    attachments=[],
                    sys_id="123",
                    assigned_to="abc123",
                    fix_notes="some fix notes",
                    cause_notes="some cause notes",
                    resolution_code="fix_applied",
                ),
                after=expected,
            ),
        )
