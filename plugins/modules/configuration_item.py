#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: configuration_item

author:
  - Manca Bizjak (@mancabizjak)
  - Miha Dolinar (@mdolin)
  - Tadej Borovsak (@tadeboro)

short_description: Manage ServiceNow configuration items

description:
  - Create, delete or update a ServiceNow configuration item.
  - For more information, refer to the ServiceNow configuration management documentation at
    U(https://docs.servicenow.com/bundle/paris-servicenow-platform/page/product/configuration-management/reference/cmdb-table-property-descriptions.html).
version_added: 1.0.0
extends_documentation_fragment:
  - servicenow.itsm.instance
  - servicenow.itsm.sys_id

seealso:
  - module: servicenow.itsm.configuration_item_info

options:
  state:
    description:
      - State of the configuration item.
    type: str
    choices: [ present, absent ]
    default: present
  name:
    description:
      - The name of the configuration item.
      - Required if the configuration item does not yet exist.
    type: str
  short_description:
    description:
      - Short description of the configuration item.
    type: str
  sys_class_name:
    description:
      - ServiceNow configuration item class.
      - The value of this parameter should point to a ServiceNow CMDB configuration
        item table, for instance C(cmdb_ci_server).
      - For a list of valid CMDB tables, refer to ServiceNow documentation on
        U(https://docs.servicenow.com/bundle/paris-servicenow-platform/page/product/configuration-management/reference/cmdb-tables-details.html).
      - If this parameter is unset when a new configuration item needs to be created,
        the default value C(cmdb_ci) will be used.
    type: str
  asset_tag:
    description:
      - Asset tag of the asset logically related to this configuration item.
      - Read more about the relationship between configuration items and assets at
        U(https://docs.servicenow.com/bundle/paris-it-asset-management/page/product/asset-management/concept/c_ManagingAssets.html).
    type: str
  install_status:
    description:
      - The functional status of the configuration item.
    type: str
    choices: [ implementing, installed, on_order, in_maintenance, pending_install, pending_repair,
      in_stock, retired, stolen, absent ]
  operational_status:
    description:
      - The operational status of the configuration item.
    type: str
    choices: [ operational, non_operational, repair_in_progress, dr_standby, ready, retired,
      pipeline, catalog ]
  serial_number:
    description:
      - Serial number of the configuration item.
    type: str
  ip_address:
    description:
      - Primary IP address used by the configuration item.
    type: str
  mac_address:
    description:
      - MAC address of the configuration item.
    type: str
  category:
    description:
      - Category of the configuration item, for instance C(Hardware).
    type: str
  environment:
    description:
      - The environment to which this configuration item belongs.
    choices: [ development, production, test ]
    type: str
  assigned_to:
    description:
      - A person to whom this configuration item is assigned to.
      - Expected value for I(assigned_to) is user id (usually in the form of
        C(first_name.last_name)).
    type: str
  other:
    description:
      - Any of the remaining configuration parameters.
      - For the attributes of the base C(cmdb_ci) table, refer to the ServiceNow documentation on
        U(https://docs.servicenow.com/bundle/paris-servicenow-platform/page/product/configuration-management/reference/cmdb-table-property-descriptions.html).
      - For the attributes of configuration items specific to I(sys_class_name),
        please consult the relevant ServiceNow documentation.
    type: dict
"""

EXAMPLES = r"""
- name: Create a configuration item
  servicenow.itsm.configuration_item:
    name: HPE ProLiant BL465C G7
    short_description: HPE ProLiant Server G7
    serial_number: ECE-164-E10834-NO
    asset_tag: P1000613
    sys_class_name: cmdb_ci_server
    assigned_to: some.user
    environment: production
    category: Hardware
    other:
      model_number: BL465C G7
  register: server

- name: Update a configuration item
  servicenow.itsm.configuration_item:
    sys_id: "{{ server.record.sys_id }}"
    install_status: in_maintenance
    operational_status: repair_in_progress
    other:
      fault_count: 1
      classification: Development

- name: Delete a configuration item
  servicenow.itsm.configuration_item:
    sys_id: "{{ server.record.sys_id }}"
    state: absent
"""

RETURN = r"""
record:
  description:
    - The configuration item record.
    - Note that the fields of the returned record depend on the configuration
      item's I(sys_class_name).
  returned: success
  type: dict
  sample:
    "asset": "05a9ec0d3790200044e0bfc8bcbe5dc2"
    "asset_tag": "P1000440"
    "assigned": "2019-02-28 08:00:00"
    "assigned_to": "8a826bf03710200044e0bfc8bcbe5d96"
    "assignment_group": ""
    "attestation_score": ""
    "attested": "false"
    "attested_by": ""
    "attested_date": ""
    "attributes": ""
    "can_print": "false"
    "category": "Hardware"
    "change_control": ""
    "checked_in": ""
    "checked_out": ""
    "comments": ""
    "company": "81fca4cbac1d55eb355b4b6db0e3c80f"
    "correlation_id": ""
    "cost": "1699.99"
    "cost_cc": "USD"
    "cost_center": "d9d01546c0a80a6403e18b82250c80a1"
    "delivery_date": "2018-07-05 07:00:00"
    "department": "a581ab703710200044e0bfc8bcbe5de8"
    "discovery_source": ""
    "dns_domain": ""
    "due": ""
    "due_in": ""
    "duplicate_of": ""
    "environment": ""
    "fault_count": "0"
    "first_discovered": ""
    "fqdn": ""
    "gl_account": ""
    "install_date": "2018-10-02 07:00:00"
    "install_status": "installed"
    "invoice_number": ""
    "ip_address": ""
    "justification": ""
    "last_discovered": ""
    "lease_id": ""
    "life_cycle_stage": ""
    "life_cycle_stage_status": ""
    "location": "8228cda2ac1d55eb7029baf443945c37"
    "mac_address": ""
    "maintenance_schedule": ""
    "managed_by": ""
    "managed_by_group": ""
    "manufacturer": "aa0a6df8c611227601cd2ed45989e0ac"
    "model_id": "0c43b858c611227501522de20c61ac75"
    "model_number": ""
    "monitor": "false"
    "name": "ThinkStation S20"
    "operational_status": "operational"
    "order_date": "2018-06-07 07:00:00"
    "owned_by": ""
    "po_number": "PO100005"
    "purchase_date": "2018-06-22"
    "schedule": ""
    "serial_number": "WCL-206-Q10853-BF"
    "short_description": ""
    "skip_sync": "false"
    "start_date": ""
    "subcategory": "Computer"
    "support_group": ""
    "supported_by": ""
    "sys_class_name": "cmdb_ci_computer"
    "sys_class_path": "/!!/!2/!("
    "sys_created_by": "admin"
    "sys_created_on": "2012-02-18 08:14:42"
    "sys_domain": "global"
    "sys_domain_path": "/"
    "sys_id": "01a9ec0d3790200044e0bfc8bcbe5dc3"
    "sys_mod_count": "6"
    "sys_tags": ""
    "sys_updated_by": "system"
    "sys_updated_on": "2021-01-16 05:50:31"
    "unverified": "false"
    "vendor": "aa0a6df8c611227601cd2ed45989e0ac"
    "warranty_expiration": "2021-10-01"
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments, client, errors, table, utils
from ..module_utils.configuration_item import PAYLOAD_FIELDS_MAPPING

DIRECT_PAYLOAD_FIELDS = (
    "name",
    "short_description",
    "sys_class_name",
    "asset_tag",
    "install_status",
    "operational_status",
    "serial_number",
    "ip_address",
    "mac_address",
    "category",
    "environment",
)


def ensure_absent(module, table_client):
    mapper = utils.PayloadMapper(PAYLOAD_FIELDS_MAPPING, module.warn)
    query = utils.filter_dict(module.params, "sys_id")
    configuration_item = table_client.get_record("cmdb_ci", query)

    if configuration_item:
        cmdb_table = configuration_item["sys_class_name"]
        if cmdb_table != "cmdb_ci":
            configuration_item = table_client.get_record(cmdb_table, query)
        table_client.delete_record(cmdb_table, configuration_item, module.check_mode)
        return (
            True,
            None,
            dict(before=mapper.to_ansible(configuration_item), after=None),
        )

    return False, None, dict(before=None, after=None)


def build_payload(module, table_client):
    payload = (module.params["other"] or {}).copy()
    payload.update(utils.filter_dict(module.params, *DIRECT_PAYLOAD_FIELDS))

    if module.params["assigned_to"]:
        user = table.find_user(table_client, module.params["assigned_to"])
        payload["assigned_to"] = user["sys_id"]

    return payload


def ensure_present(module, table_client):
    mapper = utils.PayloadMapper(PAYLOAD_FIELDS_MAPPING, module.warn)
    query = utils.filter_dict(module.params, "sys_id")
    payload = build_payload(module, table_client)

    if not query:
        cmdb_table = module.params["sys_class_name"] or "cmdb_ci"

        if not module.params["name"]:
            raise errors.ServiceNowError("Missing required parameter: name")
        # User did not specify existing CI, so we need to create a new one.
        new = mapper.to_ansible(
            table_client.create_record(
                cmdb_table, mapper.to_snow(payload), module.check_mode
            )
        )
        return True, new, dict(before=None, after=new)

    old = mapper.to_ansible(table_client.get_record("cmdb_ci", query, must_exist=True))
    cmdb_table = old["sys_class_name"]
    # If necessary, fetch the record from the table for the extended CI class
    if cmdb_table != "cmdb_ci":
        old = mapper.to_ansible(
            table_client.get_record(cmdb_table, query, must_exist=True)
        )

    if utils.is_superset(old, payload):
        # No change in parameters we are interested in - nothing to do.
        return False, old, dict(before=old, after=old)

    new = mapper.to_ansible(
        table_client.update_record(
            cmdb_table, mapper.to_snow(old), mapper.to_snow(payload), module.check_mode
        )
    )
    return True, new, dict(before=old, after=new)


def run(module, table_client):
    if module.params["state"] == "absent":
        return ensure_absent(module, table_client)
    return ensure_present(module, table_client)


def main():
    module_args = dict(
        arguments.get_spec("instance", "sys_id"),
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
        short_description=dict(
            type="str",
        ),
        sys_class_name=dict(
            type="str",
        ),
        asset_tag=dict(
            type="str",
        ),
        install_status=dict(
            type="str",
            choices=[i[1] for i in PAYLOAD_FIELDS_MAPPING["install_status"] if i[0]],
        ),
        operational_status=dict(
            type="str",
            choices=[
                i[1] for i in PAYLOAD_FIELDS_MAPPING["operational_status"] if i[0]
            ],
        ),
        serial_number=dict(
            type="str",
        ),
        ip_address=dict(
            type="str",
        ),
        mac_address=dict(
            type="str",
        ),
        category=dict(
            type="str",
        ),
        environment=dict(
            type="str",
            choices=[
                "development",
                "production",
                "test",
            ],
        ),
        assigned_to=dict(
            type="str",
        ),
        other=dict(
            type="dict",
        ),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=[
            ("state", "absent", ("sys_id",)),
        ],
    )

    try:
        snow_client = client.Client(**module.params["instance"])
        table_client = table.TableClient(snow_client)
        changed, record, diff = run(module, table_client)
        module.exit_json(changed=changed, record=record, diff=diff)
    except errors.ServiceNowError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
