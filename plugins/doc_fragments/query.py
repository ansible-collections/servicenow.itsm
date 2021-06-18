# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  query:
    description:
      - Provides a set of operators for use with filters, condition builders, and encoded queries.
      - The data type of a field determines what operators are available for it.
        Refer to the ServiceNow Available Filters Queries documentation at
        U(https://docs.servicenow.com/bundle/quebec-platform-user-interface/page/use/common-ui-elements/reference/r_OpAvailableFiltersQueries.html).
    type: list
    elements: dict
"""
