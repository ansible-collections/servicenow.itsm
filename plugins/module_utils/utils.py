# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

from ansible_collections.servicenow.itsm.plugins.module_utils.query import (
    OPERATORS_MAPPING,
    ONE_SIDE_OPERATORS,
)

__metaclass__ = type


def filter_dict(input, *field_names):
    output = {}

    for field_name in field_names:
        if field_name in input:
            value = input[field_name]
            if value is not None:
                output[field_name] = value

    return output


def _operators_query_two_side(column, operator, elements, is_excludes):
    """column, =, ["a1", "a2", "a3", "a4"] -->  column=a1^ORcolumn=a2^ORcolumn=a3^ORcolumn=a4"""
    boolean_operator = "^OR" if not is_excludes else "^"
    return boolean_operator.join(
        "{0}{1}{2}".format(column, operator, i) for i in elements
    )


def _operators_query_one_side(column, operator):
    """column, EMPTYSTRING --> columnEMPTYSTRING"""
    return column + operator


def sysparm_query_from_conditions(conditions):
    # At the moment, queries for datetime fields is not supported.
    """
    From a dictionary that holds conditions for the specified fields
    dict(
       a=dict(starts_with=["a1", "a2"], ends_with=["a3", "a4"]),
       b=dict(is_not=["b1", "b2"]),
    )
    creates the value directly usable for the sysparm_query ServiceNow API
    query parameter: "aSTARTSWITHa1^ORaSTARTSWITHa2^aENDSWITHa3^ORaENDSWITHa4^b!=b1^ORb!=b2"
    More example in tests, in test_utils.py.
    """
    param_queries = []
    # column represents field we're going to describe, val represents expressions we're going to apply to that field
    for column_name, operators_dict in conditions.items():
        if not operators_dict:
            continue
        for input_operator, input_desired_values in operators_dict.items():
            query_operator = OPERATORS_MAPPING[input_operator]
            if input_operator in ONE_SIDE_OPERATORS:
                param_queries.append(
                    _operators_query_one_side(column_name, query_operator)
                )
            elif (
                input_operator in OPERATORS_MAPPING.keys()
                and input_operator not in ONE_SIDE_OPERATORS
            ):
                # ONE_SIDE_OPERATORS is subset of OPERATORS_MAPPING.keys()
                if not input_desired_values:
                    continue
                # 'excludes' is the only operator that is being tied by 'AND' operator and not by 'OR'
                param_queries.append(
                    _operators_query_two_side(
                        column_name,
                        query_operator,
                        input_desired_values,
                        input_operator == "excludes",
                    )
                )
            else:
                raise ValueError(
                    input_operator + " is not possible field for sysparm_query"
                )
    if param_queries:
        return "^".join(param_queries)
    return None


def is_superset(superset, candidate):
    for k, v in candidate.items():
        if k not in superset or superset[k] != v:
            return False

    return True


def get_choices(module, mapping_field, default_payload_fields_mapping):
    if mapping_field not in module.params:
        return default_payload_fields_mapping
    if module.params[mapping_field] is None:
        return default_payload_fields_mapping

    overrides = module.params[mapping_field]
    clone = {}
    for key, item in default_payload_fields_mapping.items():
        override = overrides.get(key)
        clone[key] = override if override else item

    return clone


def get_mapper(module, mapping_field, default_payload_fields_mapping):
    choices = get_choices(module, mapping_field, default_payload_fields_mapping)
    mapper = PayloadMapper(choices, module.warn)
    return mapper


class PayloadMapper:
    def __init__(self, mapping, unknown_value_handler=None):
        # Convert
        #   dict(a=[("s1", "a1"), ("s2", "a2")], b=[("s3", "a3")])
        # to
        #   _to_ansible == dict(a=dict(s1="a1", s2="a2"), b=dict(s3="a3"))
        #   _to_snow == dict(a=dict(a1="s1", a2="s2"), b=dict(a3="s3"))
        #
        # This allows efficient transformation of our internal values to ServiceNow
        # equivalents.

        self._to_ansible = {}
        self._to_snow = {}
        self.unknown_value_handler = unknown_value_handler

        for key, value_map in mapping.items():
            if isinstance(value_map, dict):
                self._to_ansible[key] = value_map
                self._to_snow[key] = dict(
                    (ansible_val, snow_val)
                    for snow_val, ansible_val in value_map.items()
                )
            else:
                self._to_ansible[key] = dict(value_map)
                self._to_snow[key] = dict(
                    (ansible_val, snow_val) for snow_val, ansible_val in value_map
                )

    def _map_key(self, key, val, mapping):
        if val in mapping[key]:
            return mapping[key][val]

        if self.unknown_value_handler:
            self.unknown_value_handler(
                "Encountered unknown value {0} while mapping field {1}.".format(
                    val, key
                )
            )
        return val

    def _transform(self, mapping, data):
        result = {}
        for k, v in data.items():
            if k in mapping:
                result[k] = self._map_key(k, v, mapping)
            else:
                result[k] = v
        return result

    def to_ansible(self, snow_data):
        return self._transform(self._to_ansible, snow_data)

    def to_snow(self, ansible_data):
        return self._transform(self._to_snow, ansible_data)
