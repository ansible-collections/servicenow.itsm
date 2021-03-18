# -*- coding: utf-8 -*-
# # Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys
import pytest


from ansible_collections.servicenow.itsm.plugins.modules import incident
from ansible_collections.servicenow.itsm.plugins.module_utils import errors


pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestEnsureAbsent:
    def test_delete_incident(self, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(host="my.host.name", username="user", password="pass"),
                state="absent",
                number="INC0000001",
                sys_id=None,
            )
        )
        table_client.get_record.return_value = dict(state="7", number="INC0000001")

        result = incident.ensure_absent(module, table_client)

        table_client.delete_record.assert_called_once()
        assert result == (
            True,
            None,
            dict(before=dict(state="closed", number="INC0000001"), after=None),
        )

    def test_delete_incident_not_present(self, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(host="my.host.name", username="user", password="pass"),
                state="absent",
                number=None,
                sys_id="1234",
            ),
        )
        table_client.get_record.return_value = None

        result = incident.ensure_absent(module, table_client)

        table_client.delete_record.assert_not_called()
        assert result == (False, None, dict(before=None, after=None))


class TestBuildPayload:
    def test_build_payload(self, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(host="my.host.name", username="user", password="pass"),
                state="new",
                number="",
                caller="admin",
                short_description="Test incident",
                description=None,
                impact="low",
                urgency="low",
                close_code=None,
                close_notes=None,
                hold_reason=None,
                other=None,
            ),
        )
        table_client.get_record.return_value = {
            "sys_id": "681ccaf9c0a8016400b98a06818d57c7"
        }

        result = incident.build_payload(module, table_client)

        assert result["caller_id"] == "681ccaf9c0a8016400b98a06818d57c7"
        assert result["state"] == "new"
        assert result["short_description"] == "Test incident"
        assert result["impact"] == "low"
        assert result["urgency"] == "low"
        assert "hold_reason" not in result

    def test_build_payload_with_other_option(self, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(host="my.host.name", username="user", password="pass"),
                state="new",
                number=None,
                caller=None,
                short_description="Test incident",
                description=None,
                impact="low",
                urgency="low",
                close_code=None,
                close_notes=None,
                hold_reason=None,
                other=dict(notify="1"),
            ),
        )

        result = incident.build_payload(module, table_client)

        assert result["state"] == "new"
        assert result["short_description"] == "Test incident"
        assert result["impact"] == "low"
        assert result["urgency"] == "low"
        assert "hold_reason" not in result
        assert result["notify"] == "1"


class TestValidateParams:
    VALID_PARAMS = dict(
        state="resolved", close_code="Solved (Permanently)", close_notes="Solved"
    )

    @pytest.mark.parametrize("missing_field", ["close_code", "close_notes"])
    def test_validate_params_missing_field(self, missing_field):
        params = self.VALID_PARAMS.copy()
        params[missing_field] = None

        with pytest.raises(errors.ServiceNowError, match=missing_field):
            incident.validate_params(params)

    def test_validate_params(self):
        incident.validate_params(self.VALID_PARAMS)


class TestEnsurePresent:
    def test_ensure_present_create_new(self, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(host="my.host.name", username="user", password="pass"),
                state="new",
                caller=None,
                short_description="Test incident",
                impact="low",
                urgency="low",
                number=None,
                sys_id=None,
                description=None,
                close_code=None,
                close_notes=None,
                hold_reason=None,
                other=None,
            ),
        )
        table_client.create_record.return_value = dict(
            state="1",
            number="INC0000001",
            short_description="Test incident",
            impact="3",
            urgency="3",
        )

        result = incident.ensure_present(module, table_client)

        table_client.create_record.assert_called_once()
        assert result == (
            True,
            dict(
                state="new",
                number="INC0000001",
                short_description="Test incident",
                impact="low",
                urgency="low",
            ),
            dict(
                before=None,
                after=dict(
                    state="new",
                    number="INC0000001",
                    short_description="Test incident",
                    impact="low",
                    urgency="low",
                ),
            ),
        )

    def test_ensure_present_nothing_to_do(self, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(host="my.host.name", username="user", password="pass"),
                state="new",
                number="INC0000001",
                caller=None,
                short_description="Test incident",
                impact=None,
                urgency=None,
                sys_id=None,
                description=None,
                close_code=None,
                close_notes=None,
                hold_reason=None,
                other=None,
            ),
        )
        table_client.get_record.return_value = dict(
            state="1", number="INC0000001", short_description="Test incident"
        )

        result = incident.ensure_present(module, table_client)

        table_client.get_record.assert_called_once()
        assert result == (
            False,
            dict(state="new", number="INC0000001", short_description="Test incident"),
            dict(
                before=dict(
                    state="new", number="INC0000001", short_description="Test incident"
                ),
                after=dict(
                    state="new", number="INC0000001", short_description="Test incident"
                ),
            ),
        )

    def test_ensure_present_update(self, mocker, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(host="my.host.name", username="user", password="pass"),
                state="in_progress",
                number="INC0000001",
                caller="admin",
                short_description="Test incident",
                impact=None,
                urgency=None,
                sys_id=None,
                description=None,
                close_code=None,
                close_notes=None,
                hold_reason=None,
                other=None,
            ),
        )
        payload_mocker = mocker.patch.object(incident, "build_payload")
        payload_mocker.return_value = dict(
            state="in_progress", number="INC0000001", short_description="Test incident"
        )
        table_client.get_record.return_value = dict(
            state="1", number="INC0000001", short_description="Test incident"
        )
        table_client.update_record.return_value = dict(
            state="2", number="INC0000001", short_description="Test incident"
        )

        result = incident.ensure_present(module, table_client)

        table_client.update_record.assert_called_once()
        assert result == (
            True,
            dict(
                state="in_progress",
                number="INC0000001",
                short_description="Test incident",
            ),
            dict(
                before=dict(
                    state="new", number="INC0000001", short_description="Test incident"
                ),
                after=dict(
                    state="in_progress",
                    number="INC0000001",
                    short_description="Test incident",
                ),
            ),
        )
