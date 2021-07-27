# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  attachments:
    description:
      - ServiceNow attachments.
    type: dict
    suboptions:
      path:
        description:
          - The ServiceNow host name.
          - If not set, the value of the C(SN_HOST) environment
            variable will be used.
        required: true
        type: str
      name:
        description:
          - Name of the file to be uploaded without the file extension.
        required: false
        type: str
      type:
        description:
          - MIME type of the file to be attached.
        required: false
        type: str
"""
