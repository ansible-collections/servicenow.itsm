#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: api_info

author:
  - Manca Bizjak (@mancabizjak)
  - Miha Dolinar (@mdolin)
  - Tadej Borovsak (@tadeboro)
  - Matej Pevec (@mysteriouswolf)

short_description: ServiceNow REST API "client" module

description:
    - 

"""

EXAMPLES = """ """

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments, attachment, client, errors, query, table, utils
from ..module_utils.change_request import PAYLOAD_FIELDS_MAPPING
from ..module_utils.utils import get_mapper


def remap_assignment(query, table_client):
    # TODO: Kaj ta funkcija pocne?
    query_load = []

    for item in query:
        q = dict()
        for k, v in item.items():
            # TODO: Write if/else sentences for this iteration
            pass
        query_load.append(q)

    return query_load


def sysparms_query(module, table_client, mapper):
    parsed, err = query.parse_query(module.params["query"])
    if err:
        raise errors.ServiceNowError(err)

    remap_query = remap_assignment(parsed, table_client)

    return query.serialize_query(query.map_query_values(remap_query, mapper))


def run(module, table_client):
    mapper = get_mapper(module, "api_mapping", PAYLOAD_FIELDS_MAPPING)

    module.params["sysparm_fields"] = ",".join(module.params["sysparm_fields"])

    query = utils.filter_dict(
        module.params,
        "sysparm_query", "sysparm_display_value", "sysparm_exclude_reference_link", "sysparm_fields",
        "sysparm_query_category", "sysparm_query_no_domain", "sysparm_no_count"
    )

    return [
        mapper.to_ansible(record)
        for record in table_client.list_records(module.params["resource"], query)
    ]


def main():
    arg_spec = dict(
        arguments.get_spec(
            "instance", "sys_id"
        ),
        resource=dict(  # resource - table name
            type="str",
            required=True
        ),
        sysparm_query=dict(
            type="str",
            default=None
        ),  # An encoded query string used to filter the results
        sysparm_display_value=dict(
            type="str",
            choices=[
                "true",
                "false",
                "both"
            ]
        ),  # Return field display values (true), actual values (false), or both (all) (default: false)
        sysparm_exclude_reference_link=dict(
            type="bool"
        ),  # True to exclude Table API links for reference fields (default: false)
        sysparm_fields=dict(
            type="list",
            default=[]
            # TODO: Add all possible choices for sysparam_fields
        ),  # A comma-separated list of fields to return in the response
        sysparm_query_category=dict(
            type="str"
        ),  # Name of the query category (read replica category) to use for queries
        sysparm_query_no_domain=dict(
            type="bool"
        ),  # True to access data across domains if authorized (default: false)
        sysparm_no_count=dict(
            type="bool"
        ),  # Do not execute a select count(*) on table (default: false)
    )

    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=arg_spec
    )

    try:
        # TODO:
        #   - preimenuj parametre. Predpono sysparm daj stran
        #   - Dodaj filter eq, neq, ... poglej si dele, kjer je to že razvito
        #   - Poglej: inventory vtičnik. Poglej kaj lahko pouporabimo
        #   - Zaenkrat pustimo (do srede). Docse pusti
        #   - Naslednji korak: Dodaj možnosti: create, update, delete
        #   - create: dodaj atribute, sprejmi, daj v tabelo, post
        #   - update: podobno. Mora biti neki query, ki določi zapis
        #   - delete: 2 možnosti:
        #       - Zaenkrat ne: state present/absent. Na podlagi tega ugotovimo: create/upd/del
        #       - Brisanje zapisov je možnos je ob danes sys id
        #       - trenutno: Preko state parametra
        #   - api modul naj ima tako strukturo.
        #   - Za update potrebujemo vse podatke ter navesti nove vrednosti določenih atributov
        #   - Update po svoje zastavimo
        #   - Najprej ga podprimo za post
        #   - Naredi ogrodje tega modula (za pomoč prosi Uroša)
        #   -
        snow_client = client.Client(**module.params["instance"])
        table_client = table.TableClient(snow_client)
        records = run(module, table_client)
        module.exit_json(changed=False, record=records)
    except errors.ServiceNowError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
