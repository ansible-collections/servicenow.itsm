# -*- coding: utf-8 -*-
# # Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible_collections.servicenow.itsm.plugins.modules import incident_info

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestMain:
    def test_minimal_set_of_params(self, run_main):
        params = dict(
            instance=dict(host="my.host.name", username="user", password="pass"),
        )
        success, result = run_main(incident_info, params)

        assert success is True

    def test_all_params(self, run_main):
        params = dict(
            instance=dict(host="my.host.name", username="user", password="pass"),
            sys_id="id",
            number="INC001",
        )
        success, result = run_main(incident_info, params)

        assert success is True

    def test_fail(self, run_main):
        success, result = run_main(incident_info)

        assert success is False
        assert "instance" in result["msg"]


class TestRun:
    def test_run(self, create_module, mocker):
        module = create_module(
            params=dict(
                instance=dict(host="my.host.name", username="user", password="pass"),
                sys_id=None,
                number="INC001",
            )
        )
        client_mock = mocker.patch.object(incident_info.client, "Client").return_value
        client_mock.get.return_value.json = {"result": [1, 2, 3]}

        records = incident_info.run(module)

        client_mock.get.assert_called_once_with(
            "table/incident", query=dict(number="INC001")
        )
        assert records == [1, 2, 3]
