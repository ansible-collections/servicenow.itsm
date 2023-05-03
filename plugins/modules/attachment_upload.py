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
  description: List of attachments on selected table
  returned: success
  type: list
  contains: # contains or sample?
  sample: # contains or sample?
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

    if not any(
        attachment.are_changed(old_attachments, attachments)
    ):
        # No change in parameters we are interested in - nothing to do.
        return False, old_attachments, dict(before=old_attachments, after=old_attachments)

    updated_attachments = attachment_client.update_records(
        module.params["table_name"],
        module.params["table_sys_id"],
        attachments,
        old_attachments,
        module.check_mode,  # if check_mode = True then list of queries is returned
    )

    return True, updated_attachments, dict(before=old_attachments, after=updated_attachments)


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
