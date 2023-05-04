#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: attachment_upload

author:
  - Polona Mihalič (@PolonaM)

short_description: a module that users can use to upload attachment to selected table

description:
  - Upload attachment using table name and table sys_id.
version_added: 2.0.0 # WHICH VERSION?
extends_documentation_fragment:
  - servicenow.itsm.instance
  - servicenow.itsm.attachments
seealso:
  - module: servicenow.itsm.attachement # SHOULD BE RENAMED TO ATTACHMENT_INFO

options:
  table_name:
    description:
      - Table to attach the file to.
    type: str
    required: true
  table_sys_id:
    description:
      - Record to attach the file to.
    type: str
    required: true

notes:
  - Supports check_mode.
"""

EXAMPLES = r"""
- name: Upload attachment to table
  servicenow.itsm.attachment_upload:
    instance:
      host: https://instance_id.service-now.com
      username: user
      password: pass
    table_name: incident
    table_sys_id: 003a3ef24ff1120031577d2ca310c74b
    attachments:
      - path: path/to/attachment1.txt
        name: attachment1
      - path: path/to/attachment2.txt
        name: attachment2
"""


RETURN = r"""
records:
  description: List of attachments # update
  returned: success
  type: list
  elements: dict
  sample:
    "average_image_color": "",
    "chunk_size_bytes": "700000",
    "compressed": "true",
    "content_type": "text/plain",
    "download_link": "https://dev139037.service-now.com/api/now/attachment/f2d5cb9647222110afc6fa37536d4361/file",
    "file_name": "sample_file2.txt",
    "hash": "f52a678046a6f06e5fca54b4c535b210f29cbaf1134f2b75197cf47078621902",
    "image_height": "",
    "image_width": "",
    "size_bytes": "210",
    "size_compressed": "207",
    "state": "pending",
    "sys_created_by": "admin",
    "sys_created_on": "2023-05-04 08:53:07",
    "sys_id": "f2d5cb9647222110afc6fa37536d4361",
    "sys_mod_count": "0",
    "sys_tags": "",
    "sys_updated_by": "admin",
    "sys_updated_on": "2023-05-04 08:53:07",
    "table_name": "incident",
    "table_sys_id": "7cd58f1647222110afc6fa37536d43ed"
"""


from ansible.module_utils.basic import AnsibleModule

from ..module_utils import (
    arguments,
    attachment,
    client,
    errors,
)


def run(module, attachment_client):
    attachments = attachment.transform_metadata_list(
        module.params["attachments"], module.sha256
    )
    old_attachments = attachment_client.list_records(
        dict(table_name=module.params["table_name"], table_sys_id=module.params["table_sys_id"])
    )

    changed, unchanged = attachment.are_changed_return_records(old_attachments, attachments)
    if not changed:
    # if not any(
    #     attachment.are_changed(old_attachments, attachments)
    # ):
        return False, unchanged, dict(before=unchanged, after=unchanged)

    updated_attachments = attachment_client.update_records(
        module.params["table_name"],
        module.params["table_sys_id"],
        attachments,
        changed,
        module.check_mode,  # if check_mode = True then list of queries is returned
    )

    return True, updated_attachments + unchanged, dict(before=changed + unchanged, after=updated_attachments + unchanged)


def main():
    module_args = dict(
        arguments.get_spec("instance", "attachments"),
        table_sys_id=dict(
            type="str",
            required=True,
        ),
        table_name=dict(
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
        changed, records, diff = run(module, attachment_client)
        module.exit_json(changed=changed, records=records, diff=diff)
    except errors.ServiceNowError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
