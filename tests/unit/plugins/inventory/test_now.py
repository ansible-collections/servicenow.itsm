# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible_collections.servicenow.itsm.plugins.inventory import now

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestSysparmQueryFromConditions:
    def test_empty_conditions(self):
        assert now.sysparm_query_from_conditions({}) is None

    @pytest.mark.parametrize(
        "conditions,expected",
        [
            (dict(a=dict(includes=["b"])), "a=b"),
            (dict(a=dict(includes=["b", "c"])), "a=b^ORa=c"),
            (dict(a=dict(excludes=["b"])), "a!=b"),
            (dict(a=dict(excludes=["b", "c"])), "a!=b^a!=c"),
        ],
    )
    def test_conditions_single_field(self, conditions, expected):
        assert expected == now.sysparm_query_from_conditions(conditions)

    def test_conditions_multiple_fields(self):
        conditions = dict(
            a=dict(includes=["a1", "a2"]),
            b=dict(excludes=["b1", "b2"]),
        )
        sysparm_query = now.sysparm_query_from_conditions(conditions)

        # We do not care about the order, we just want to make sure
        # that there is "and" between conditions for both fields.
        assert sysparm_query in ("a=a1^ORa=a2^b!=b1^b!=b2", "b!=b1^b!=b2^a=a1^ORa=a2")
