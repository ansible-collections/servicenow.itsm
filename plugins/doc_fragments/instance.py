# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = """
options:
  instance:
    description:
      - ServiceNow instance information.
    type: dict
    suboptions:
      host:
        description:
          - The ServiceNow host name.
        required: true
        type: str
      username:
        description:
          - Username used for authentication.
        required: true
        type: str
      password:
        description:
          - Password used for authentication.
        required: true
        type: str
      client_id:
        description:
          - ID of the client application used for OAuth authentication.
          - If provided, it requires I(client_secret).
        type: str
      client_secret:
        description:
          - Secret associated with I(client_id). Used for OAuth authentication.
          - If provided, it requires I(client_id).
        type: str
"""
