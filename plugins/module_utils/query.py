# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


# https://docs.servicenow.com/bundle/quebec-platform-user-interface/page/use/common-ui-elements/reference/r_OpAvailableFiltersQueries.html
OPERATORS_STRING = set(
    (
        "STARTSWITH",
        "%",
        "ENDSWITH",
        "*",
        "LIKE",
        "!*",
        "NOT LIKE",  # Space added based on example query in the upstream docs
        "=",
        "!=",
        "ISEMPTY",
        "ISNOTEMPTY",
        "ANYTHING",
        "EMPTYSTRING",
        "<=",
        ">=",
        "BETWEEN",
        "SAMEAS",
        "NSAMEAS",
    )
)
OPERATORS_REFERENCE = set(
    (
        "=",
        "!=",
        "ISEMPTY",
        "ISNOTEMPTY",
        "STARTSWITH",
        "%",
        "ENDSWITH",
        "*",
        "LIKE",
        "!*",
        "NOT LIKE",  # Space added based on example query in the upstream docs
        "ANYTHING",
        "SAMEAS",
        "NSAMEAS",
        "EMPTYSTRING",
        "DYNAMIC",
    )
)
OPERATORS_CHOICE_STRINGS = set(
    (
        "=",
        "!=",
        "IN",
        "NOT IN",
        "LIKE",
        "STARTSWITH",
        "%",
        "ENDSWITH",
        "NOT LIKE",
        "ANYTHING",
        "SAMEAS",
        "NSAMEAS",
    )
)
OPERATORS_CHOICE_INTEGERS = set(
    (
        "=",
        "!=",
        "IN",
        "NOT IN",
        "EMPTY",
        "NOTEMPTY",
        "<",
        ">",
        "<=",
        ">=",
        "BETWEEN",
        "ANYTHING",
        "SAMEAS",
        "NSAMEAS",
    )
)
OPERATORS_DATE_TIME = set(
    (
        "ONToday",
        "NOTONToday",
        "<",
        "<=",
        ">",
        ">=",
        "BETWEEN",
        "DATEPART",
        "RELATIVEGE",
        "RELATIVELE",
        "RELATIVEGT",
        "RELATIVELT",
        "RELATIVEEE",
        "ISEMPTY",
        "ISNOTEMPTY",
        "ANYTHING",
        "SAMEAS",
        "NSAMEAS",
        "MORETHAN",
        "LESSTHAN",
    )
)
OPERATORS_NUMERIC = set(
    (
        "=",
        "!=",
        "ISEMPTY",  # EMPTY changed to ISEMPTY based on example query in the upstream docs
        "ISNOTEMPTY",  # NOTEMPTY changed to ISNOTEMPTY based on example query in the upstream docs
        "<",
        ">",
        "<=",
        ">=",
        "BETWEEN",
        "ANYTHING",
        "SAMEAS",
        "NSAMEAS",
        "GT_FIELD",
        "LT_FIELD",
        "GT_OR_EQUALS_FIELD",
        "LT_OR_EQUALS_FIELD",
    )
)
OPERATORS_BOOLEAN = set(
    (
        "=",
        "!=",
        "ISEMPTY",
        "ISNOTEMPTY",
        "ANYTHING",
        "SAMEAS",
        "NSAMEAS",
    )
)
OPERATORS_EMAIL = set(("VALCHANGES", "CHANGESFROM", "CHANGESTO"))

UNARY_OPERATORS = set(
    (
        "ISEMPTY",
        "ISNOTEMPTY",
        "ANYTHING",
        "EMPTYSTRING",
        "ONToday",
        "NOTONToday",
        "VALCHANGES",
    )
)

OPERATORS = (
    OPERATORS_STRING
    | OPERATORS_REFERENCE
    | OPERATORS_CHOICE_STRINGS
    | OPERATORS_CHOICE_INTEGERS
    | OPERATORS_DATE_TIME
    | OPERATORS_NUMERIC
    | OPERATORS_BOOLEAN
    | OPERATORS_EMAIL
)

# Example:
#   - starts_with is not one-side operator, as it's used in the following way: short_descriptionSTARTSWITHSAP
#   - is_empty is one-side operator, as it's used in the following way: short_descriptionISEMPTY
#     (meaning, there is no comparison attribute on the right side)
# This will play a role in /plugins/module_utils/utils.py's method sysparm_query_from_conditions, where it's important
# how to set the URL for the search query
ONE_SIDE_OPERATORS = [
    'is_empty', 'is_not_empty', 'is_anything', 'is_empty_string',
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
# Additionally adding 'is' as a key in the dict the following way as 'is' is python's builtin word.
OPERATORS_MAPPING['is'] = '='


def get_operator_and_value(condition):
    # Return operator and value
    for o in OPERATORS:
        if condition == o:
            return (o, "")

        elif condition.startswith(o) and condition[len(o)] == " ":
            return (o, condition[len(o) + 1 :])

    return None, None


def parse_query(query):
    # input: list({"caller": "= abel.tuter", "state": "= new"}, {"short_description": "LIKE SAP"})
    # output: list({"caller": ("=", "able.tuter"), "state": ("=", "new")}, {"short_description": ("LIKE", "SAP")}})
    parsed_query, errors = [], []

    for old_subquery in query:
        new_subquery = dict()
        for column, condition in old_subquery.items():
            oper, field = get_operator_and_value(condition)

            if not oper:
                errors.append(
                    "Invalid condition '{0}' for column '{1}'.".format(
                        condition, column
                    )
                )
                continue

            if oper in UNARY_OPERATORS and field:
                errors.append("Operator {0} does not take any arguments".format(oper))
                continue

            new_subquery[column] = (oper, field)

        if new_subquery:
            parsed_query.append(new_subquery)

    return parsed_query, errors


def serialize_query(query):
    # input: list({"caller_id": ("=", "712083754987"), "state": ("=", "3")}, {})
    # output: "caller_id=712083754987^state=3"
    subqueries = []

    for subquery in query:
        conditions = []
        for column, (operator, value) in subquery.items():
            conditions.append(column + operator + value)
        # isert AND between items
        subqueries.append("^".join(conditions))

    # insert OR between items
    return "^NQ".join(subqueries)


def map_query_values(query, mapper):
    for subquery in query:
        for_lut = dict((key, value[1]) for (key, value) in subquery.items())
        lut = mapper.to_snow(for_lut)

        for k, v in lut.items():
            subquery[k] = (subquery[k][0], v)

    return query
