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


class TestMain:
    pass


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


class TestRun:
    pass
