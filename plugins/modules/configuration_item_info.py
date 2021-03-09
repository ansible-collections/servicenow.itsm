#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: configuration_item_info

author:
  - Manca Bizjak (@mancabizjak)
  - Miha Dolinar (@mdolin)
  - Tadej Borovsak (@tadeboro)

short_description: List ServiceNow configuration item

description:
  - Retrieve information about ServiceNow configuration item.
  - For more information, refer to the ServiceNow configuration item management documentation at
    U(https://docs.servicenow.com/bundle/quebec-servicenow-platform/page/product/configuration-management/concept/c_ITILConfigurationManagement.html).

extends_documentation_fragment:
  - servicenow.itsm.instance
  - servicenow.itsm.sys_id.info

seealso:
  - module: servicenow.itsm.configuration_item

options:
  sys_class_name:
    description:
      - ServiceNow configuration item class.
      - The value of this parameter should point to a ServiceNow CMDB configuration
        item table, for instance C(cmdb_ci_server).
      - For a list of valid CMDB tables, refer to ServiceNow documentation on
        U(https://docs.servicenow.com/bundle/paris-servicenow-platform/page/product/configuration-management/reference/cmdb-tables-details.html).
      - If this parameter is unset when a configuration item info is queried,
        the default value C(cmdb_ci) will be used.
    type: str
"""

EXAMPLES = r"""
- name: Retrieve all configuration items
  servicenow.itsm.configuration_item_info:
  register: result

- name: Retrieve a specific configuration item by its sys_id
  servicenow.itsm.configuration_item_info:
    sys_id: 01a9ec0d3790200044e0bfc8bcbe5dc3
  register: result
"""

RETURN = r"""
record:
  description:
    - A list of configuration item records.
    - Note that the fields of the returned records depend on the configuration
      item's I(sys_class_name).
  returned: success
  type: list
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


def run(module, table_client):
    query = utils.filter_dict(module.params, "sys_id")
    cmdb_table = module.params["sys_class_name"] or "cmdb_ci"
    mapper = utils.PayloadMapper(PAYLOAD_FIELDS_MAPPING)

    return [
        mapper.to_ansible(record)
        for record in table_client.list_records(cmdb_table, query)
    ]


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec("instance", "sys_id"),
            sys_class_name=dict(
                type="str",
            ),
        ),
    )

    try:
        snow_client = client.Client(**module.params["instance"])
        table_client = table.TableClient(snow_client)
        records = run(module, table_client)
        module.exit_json(changed=False, records=records)
    except errors.ServiceNowError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
