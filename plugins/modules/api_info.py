#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r""" """

EXAMPLES = """ """

from ansible.module_utils.basic import AnsibleModule

from ..module_utils import arguments, attachment, client, errors, query, table, utils
from ..module_utils.change_request import PAYLOAD_FIELDS_MAPPING
from ..module_utils.utils import get_mapper


def run(module, table_client, attachment_client):
    # TODO: Implement the logic of api.py here
    hardcoded_output = -1
    return hardcoded_output


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            arguments.get_spec(
                "instance", "sys_id", "number", "query", "change_request_mapping"
            ),
        ),
        mutually_exclusive=[("sys_id", "query"), ("number", "query")],
    )

    try:
        snow_client = client.Client(**module.params["instance"])
        table_client = table.TableClient(snow_client)
        attachment_client = attachment.AttachmentClient(snow_client)
        records = run(module, table_client, attachment_client)
        module.exit_json(changed=False, record=records)
    except errors.ServiceNowError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
