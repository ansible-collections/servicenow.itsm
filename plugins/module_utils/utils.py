# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


def filter_dict(input, *field_names):
    output = {}

    for field_name in field_names:
        value = input[field_name]
        if value is not None:
            output[field_name] = value

    return output


def is_superset(superset, candidate):
    for k, v in candidate.items():
        if k not in superset or superset[k] != v:
            return False

    return True


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
