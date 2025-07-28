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
          - Since version 2.3.0, it no longer has a default value in the argument
            specifications.
          - If not set by any means, the default value (that is, I(password)) will be set
            internally to preserve backwards compatibility.
        choices: [ 'password', 'refresh_token', 'client_credentials' ]
        type: str
        version_added: '1.1.0'
      api_path:
        description:
          - Change the API endpoint of SNOW instance from default 'api/now'.
        type: str
        default: 'api/now'
        version_added: '2.4.0'
      client_id:
        description:
          - ID of the client application used for OAuth authentication.
          - If not set, the value of the C(SN_CLIENT_ID) environment
            variable will be used.
          - If provided, it requires I(client_secret).
          - Required when I(grant_type=client_credentials).
        type: str
      client_secret:
        description:
          - Secret associated with I(client_id). Used for OAuth authentication.
          - If not set, the value of the C(SN_CLIENT_SECRET) environment
            variable will be used.
          - If provided, it requires I(client_id).
          - Required when I(grant_type=client_credentials).
        type: str
      client_certificate_file:
        description:
          - The path to the PEM certificate file that should be used for authentication.
          - The file must be local and accessible to the host running the module.
          - I(client_certificate_file) and I(client_key_file) must be provided together.
          - If client certificate parameters are provided, they will be used instead of other
            authentication methods.
        type: str
      client_key_file:
        description:
          - The path to the certificate key file that should be used for authentication.
          - The file must be local and accessible to the host running the module.
          - I(client_certificate_file) and I(client_key_file) must be provided together.
          - If client certificate parameters are provided, they will be used instead of other
            authentication methods.
        type: str
      custom_headers:
        description:
          - A dictionary containing any extra headers which will be passed with the request.
        type: dict
        version_added: '2.4.0'
      refresh_token:
        description:
          - Refresh token used for OAuth authentication.
          - If not set, the value of the C(SN_REFRESH_TOKEN) environment
            variable will be used.
          - Required when I(grant_type=refresh_token).
        type: str
        version_added: '1.1.0'
      access_token:
        description:
          - Access token obtained via OAuth authentication.
          - Used for OAuth-generated tokens that require Authorization Bearer headers.
          - If not set, the value of the C(SN_ACCESS_TOKEN) environment
            variable will be used.
          - Mutually exclusive with I(api_key).
        type: str
        version_added: '2.3.0'
      api_key:
        description:
          - ServiceNow API key for direct authentication.
          - Used for direct API keys that require x-sn-apikey headers.
          - If not set, the value of the C(SN_API_KEY) environment
            variable will be used.
          - Mutually exclusive with I(access_token).
        type: str
      timeout:
        description:
          - Timeout in seconds for the connection with the ServiceNow instance.
          - If not set, the value of the C(SN_TIMEOUT) environment variable will be used.
        type: float
        default: 10
      validate_certs:
        description:
          - If host's certificate is validated or not.
        default: True
        type: bool
        version_added: '2.3.0'
"""
