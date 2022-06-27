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


@pytest.fixture
def missing_field(mocker):
    return "abc"


@pytest.fixture
def superset(mocker):
    return "abc"


@pytest.fixture
def candidate(mocker):
    return "abc"


@pytest.fixture
def record(mocker):
    return "abc"


@pytest.fixture
def params(mocker):
    return "abc"


class TestEnsureAbsent:
    def test_delete_change_request(self, create_module, table_client):
        pass

    def test_delete_change_request_not_present(self, create_module, table_client):
        pass


class TestValidateParams:

    def test_validate_params_missing_field(self, missing_field):
        pass

    def test_validate_params_missing_on_hold_field(self, missing_field):
        pass

    def test_validate_params(self):
        pass

    def test_validate_params_on_hold(self):
        pass


class TestEnsurePresent:
    def test_ensure_present_create_new(self, create_module, table_client):
        pass

    def test_ensure_present_nothing_to_do(self, create_module, table_client):
        pass

    def test_ensure_present_update(self, create_module, table_client):
        pass


class TestBuildPayload:
    def test_build_payload(self, create_module, table_client):
        pass

    def test_build_payload_with_other_option(self, create_module, table_client):
        pass


class TestSupersetWithDateCheck:

    def test_valid_superset(self, superset, candidate):
        pass

    def test_not_a_superset(self, superset, candidate):
        pass

    def test_same_point_in_time(self, record, params):
        pass

    def test_different_point_in_time(self, record, params):
        pass

    def test_empty_superset_dates(self, record, params):
        pass

    def test_empty_not_superset_dates(self, record, params):
        pass
