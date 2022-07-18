#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: attachment

author:
  - Polona Mihalič (@PolonaM)

short_description: a module that users can use to download attachment using sys_id

description:
  - Download attachment using attachment's sys_id.
version_added: 2.0.0
extends_documentation_fragment:
  - servicenow.itsm.instance

options:
  dest:
    description:
      - Specify download file.
    type: str
    required: true
  sys_id:
    description:
      - Attachment's sys_id.
    type: str
    required: true
"""

EXAMPLES = """
  - name: ServiceNow download attachment module
    servicenow.itsm.attachment:
      instance:
        host: sn_host
        username: sn_username
        password: sn_password
      dest: /tmp/sn-attachment
      sys_id: sn_attachment_id
    tags:
      - download-attachment-sn
"""


RETURN = r"""
record:
  description: download attachment record
  returned: success
  type: dict
  contains:
    elapsed:
        description: the number of seconds that elapsed while performing the download
        returned: success
        type: float
        sample: 2.3
    msg:
        description: OK or error message
        returned: always
        type: str
        sample: OK
    size:
        description: size of the target
        returned: success
        type: int
        sample: 1220
    status_code:
        description: the HTTP status code from the request
        returned: success
        type: int
        sample: 200
"""


import time
import json

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import (
    arguments,
    client,
    attachment,
    errors,
)


def run(module, attachment_client):
    start = time.time()
    response = attachment_client.get_attachment(module.params["sys_id"])
    if response.status == 200:
        attachment_client.save_attachment(response.data, module.params["dest"])
    elif response.status == 404:
        raise errors.ServiceNowError(
            "Status code: 404, Details: " + json.loads(response.data)["error"]["detail"]
        )
    end = time.time()
    elapsed = round(end - start, 2)
    size = int(json.loads(response.headers["x-attachment-metadata"])["size_bytes"])
    status_code = response.status
    msg = "OK"

    return {
        "size": size,
        "elapsed": elapsed,
        "status_code": status_code,
        "msg": msg,
    }


def main():
    module_args = dict(
        arguments.get_spec("instance"),
        # Overwrites sys_id from SHARED_SPECS to add required=True
        sys_id=dict(
            type="str",
            required=True,
        ),
        dest=dict(
            type="str",
            required=True,
        ),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    try:
        snow_client = client.Client(**module.params["instance"])
        attachment_client = attachment.AttachmentClient(snow_client)
        record = run(module, attachment_client)
        module.exit_json(changed=True, record=record)
    except errors.ServiceNowError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()