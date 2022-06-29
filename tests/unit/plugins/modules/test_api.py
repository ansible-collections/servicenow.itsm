# -*- coding: utf-8 -*-
# # Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys
import pytest

from ansible_collections.servicenow.itsm.plugins.modules import api
from ansible_collections.servicenow.itsm.plugins.module_utils import errors

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestUpdateResource:

    def test_update_resource_not_present(self, create_module, table_client):
        pass

    def test_present_resource_present(self, create_module, table_client):
        pass


class TestCreateResource:

    def test_create_resource(self):
        pass


class TestDeleteResource:

    def test_delete_resource_not_present(self):
        pass

    def test_delete_resource_present(self):
        pass
