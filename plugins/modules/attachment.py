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
  - Download attachment using sys_id.
  - For more information, refer to the INSERT LINK FROM SERVICE NOW
version_added: 2.0.0
extends_documentation_fragment:
  - servicenow.itsm.instance
  - servicenow.itsm.sys_id

options:
  type:
    dest:
      - Specify download folder.
    type: str
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


import hashlib
import os
import time

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import (
    arguments,
    client,
    attachment,
    errors,
)


def get_checksum_dest(file_path):
    h = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()


def get_checksum_src(binary_data):
    h = hashlib.sha256()
    h.update(binary_data)
    return h.hexdigest()


def run(module, attachment_client):
    start = time.time()
    url, response = attachment_client.get_attachment(
        module.params["sys_id"], module.params["dest"]
    )
    end = time.time()
    elapsed = f"{end - start:.1f}"
    checksum_src = get_checksum_src(response.data)
    checksum_dest = get_checksum_dest(module.params["dest"])
    size = os.path.getsize(module.params["dest"])  # bytes

    return elapsed, response, checksum_src, checksum_dest, size, url


def main():
    module_args = dict(
        arguments.get_spec("instance", "sys_id"),
        dest=dict(
            type="str",
        ),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    try:
        snow_client = client.Client(**module.params["instance"])
        attachment_client = attachment.AttachmentClient(snow_client)
        elapsed, response, checksum_src, checksum_dest, size, url = run(
            module, attachment_client
        )
        module.exit_json(
            changed=True,
            checksum_src=checksum_src,
            checksum_dest=checksum_dest,
            elapsed=elapsed,
            size=size,
            status_code=response.status,
            url=url,  # the actual URL used for the request
        )
    except errors.ServiceNowError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
