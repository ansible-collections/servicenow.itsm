# -*- coding: utf-8 -*-
# # Copyright: (c) 2021, Toni Moreno <toni.moreno@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest
from ansible_collections.servicenow.itsm.plugins.modules import cmdb_relationship

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestMain:
    def test_minimal_set_of_params(self, run_main):
        params = dict(
            instance=dict(
                host="https://my.host.name", username="user", password="pass"
            ),
            relationship_name="Depends on::Used by",
            relationship_type="ci_downstream",
            parent_ci_name="MI_SERVICE",
            parent_ci_class_name="cmdb_ci_service_discovered",
            child_ci_name_list=["MY_APP1", "MY_APP2"],
            child_ci_class_name="cmdb_ci_appl",
        )
        success, result = run_main(cmdb_relationship, params)

        assert success is True

    def test_all_params(self, run_main):
        params = dict(
            instance=dict(
                host="https://my.host.name", username="user", password="pass"
            ),
            state="present",
            relationship_name="Depends on::Used by",
            relationship_type="ci_downstream",
            parent_ci_name="MI_SERVICE",
            parent_ci_class_name="cmdb_ci_service_discovered",
            child_ci_name_list=["MY_APP1", "MY_APP2"],
            child_ci_class_name="cmdb_ci_appl",
        )

        success, result = run_main(cmdb_relationship, params)
        assert success is True

    def test_fail(self, run_main):
        success, result = run_main(cmdb_relationship)

        assert success is False


class TestRun:
    def test_run_absent(self, mocker, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(
                    host="https://my.host.name", username="user", password="pass"
                ),
                state="absent",
                relationship_name="Depends on::Used by",
                relationship_type="ci_downstream",
                parent_ci_name="MI_SERVICE",
                parent_ci_class_name="cmdb_ci_service_discovered",
                child_ci_name_list=["MY_APP1", "MY_APP2"],
                child_ci_class_name="cmdb_ci_appl",
            ),
        )
        mocker.patch(
            "ansible_collections.servicenow.itsm.plugins.modules.cmdb_relationship.get_relationship_name_id"
        ).return_value = "got_relationship_id"

        mocker.patch(
            "ansible_collections.servicenow.itsm.plugins.modules.cmdb_relationship.get_parent_sys_id"
        ).return_value = "got_parent_sys_id"

        mocker.patch(
            "ansible_collections.servicenow.itsm.plugins.modules.cmdb_relationship.check_relationship_exist"
        ).return_value = (True, "idX")

        mocker.patch(
            "ansible_collections.servicenow.itsm.plugins.modules.cmdb_relationship.ensure_absent"
        ).return_value = (False, "Ok relations removed successfully")

        snow_client = ""

        table_client.list_records.return_value = [
            {"name": "MY_APP1", "sys_id": "id1"},
            {"name": "MY_APP1", "sys_id": "id2"},
        ]

        changed, failed, detailed_info = cmdb_relationship.run(
            module, snow_client, table_client
        )
        print(detailed_info)
        assert changed is True
        assert failed is False
        assert detailed_info == {
            "msg": "Ok relations removed successfully",
            "relations_requested_changes": 2,
            "relations_changed_detail": [
                {
                    "parent": "MI_SERVICE",
                    "type_id": "got_relationship_id",
                    "parent_id": "got_parent_sys_id",
                    "sys_id": "idX",
                    "child": "MY_APP1",
                    "child_id": "id1",
                    "type": "Depends on::Used by",
                    "relationshipType": "ci_downstream",
                },
                {
                    "parent": "MI_SERVICE",
                    "type_id": "got_relationship_id",
                    "parent_id": "got_parent_sys_id",
                    "sys_id": "idX",
                    "child": "MY_APP1",
                    "child_id": "id2",
                    "type": "Depends on::Used by",
                    "relationshipType": "ci_downstream",
                },
            ],
            "relations_deleted": 2,
            "relations_created": 0,
        }

    def test_run_present(self, mocker, create_module, table_client):
        module = create_module(
            params=dict(
                instance=dict(
                    host="https://my.host.name", username="user", password="pass"
                ),
                state="present",
                relationship_name="Depends on::Used by",
                relationship_type="ci_downstream",
                parent_ci_name="MI_SERVICE",
                parent_ci_class_name="cmdb_ci_service_discovered",
                child_ci_name_list=["MY_APP1", "MY_APP2"],
                child_ci_class_name="cmdb_ci_appl",
            ),
        )
        mocker.patch(
            "ansible_collections.servicenow.itsm.plugins.modules.cmdb_relationship.get_relationship_name_id"
        ).return_value = "got_relationship_id"

        mocker.patch(
            "ansible_collections.servicenow.itsm.plugins.modules.cmdb_relationship.get_parent_sys_id"
        ).return_value = "got_parent_sys_id"

        mocker.patch(
            "ansible_collections.servicenow.itsm.plugins.modules.cmdb_relationship.check_relationship_exist"
        ).return_value = (False, "")

        mocker.patch(
            "ansible_collections.servicenow.itsm.plugins.modules.cmdb_relationship.ensure_present"
        ).return_value = (False, "Ok relations created successfully")

        snow_client = ""

        table_client.list_records.return_value = [
            {"name": "MY_APP1", "sys_id": "id1"},
            {"name": "MY_APP1", "sys_id": "id2"},
        ]

        changed, failed, detailed_info = cmdb_relationship.run(
            module, snow_client, table_client
        )
        assert changed is True
        assert failed is False
        assert detailed_info == {
            "msg": "Ok relations created successfully",
            "relations_requested_changes": 2,
            "relations_changed_detail": [
                {
                    "parent": "MI_SERVICE",
                    "type_id": "got_relationship_id",
                    "parent_id": "got_parent_sys_id",
                    "sys_id": "",
                    "child": "MY_APP1",
                    "child_id": "id1",
                    "type": "Depends on::Used by",
                    "relationshipType": "ci_downstream",
                },
                {
                    "parent": "MI_SERVICE",
                    "type_id": "got_relationship_id",
                    "parent_id": "got_parent_sys_id",
                    "sys_id": "",
                    "child": "MY_APP1",
                    "child_id": "id2",
                    "type": "Depends on::Used by",
                    "relationshipType": "ci_downstream",
                },
            ],
            "relations_deleted": 0,
            "relations_created": 2,
        }
