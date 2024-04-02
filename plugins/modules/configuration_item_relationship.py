#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Red Hat
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: configuration_item_relationship

author:
  - Cosmin Tupangiu (@tupyy)

short_description: Manage ServiceNow relationships between configuration items

description:
  - Create, update, delete ServiceNow relationships between configuration items.
  - For more information, refer to the ServiceNow configuration TODO

version_added: 2.5.0

extends_documentation_fragment:
  - servicenow.itsm.instance

seealso:
  - module: servicenow.itsm.configuration_item
  - module: servicenow.itsm.configuration_item_info

options:
  state:
    description:
      - State of the relationship.
    type: str
    choices: [ present, absent ]
    default: present
    required: true
  name:
    description:
      - The name of the relationship
      - Mutually exclusive with C(sys_id).
    type: str
  direction:
    description:
      - Direction of the relationship
    type: str
    choices: [ inbound, outbound ]
    default: outbound
    required: true
  sys_id:
    description:
      - The sys_id of the relationship
      - Mutually exclusive with C(name).
    type: str
  ci_sys_id:
    description:
      - The sys_id of the configuration item who own the relationship
    type: str
    required: true
  ci_classname:
    description:
      - Name of the configuration item class
    type: str
    required: true
  ci_target_ids:
    description:
      - List of id the configuration items associated with the relationships
      - Required if I(state) value is C(present).
    type: list
    elements: str
"""

EXAMPLES = r"""
- name: Create relationship between two ci
  servicenow.itsm.configuration_item_relationship:
    sys_id: "{{ relationship_sys_id }}"
    direction: outbound
    state: present
    ci_sys_id: "{{ owner_sys_id }}"
    ci_classname: cmbd_ci_linux_server
    ci_target_ids:
      - target1_id

- name: Remove relationship
  servicenow.itsm.configuration_item_relationship:
    sys_id: "{{ relationship_sys_id }}"
    direction: outbound
    state: absent
    ci_sys_id: "{{ owner_sys_id }}"
    ci_classname: cmbd_ci_linux_server

- name: Update relationship by adding one more target
    sys_id: "{{ relationship_sys_id }}"
    direction: outbound
    state: present
    ci_sys_id: "{{ owner_sys_id }}"
    ci_classname: cmbd_ci_linux_server
    ci_target_ids:
      - target1_id
      - new_target_id
"""

from ansible.module_utils.basic import AnsibleModule
from ..module_utils import arguments, client, errors, table, utils, generic
from ..module_utils import relation_client
from ..module_utils.configuration_item import PAYLOAD_FIELDS_MAPPING
from ..module_utils.utils import get_mapper

CMDB_INSTANCE_BASE_API_PATH = "/now/cmdb/instance"

DIRECT_PAYLOAD_FIELDS = (
    "direction",
    "state",
    "name",
    "ci_sys_id",
    "ci_target_ids",
)


def ensure_present(module, table_client, generic_client):
    mapper = get_mapper(
        module,
        "configuration_item_mapping",
        PAYLOAD_FIELDS_MAPPING,
        sysparm_display_value=module.params["sysparm_display_value"],
    )

    # Get the ci_classname from ci_record
    class_name = utils.filter_dict(
        mapper.to_ansible(table_client.get_by_sys_id("cmdb_ci", module.params["ci_sys_id"], True)),
        "sys_class_name"
    )

    ci = generic_client.get_by_sys_id(
        "/".join([CMDB_INSTANCE_BASE_API_PATH, class_name["sys_class_name"]]),
        module["ci_sys_id"],
        True
    )

    relation = relation_client.CmdbRelation(ci["outbound_relations"])

    return False, None, None


def run(module, table_client, generic_client):
    # if module.params["state"] == "absent":
    #     return ensure_absent(module, table_client, generic_client)
    return ensure_present(module, table_client, generic_client)


def main():
    module_args = dict(
        arguments.get_spec(
            "instance",
            "sys_id",
            "sysparm_display_value",
        ),
        state=dict(
            type="str",
            choices=[
                "present",
                "absent",
            ],
            default="present",
        ),
        name=dict(
            type="str",
        ),
        direction=dict(
            type="str",
            choices=[
                "inbound",
                "outbound",
            ],
            default="outbound",
        ),
        ci_sys_id=dict(
            type="str",
            required=True,
        ),
        ci_classname=dict(
            type="str",
            required=True,
        ),
        ci_target_ids=dict(
            type="list",
            elements="str"
        ),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ("state", "present", ("ci_target_ids",))
        ],
        mutually_exclusive=[("sys_id", "name")],
        required_one_of=[("sys_id", "name")],
    )

    try:
        snow_client = client.Client(**module.params["instance"])
        table_client = table.TableClient(snow_client)
        generic_client = generic.GenericClient(snow_client)
        changed, record, diff = run(module, table_client, generic_client)
        module.exit_json(changed=changed, record=record, diff=diff)
    except errors.ServiceNowError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
