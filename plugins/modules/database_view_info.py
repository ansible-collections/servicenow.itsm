#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Toni Moreno <toni.moreno@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: database_view_info

author:
  - Toni Moreno (@toni-moreno)

short_description: a module that users can use to query on any previously defined database_view

description:
  - This module can be used to query any previously defined database_view
version_added: 2.0.0
extends_documentation_fragment:
  - servicenow.itsm.instance
  - servicenow.itsm.query
options:
  database_view:
    description:
      - The name of the database view to query.
    type: str
    required: true
  return_fields:
    description:
      - A list of fields to return.
    type: list
    elements: str
    required: false
notes:
  - Supports check_mode.
"""

EXAMPLES = r"""
- name: Retrieve all entries from the requested view
  servicenow.itsm.database_view_info:
    instance:
      host: https://instance_id.service-now.com
      username: user
      password: pass
    database_view: "u_my_db_view_1"
    return_fields:
    - prefix1_sys_id
    - prefix1_name
    - prefix2_name
    - prefix2_attr_1
    - prefix2_attr_2

- name: Retrieve all entries from the requested view
  servicenow.itsm.configuration_item_info:
    database_view: "u_my_db_view_2"
    query:
      - prefix1_sys_id: = <some_sys_id>
        prefix1_atribute_1: = <any_value>
      - prefix1_sys_id: = <some_sys_id>
    return_fields:
      - prefix1_sys_id
      - prefix1_name
      - prefix2_name
      - prefix2_attr_1
      - prefix2_attr_2
  register: result

- name: Retrieve all entries from that not contain SAP in the name by using field sysparm_query
  servicenow.itsm.configuration_item_info:
    database_view: "u_my_db_view_2"
    sysparm_query: nameNOT LIKESAP
  register: result

"""


RETURN = r"""
record:
  description:
    - A list of database records.
    - Note that the fields of the returned records depend on the database view I(database_view) definition.
    - field names will be prefixed depending on the prefix defined in the database view definition.
    - be careful each record will have the sum of fields from each single joined table.
    - use return_fields to limit the fields to be returned.
  type: list
  elements: dict
  returned: success
  sample:
    - ms_name: MY_SERVICE
      ms_sys_id: 762ed2a807e01110befff6fd7c1ed0bf
      tns_name: AAACDB2-PDB22-DB1
      tns_operational_status: '1'
      tns_sys_id: 6a29040107a01110befff6fd7c1ed070
    - ms_name: MY_SERVICE
      ms_sys_id: 762ed2a807e01110befff6fd7c1ed0bf
      tns_name: AAACDB1-PDB11-DB2
      tns_operational_status: '1'
      tns_sys_id: 9bb1fee807241110befff6fd7c1ed089
    - ms_name: MY_SERVICE
      ms_sys_id: 762ed2a807e01110befff6fd7c1ed0bf
      tns_name: AAACDB1-PDB12-DB3
      tns_operational_status: '1'
      tns_sys_id: fac2be2c07241110befff6fd7c1ed0a9
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments, client, errors, query, table
from ..module_utils.utils import get_mapper


def sysparms_query(module, mapper):
    q = []
    if "query" in module.params and module.params["query"] is not None:
        q = module.params["query"]
    parsed, err = query.parse_query(q)
    if err:
        raise errors.ServiceNowError(err)
    return query.serialize_query(query.map_query_values(parsed, mapper))


def run(module, table_client):
    database_view = module.params["database_view"]
    mapper = get_mapper(module, "database_view_item_mapping", dict())

    if "sysparm_query" in module.params and module.params["sysparm_query"] is not None:
        q = {"sysparm_query": module.params["sysparm_query"]}
    else:
        q = {"sysparm_query": sysparms_query(module, mapper)}
    if "return_fields" in module.params and module.params["return_fields"] is not None:
        q["sysparm_fields"] = ",".join(module.params["return_fields"])
    return [
        dict(
            mapper.to_ansible(record),
        )
        for record in table_client.list_records(database_view, q)
    ]


def main():
    module_args = dict(
        arguments.get_spec("instance", "query", "sysparm_query"),
        database_view=dict(type="str", required=True),
        return_fields=dict(type="list", elements="str", required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        mutually_exclusive=[
            ("sysparm_query", "query"),
        ],
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
