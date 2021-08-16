#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: configuration_item_batch

author:
  - Manca Bizjak (@mancabizjak)
  - Miha Dolinar (@mdolin)
  - Tadej Borovsak (@tadeboro)

short_description: Manage ServiceNow configuration items

description:
  - Create, delete or update a ServiceNow configuration item.
  - For more information, refer to the ServiceNow configuration management documentation at
    U(https://docs.servicenow.com/bundle/paris-servicenow-platform/page/product/configuration-management/reference/cmdb-table-property-descriptions.html).
version_added: 1.2.0
extends_documentation_fragment:
  - servicenow.itsm.instance

seealso:
  - module: servicenow.itsm.configuration_item
  - module: servicenow.itsm.configuration_item_info

options:
  sys_class_name:
    description:
      - Table name (configuration item type) that we would like to manipulate.
    required: true
    type: str
  id_column_set:
    description:
      - Columns that should be used to identify an existing record that we need to update.
    required: true
    type: list
    elements: str
  dataset:
    description:
      - List of dictionaries that will be used as a data source.
      - Each item in a list represents one CMDB item.
    required: true
    type: list
    elements: dict
  map:
    description:
      - Transformation instructions on how to convert input data to CMDB items.
      - Keys represent the CMDB item column names and the values are Jinja expressions
        that extract the value from the source data.
      - Data is returned as string because ServiceNow API expect this
    required: true
    type: dict
"""

EXAMPLES = r"""
- name: Update CMDB with some data
  servicenow.itsm.configuration_item_batch:
    sys_class_name: cmdb_ci_ec2_instance
    id_column_set: vm_inst_id
    dataset:
      - instance_id: 12345
        public_ip_address: 1.2.3.4
        tags:
          Name: my_name
      - instance_id: 54321
        public_ip_address: 4.3.2.1
        tags:
          Name: other_name
    map:
      vm_inst_id: instance_id
      ip_address: public_ip_adress
      name: tags.Name

- name: Identify CMDB item using combination of two columns
  servicenow.itsm.configuration_item_batch:
    sys_class_name: cmdb_ci_server
    id_column_set:
      - name
      - ip_address
    dataset: "{{ input_data }}"
    map:
      name: tags.Name
      ip_address: private_ip_address
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments, client, errors, table, utils


def update(module, table_client):
    changed = False
    cmdb_table = module.params["sys_class_name"]
    id_column_set = module.params["id_column_set"]

    for desired in module.params["dataset"]:
        query = dict((c, desired[c]) for c in id_column_set)
        current = table_client.get_record(cmdb_table, query)

        if not current:
            table_client.create_record(cmdb_table, desired, module.check_mode)
            changed = True
            continue

        if utils.is_superset(current, desired):
            continue

        table_client.update_record(cmdb_table, current, desired, module.check_mode)
        changed = True

    return changed


def main():
    module_args = dict(
        arguments.get_spec("instance"),
        sys_class_name=dict(
            type="str",
            required=True,
        ),
        id_column_set=dict(
            type="list",
            elements="str",
            required=True,
        ),
        dataset=dict(
            type="list",
            elements="dict",
            required=True,
        ),
        map=dict(
            type="dict",
            required=True,
        ),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    if not module.params["id_column_set"]:
        module.fail_json(msg="id_column_set should not be empty")

    try:
        snow_client = client.Client(**module.params["instance"])
        table_client = table.TableClient(snow_client)
        changed = update(module, table_client)
        module.exit_json(changed=changed)
    except errors.ServiceNowError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
