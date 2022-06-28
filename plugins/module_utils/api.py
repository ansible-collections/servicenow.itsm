# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

SERVICENOW_QUERY_PREFIX = "sysparm_"


def transform_query_to_servicenow_query(query):
    """
    Transforms query by adding suffix to the query
    """
    return {SERVICENOW_QUERY_PREFIX + query_key: query_value for (query_key, query_value) in query.items()}
