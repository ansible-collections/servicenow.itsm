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


def get_operator_and_value(condition):
    # Return operator and value
    for o in OPERATORS:
        if condition.startswith(o) and condition[len(o)] == " ":
            return (o, condition[len(o) + 1:])

    return None, None


def parse_query(query):
    # input: list({"caller": "= abel.tuter", "state": "= new"}, {"short_description": "LIKE SAP"})
    # output: list({"caller": ("=", "able.tuter"), "state": ("=", "new")}, {"short_description": ("LIKE", "SAP")}})
    parsed_query, errors = [], []

    for old_subquery in query:
        new_subquery = dict()
        for column, condition in old_subquery.items():
            oper, field = get_operator_and_value(condition)
            if oper:
                new_subquery[column] = (oper, field)
            else:
                errors.append(
                    "Invalid condition '{0}' for column '{1}'.".format(
                        condition, column
                    )
                )
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
