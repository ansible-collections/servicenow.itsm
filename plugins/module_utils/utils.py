# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


def filter_dict(input, *field_names):
    output = {}

    for field_name in field_names:
        value = input[field_name]
        if value is not None:
            output[field_name] = value

    return output
