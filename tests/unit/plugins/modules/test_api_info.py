# -*- coding: utf-8 -*-
# # Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys
import pytest

from ansible_collections.servicenow.itsm.plugins.modules import api_info
from ansible_collections.servicenow.itsm.plugins.module_utils import errors

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestRemapCaller:
    def test_remap_params_direct(self, table_client):
        pass

    def test_remap_params_full(self, table_client):
        pass


class TestMain:
    def test_minimal_set_of_params(self, run_main):
        pass

    def test_all_params(self, run_main):
        pass

    def test_fail(self, run_main):
        pass


class TestRun:
    def test_run(self, create_module, table_client):
        pass
