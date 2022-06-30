# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

SERVICENOW_QUERY_PREFIX = "sysparm_"

POSSIBLE_FILTER_PARAMETERS = [
    "query", "display_value", "exclude_reference_link",  "fields", "query_category",
    "query_no_domain", "no_count", "columns"
]

POSSIBLE_FIELDS = [
    'starts_with', 'ends_with', 'contains', 'does_not_contain', 'is_not', 'is_empty', 'is_not_empty', 'is_anything',
    'is_empty_string', 'less_than_or_is', 'greater_than_or_is', 'between', 'is_same', 'is_different', 'is_dynamic',
    'is_one_of', 'is_not_one_of', 'less_than', 'greater_than', 'on', 'not_on', 'trend_on_or_after',
    'trend_on_or_before', 'trend_after', 'trend', 'trend_before', 'trend_on', 'relative_on_or_after',
    'relative_on_or_before', 'relative_after', 'relative_before', 'relative_on', 'is_more_than', 'is_less_than',
    'greater_than_field', 'less_than_field', 'greater_than_or_is_field', 'less_than_or_is_field', 'changes',
    'changes_from', 'changes_to',
]

OPERATORS_MAPPING = dict(
    starts_with='STARTSWITH', ends_with='ENDSWITH', contains='LIKE', does_not_contain='NOT LIKE', is_not='!=',
    is_empty='ISEMPTY', is_not_empty='ISNOTEMPTY', is_anything='ANYTHING', is_empty_string='EMPTYSTRING',
    less_than_or_is='<=', greater_than_or_is='>=', between='BETWEEN', is_same='SAMEAS', is_different='NSAMEAS',
    is_dynamic='DYNAMIC', is_one_of='IN', is_not_one_of='NOT IN', less_than='<', greater_than='>', on='ONToday',
    not_on='NOTONToday', trend_on_or_after='DATEPART', trend_on_or_before='DATEPART', trend_after='DATEPART',
    trend='DATEPART', trend_before='DATEPART', trend_on='DATEPART', relative_on_or_after='RELATIVEGE',
    relative_on_or_before='RELATIVELE', relative_after='RELATIVGT', relative_before='RELATIVELT',
    relative_on='RELATIVEEE', is_more_than='MORETHAN', is_less_than='LESSTHAN', greater_than_field='GT_FIELD',
    less_than_field='LT_FIELD', greater_than_or_is_field='GT_OR_EQUALS_FIELD',
    less_than_or_is_field='LT_OR_EQUALS_FIELD', changes='VALCHANGES', changes_from='CHANGESFROM', changes_to='CHANGESTO'
)

SN_QUERY_MAPPING = dict(
    query='sysparm_query',
    display_value='sysparm_display_value',
    exclude_reference_link='sysparm_exclude_reference_link',
    suppress_pagination_header='sysparm_suppress_pagination_header',
    fields='sysparm_fields',
    columns='sysparm_fields',
    query_category='sysparm_query_category',
    limit='sysparm_limit',
    view='sysparm_view',
    query_no_domain='sysparm_query_no_domain',
    no_count='sysparm_no_count'
)

FIELDS_NAME = 'columns'


def transform_query_to_servicenow_query(query):
    """
    Transforms query by applying SN_QUERY_MAPPING to query's keys.
    """
    return {SN_QUERY_MAPPING[query_key]: query_value for (query_key, query_value) in query.items()}


def table_name(module):
    """
    In api.py and api_info.py the table's name is always going to be stored in module's resource
    """
    return module.params["resource"]
