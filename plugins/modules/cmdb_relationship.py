#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Toni Moreno <toni.moreno@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: cmdb_relationship

author:
  - Toni Moreno (@toni-moreno)

short_description: a module that users can use to create or delete relationships between two or more CMDB records

description:
  - create relationship between two CMDB records
version_added: 2.0.0
extends_documentation_fragment:
  - servicenow.itsm.instance

options:
  state:
    description:
      - State of the configuration item.
    type: str
    choices: [ present, absent ]
    default: present
  relationship_name:
    description:
      - The name of the relationship as described in the CMDB cmdb_rel_type table.
    type: str
    required: true
  relationship_type:
    description:
      - The type of the relationship.
    type: str
    choices: [ ci_downstream, ci_upstream ]
    required: true
  parent_ci_name:
    description: The name of the parent CI.
    type: str
    required: true
  parent_ci_class_name:
    description: The class name of the parent CI.
    type: str
    required: true
  child_ci_name_list:
    description: a list of child CI names from the same class.
    type: list
    elements: str
    required: true
  child_ci_class_name:
    description: the class name of the child CI list.
    type: str
    required: true

notes:
  - Supports check_mode.
"""

EXAMPLES = r"""
  - name: ServiceNow create relationship between two or more CMDB records
    servicenow.itsm.cmdb_relationship:
      state: present
      instance:
        host: https://instance_id.service-now.com
        username: user
        password: pass
      relationship_name: Depends on::Used by
      relationship_type: ci_downstream
      parent_ci_name: MI_SERVICE
      parent_ci_class_name: cmdb_ci_service_discovered
      child_ci_name_list:
          - MY_APP1
          - MY_APP2
          - MY_APP3
      child_ci_class_name: cmdb_ci_appl
"""


RETURN = r"""
record:
  description: A dictionary containing the creation/deletion information
  returned: success
  type: dict
  contains:
    relations_requested_changes:
        description: number of requested relations to create
        returned: always
        type: int
        sample: OK
    relations_created:
        description: number of finally created relations (could be less than requested if already existing)
        returned: success
        type: int
        sample: 2
    relations_deleted:
        description: number of finally deleted relations (could be less than requested if some of them doesn't exist)
        returned: success
        type: int
        sample: 2
    relations_changed_details:
        description: array with detailed information about each created relations
        returned: success
        type: list
        elements: dict
        sample:
            - child: MY_APP2
              child_id: c3833a6c07241110befff6fd7c1ed0bb
              parent: MY_SERVICE
              parent_id: 762ed2a807e01110befff6fd7c1ed0bf
              relationshipType: ci_downstream
              sys_id: ""
              type: Depends on::Used by
              type_id: 1a9cb166f1571100a92eb60da2bce5c5
    relations_delete_api_result:
        description: return message from "add-rel" API call
        returned: success
        type: dict
        sample:
            - message: Delete relationship successfully."
            - status: OK
    relations_create_api_result:
        description: return message from "delete-rel" API call
        returned: success
        type: dict
        sample:
            - message: Delete relationship successfully."
            - status: OK
"""

import json

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments, client, errors, table

# Array of structures of data got from /api/now/cmdbrelation/types
# [{
#   "child_descriptor": "Powered by",
#   "sys_id": "55ba4972c0a8010e01c5feb5ca39c04c",
#   "end_point": "false",
#   "name": "Powers::Powered by",
#   "table_name": "cmdb_rel_type",
#   "parent_descriptor": "Powers"
# }]


def get_relationship_name_id(client, relationship_name):
    relationship_id = None
    result = client.get("/api/now/cmdbrelation/types").json["result"]
    types = result["types"]
    json_types = json.loads(types)
    for rel in json_types:
        name = rel["name"]
        if name == relationship_name:
            return rel["sys_id"]
    return relationship_id


# {
#   "item": "[{\"type\":
#             \"Depends on::Used by\",
#             \"type_id\":\"1a9cb166f1571100a92eb60da2bce5c5\",
#             \"child\":\"MI_SERVICE\",
#             \"child_id\":\"889e52e807e01110befff6fd7c1ed036\",
#             \"parent\":\"MY_APP1\",
#             \"parent_id\":\"6a29040107a01110befff6fd7c1ed070\",
#             \"sys_id\":\"\",
#             \"relationshipType\":\"ci_downstream\"}]",
#   "type": "cmdb_ci",
#   "isSuggestedRelationship": true
# }


def create_relationship(client, all_relationships):
    payload = dict(
        {
            "item": json.dumps(all_relationships),
            "type": "cmdb_ci",
            "isSuggestedRelationship": True,
        }
    )
    return client.post(
        "/api/now/cmdbrelation/add-rels", payload, query=table._query()
    ).json["result"]


def delete_relationship(client, all_relationships):
    sys_ids = []
    for rel in all_relationships:
        sys_ids.append(rel["sys_id"])
    q = dict({"sysIds": ",".join(sys_ids), "type": "cmdb_ci"})
    return client.delete("/api/now/cmdbrelation/delete-rels", query=q).json["result"]


def check_relationship_exist(client, relationship):
    query = (
        "child="
        + relationship["child_id"]
        + "^parent="
        + relationship["parent_id"]
        + "^type="
        + relationship["type_id"]
    )
    children = client.list_records(
        "cmdb_rel_ci",
        dict({"sysparm_query": query, "sysparm_fields": "parent,child,type,sys_id"}),
    )

    if len(children) == 1:
        # Relationship already exist
        return True, children[0]["sys_id"]
    elif len(children) == 0:
        # Relationship does not exist
        return False, ""
    else:
        # len > 1 (not posible!)
        raise errors.ServiceNowError("Error, cmdb_rel_ci query TOO MANY ROWS")


def ensure_absent(result, snow_client, relations):
    out = delete_relationship(snow_client, relations)
    res = json.loads(out["message"])
    # print(res)
    result["relations_delete_api_result"] = res
    if res["status"] != "OK":
        result["failed"] = True
        result["msg"] = "Error removing relationship: {0}".format(res["message"])
    else:
        result["relations_deleted"] = len(relations)
        result["msg"] = res["message"]


def ensure_present(result, snow_client, relations):
    out = create_relationship(snow_client, relations)
    res = json.loads(out["message"])
    # print(res)
    result["relations_create_api_result"] = res
    if res["status"] != "OK":
        result["failed"] = True
        result["msg"] = "Error creating relationship: {0}".format(res["message"])
    else:
        result["relations_created"] = len(relations)
        result["msg"] = res["message"]


def run(module, snow_client, table_client):

    parent_ci_name = module.params["parent_ci_name"]
    parent_ci_class_name = module.params["parent_ci_class_name"]
    child_ci_name_list = module.params["child_ci_name_list"]
    child_ci_class_name = module.params["child_ci_class_name"]
    relationship_name = module.params["relationship_name"]
    relationship_type = module.params["relationship_type"]
    state = module.params["state"]

    result = dict(
        changed=False,
        relations_requested_changes=len(child_ci_name_list),
        relations_created=0,
        relations_deleted=0,
    )

    # Get relationship type id

    id = get_relationship_name_id(snow_client, relationship_name)
    if not id:
        raise Exception("Error getting relationship id: {0}".format(relationship_name))

    # Get parent sys_id

    parent = table_client.list_records(
        parent_ci_class_name,
        dict({"name": parent_ci_name, "sysparm_fields": "name,sys_id"}),
    )
    if len(parent) != 1:
        raise Exception(
            "Error getting parent id: got {0} resuts:  for CI {1}".format(
                len(parent), parent_ci_name
            )
        )
    parent_sys_id = parent[0]["sys_id"]

    # Get children sys_id's

    query = ""
    for child_ci_name in child_ci_name_list:
        if child_ci_name == child_ci_name_list[-1]:
            query += "name={0}".format(child_ci_name)
        else:
            query += "name={0}^OR".format(child_ci_name)
    children = table_client.list_records(
        child_ci_class_name,
        dict({"sysparm_query": query, "sysparm_fields": "name,sys_id"}),
    )

    # generate relation array to send to API
    relations = []
    for child in children:
        relation = dict(
            {
                "type": relationship_name,
                "type_id": id,
                "child": child["name"],
                "child_id": child["sys_id"],
                "parent": parent_ci_name,
                "parent_id": parent_sys_id,
                "sys_id": "",
                "relationshipType": relationship_type,
            }
        )
        exist, relation["sys_id"] = check_relationship_exist(table_client, relation)
        if state == "present":
            # check if relationship already exists when present
            if not exist:
                relations.append(relation)
        else:
            # check if relationship already exists when absent
            if exist:
                relations.append(relation)
    result["relations_changed_detail"] = relations

    if len(relations) > 0:
        result["changed"] = True
        if not module.check_mode:
            if state == "present":
                ensure_present(result, snow_client, relations)
            else:  # absent
                ensure_absent(result, snow_client, relations)
    else:
        if state == "present":
            result["msg"] = "No new relationship to create"
        else:
            result["msg"] = "No relationship to delete"

    return result


def main():
    module_args = dict(
        arguments.get_spec("instance"),
        state=dict(type="str", default="present", choices=["present", "absent"]),
        parent_ci_name=dict(type="str", required=True),
        parent_ci_class_name=dict(type="str", required=True),
        child_ci_name_list=dict(type="list", elements="str", required=True),
        child_ci_class_name=dict(type="str", required=True),
        relationship_name=dict(type="str", required=True),
        relationship_type=dict(
            type="str",
            choices=[
                "ci_downstream",
                "ci_upstream",
            ],
            required=True,
        ),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    try:
        snow_client = client.Client(**module.params["instance"])
        table_client = table.TableClient(snow_client)
        result = run(module, snow_client, table_client)
        module.exit_json(**result)
    except errors.ServiceNowError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
