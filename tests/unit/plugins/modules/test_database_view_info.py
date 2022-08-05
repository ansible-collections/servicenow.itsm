# -*- coding: utf-8 -*-
# # Copyright: (c) 2022, Toni Moreno <toni.moreno@gmali.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest
from ansible_collections.servicenow.itsm.plugins.modules import database_view_info

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestMain:
    def test_minimal_set_of_params(self, run_main):
        params = dict(
            instance=dict(
                host="https://my.host.name", username="user", password="pass"
            ),
            database_view="u_cmdb_ora_tns_service",
        )
        success, result = run_main(database_view_info, params)

        assert success is True

    def test_all_params(self, run_main):
        params = dict(
            instance=dict(
                host="https://my.host.name", username="user", password="pass"
            ),
            database_view="u_cmdb_ora_tns_service",
            return_fields=[
                "tns_name",
                "tns_sys_id",
                "tns_operational_status",
                "ms_name",
                "ms_sys_id",
            ],
        )
        success, result = run_main(database_view_info, params)

        assert success is True

    def test_fail(self, run_main):
        success, result = run_main(database_view_info)

        assert success is False


class TestRun:
    def test_run_full(self, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(
                    host="https://my.host.name", username="user", password="pass"
                ),
                database_view="u_cmdb_ora_tns_service",
                return_fields=[
                    "tns_name",
                    "tns_sys_id",
                    "tns_operational_status",
                    "ms_name",
                    "ms_sys_id",
                ],
            )
        )
        table_client.list_records.return_value = [
            dict(
                ms_name="MY_SERVICE1",
                ms_sys_id="msid1",
                tns_name="AAACDB2-PDB22-DB1",
                tns_operational_status=1,
                tns_sys_id="tnsid1",
            ),
            dict(
                ms_name="MY_SERVICE1",
                ms_sys_id="msid1",
                tns_name="AAACDB2-PDB11-DB2",
                tns_operational_status=1,
                tns_sys_id="tnsid2",
            ),
            dict(
                ms_name="MY_SERVICE1",
                ms_sys_id="msid1",
                tns_name="AAACDB2-PDB12-DB3",
                tns_operational_status=1,
                tns_sys_id="tnsid3",
            ),
            dict(
                ms_name="MY_SERVICE2",
                ms_sys_id="msid2",
                tns_name="AAACDB2-PDB22-DB1",
                tns_operational_status=1,
                tns_sys_id="tnsid1",
            ),
        ]

        records = database_view_info.run(module, table_client)

        table_client.list_records.assert_called_once_with(
            "u_cmdb_ora_tns_service",
            dict(
                sysparm_query="",
                sysparm_fields="tns_name,tns_sys_id,tns_operational_status,ms_name,ms_sys_id",
            ),
        )

        assert records == [
            dict(
                ms_name="MY_SERVICE1",
                ms_sys_id="msid1",
                tns_name="AAACDB2-PDB22-DB1",
                tns_operational_status=1,
                tns_sys_id="tnsid1",
            ),
            dict(
                ms_name="MY_SERVICE1",
                ms_sys_id="msid1",
                tns_name="AAACDB2-PDB11-DB2",
                tns_operational_status=1,
                tns_sys_id="tnsid2",
            ),
            dict(
                ms_name="MY_SERVICE1",
                ms_sys_id="msid1",
                tns_name="AAACDB2-PDB12-DB3",
                tns_operational_status=1,
                tns_sys_id="tnsid3",
            ),
            dict(
                ms_name="MY_SERVICE2",
                ms_sys_id="msid2",
                tns_name="AAACDB2-PDB22-DB1",
                tns_operational_status=1,
                tns_sys_id="tnsid1",
            ),
        ]

    def test_run_filtered(self, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(
                    host="https://my.host.name", username="user", password="pass"
                ),
                database_view="u_cmdb_ora_tns_service",
                return_fields=[
                    "tns_name",
                    "tns_sys_id",
                    "tns_operational_status",
                    "ms_name",
                    "ms_sys_id",
                ],
                query=[dict(ms_name="= MY_SERVICE2")],
            )
        )
        table_client.list_records.return_value = [
            dict(
                ms_name="MY_SERVICE2",
                ms_sys_id="msid2",
                tns_name="AAACDB2-PDB22-DB1",
                tns_operational_status=1,
                tns_sys_id="tnsid1",
            ),
        ]

        records = database_view_info.run(module, table_client)

        table_client.list_records.assert_called_once_with(
            "u_cmdb_ora_tns_service",
            dict(
                sysparm_query="ms_name=MY_SERVICE2",
                sysparm_fields="tns_name,tns_sys_id,tns_operational_status,ms_name,ms_sys_id",
            ),
        )

        assert records == [
            dict(
                ms_name="MY_SERVICE2",
                ms_sys_id="msid2",
                tns_name="AAACDB2-PDB22-DB1",
                tns_operational_status=1,
                tns_sys_id="tnsid1",
            ),
        ]
