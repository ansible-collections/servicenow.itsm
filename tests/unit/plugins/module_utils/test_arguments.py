# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible_collections.servicenow.itsm.plugins.module_utils import arguments

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestGetSpec:
    def test_get_params_valid_parameter(self):
        result = arguments.get_spec("instance")

        assert result == dict(
            instance=dict(
                type="dict",
                apply_defaults=True,
                options=dict(
                    host=dict(
                        type="str",
                        required=True,
                    ),
                    username=dict(
                        type="str",
                        required=True,
                    ),
                    password=dict(
                        type="str",
                        required=True,
                        no_log=True,
                    ),
                    client_id=dict(
                        type="str",
                    ),
                    client_secret=dict(
                        type="str",
                        no_log=True,
                    ),
                ),
                required_together=[("client_id", "client_secret")],
            ),
        )

    def test_get_params_no_parameter(self):
        result = arguments.get_spec()

        assert result == dict()
