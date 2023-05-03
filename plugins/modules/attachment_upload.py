#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: attachment

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
    table_name: # add table name
    table_sys_id: 003a3ef24ff1120031577d2ca310c74b
    attachments:
      - path: path/to/attachment.txt # add more attachments
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
        description: size of the attachment in bytes
        returned: success
        type: int
        sample: 1220
    status_code:
        description: the HTTP status code from the request
        returned: success
        type: int
        sample: 200
"""


from ansible.module_utils.basic import AnsibleModule

from ..module_utils import (
    arguments,
    attachment,
    client,
    errors,
    table,
)


def ensure_present(module, table_client, attachment_client):
    attachments = attachment.transform_metadata_list(
        module.params["attachments"], module.sha256
    )

    table = table_client.get_record(table=(module.params["table_name"], module.params["table_sys_id"]), query=None, must_exist=True)

    existing_attachments = attachment_client.list_records(
        dict(table_name=module.params["table_name"], table_sys_id=module.params["table_sys_id"])
    )

    table["attachments"] = existing_attachments

    if not any(
        attachment.are_changed(existing_attachments, attachments)
    ):
        # No change in parameters we are interested in - nothing to do.
        return False, table, dict(before=table, after=table)

    updated_attachments = attachment_client.update_records(
        module.params["table_name"],
        module.params["table_sys_id"],
        attachments,
        existing_attachments,
        module.check_mode,
    )

    updated_table = table
    updated_table["attachments"] = updated_attachments

    return True, updated_table, dict(before=table, after=updated_table)


def run(module, table_client, attachment_client):
    return ensure_present(module, table_client, attachment_client)


def main():
    module_args = dict(
        arguments.get_spec("instance"),
        arguments.get_spec("attachments"),
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
        table_client = table.TableClient(snow_client)
        attachment_client = attachment.AttachmentClient(snow_client)
        changed, record, diff = run(module, table_client, attachment_client)
        module.exit_json(changed=changed, record=record, diff=diff)
    except errors.ServiceNowError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
