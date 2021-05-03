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
          - Required when using basic authentication or when I(grant_type=password).
        type: str
      password:
        description:
          - Password used for authentication.
          - If not set, the value of the C(SN_PASSWORD) environment
            variable will be used.
          - Required when using basic authentication or when I(grant_type=password).
        type: str
      grant_type:
        description:
          - Grant type used for OAuth authentication.
          - If not set, the value of the C(SN_GRANT_TYPE) environment variable will be used.
        choices: [ 'password', 'refresh_token' ]
        default: password
        type: str
        version_added: '1.1.0'
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
      refresh_token:
        description:
          - Refresh token used for OAuth authentication.
          - If not set, the value of the C(SN_REFRESH_TOKEN) environment
            variable will be used.
          - Required when I(grant_type=refresh_token).
        type: str
        version_added: '1.1.0'
      timeout:
        description:
          - Timeout in seconds for the connection with the ServiceNow instance.
          - If not set, the value of the C(SN_TIMEOUT) environment
            variable will be used.
        type: float
"""
