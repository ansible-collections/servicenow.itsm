# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
options:
  instance:
    description:
      - ServiceNow instance information.
    type: dict
    suboptions:
      host:
        description:
          - The ServiceNow host name.
          - If not set, the value of the C(SN_HOST) environment
            variable will be used.
        required: true
        type: str
      username:
        description:
          - Username used for authentication.
          - If not set, the value of the C(SN_USERNAME) environment
            variable will be used.
        required: true
        type: str
      password:
        description:
          - Password used for authentication.
          - If not set, the value of the C(SN_PASSWORD) environment
            variable will be used.
        required: true
        type: str
      client_id:
        description:
          - ID of the client application used for OAuth authentication.
          - If not set, the value of the C(SN_CLIENT_ID) environment
            variable will be used.
          - If provided, it requires I(client_secret).
        type: str
      client_secret:
        description:
          - Secret associated with I(client_id). Used for OAuth authentication.
          - If not set, the value of the C(SN_CLIENT_SECRET) environment
            variable will be used.
          - If provided, it requires I(client_id).
        type: str
      timeout:
        description:
          - Timeout in seconds for the connection with the ServiceNow instance.
          - If not set, the value of the C(SN_TIMEOUT) environment
            variable will be used.
        type: float
"""
