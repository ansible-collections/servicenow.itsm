#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
# Copyright: (c) 2021, Ansible Project
# Copyright: (c) 2021, Abhijeet Kasurde <akasurde@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: table_info
author:
  - Abhijeet Kasurde (@Akasurde)
short_description: List ServiceNow tables and related information
description:
  - Retrieve ServiceNow tables and related information.
  - For a list of valid CMDB tables, refer to ServiceNow documentation on
    U(https://docs.servicenow.com/bundle/paris-servicenow-platform/page/product/configuration-management/reference/cmdb-tables-details.html).
version_added: 1.0.0
extends_documentation_fragment:
  - servicenow.itsm.instance
options:
  sysparm_query:
    description:
    - An encoded query string used to filter the results.
    type: str
  sysparm_fields:
    description:
    - A list of fields to return in the response.
    type: list
    elements: str
    default: ["name", "label", "sys_name"]
seealso:
  - module: servicenow.itsm.incident
notes:
- Supports check mode.
"""

EXAMPLES = r"""
- name: Retrieve all tables
  servicenow.itsm.table_info:

- name: Retrieve specific properties of tables
  servicenow.itsm.table_info:
    sysparm_fields:
      - name
      - label

- name: Retrieve table information based upon the query
  servicenow.itsm.table_info:
    sysparm_query: "nameLIKEts_"
"""

RETURN = r"""
tables:
  description:
    - A list of table information.
  returned: success
  type: list
  sample:
    - name: "cmdb_ci_aws_datacenter"
      sys_name: "CMDB CI Aws Datacenter"
      label: "AWS Datacenter"
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments, client, errors, table, utils
from ..module_utils.incident import PAYLOAD_FIELDS_MAPPING


def run(module, table_client):
    query = utils.filter_dict(module.params, "sysparm_query", "sysparm_fields")
    mapper = utils.PayloadMapper(PAYLOAD_FIELDS_MAPPING)
    # sysparm_fields is a list of comma separated strings
    query["sysparm_fields"] = ",".join(module.params["sysparm_fields"])

    return [
        mapper.to_ansible(record)
        for record in table_client.list_records("sys_db_object", query)
    ]


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec("instance"),
            sysparm_query=dict(type="str"),
            sysparm_fields=dict(
                type="list",
                elements="str",
                default=[
                    "name",
                    "label",
                    "sys_name",
                ],
            ),
        ),
    )

    try:
        snow_client = client.Client(**module.params["instance"])
        table_client = table.TableClient(snow_client)
        tables = run(module, table_client)
        module.exit_json(changed=False, tables=tables)
    except errors.ServiceNowError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
