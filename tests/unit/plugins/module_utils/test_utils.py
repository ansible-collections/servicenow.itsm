# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible_collections.servicenow.itsm.plugins.module_utils import utils

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestFilterDict:
    def test_no_field_names(self):
        assert {} == utils.filter_dict(dict(a=1))

    def test_ignoring_none_values(self):
        assert {} == utils.filter_dict(dict(a=None), "a")

    def test_selecting_a_subset_skip_none_values(self):
        assert dict(a=1, c="str") == utils.filter_dict(
            dict(a=1, b=2, c="str", d=None), "a", "c", "d"
        )
