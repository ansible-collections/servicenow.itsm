# -*- coding: utf-8 -*-
# Copyright: (c) 2024, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    # ServiceNow ITSM catalog_request_mapping documentation fragment
    DOCUMENTATION = r"""
options:
  catalog_request_mapping:
    description:
      - User mappings for I(catalog_request) states and fields
    type: dict
    suboptions:
      priority:
        description: User mapping for I(priority) field
        type: dict
      urgency:
        description: User mapping for I(urgency) field
        type: dict
      impact:
        description: User mapping for I(impact) field
        type: dict
      state:
        description: User mapping for I(state) field
        type: dict
      approval:
        description: User mapping for I(approval) field
        type: dict
    version_added: 2.7.0
"""
