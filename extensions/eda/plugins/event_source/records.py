#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r'''
module: records
short_description: Event Driven Ansible source for ServiceNow records.
description:
  - Poll the ServiceNow API for any new records in a table, using them as a source for Event Driven Ansible.

author:
  - ServiceNow ITSM Collection Contributors (@ansible-collections)

extends_documentation_fragment:
  - servicenow.itsm.query
  - servicenow.itsm.instance

options:
  table:
    description:
      - ServiceNow table to query for new records.
    required: true
  interval:
    description:
      - THe number of seconds to wait before performing another query.
    required: false
    default: 5
  updated_since:
    description:
      - Specify the time that a record must be updated after to be considered new and captured by this plugin.
      - This value should be a date string in the format of "%Y-%m-%d %H:%M:%S".
      - If not specified, the plugin will use the current time as a default. This means any records updated
        after the plugin started will be captured.
    required: false
'''

EXAMPLES = r'''
- name: Watch for new records
    hosts: localhost
    sources:
    - cloin.eda.snow_records:
        instance: https://dev-012345.service-now.com
        username: ansible
        password: ansible
        table: incident
        interval: 1
    rules:
    - name: New record created
        condition: event.sys_id is defined
        action:
        debug:
'''

import asyncio
from typing import Any, Dict
import datetime

# hack until imports are figured out
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from plugins.module_utils.instance_config import get_combined_instance_config
from plugins.module_utils import client, table


# Entrypoint from ansible-rulebook
async def main(queue: asyncio.Queue, args: Dict[str, Any]):

    instance_config = get_combined_instance_config(config_from_params=args.get("instance"))
    table_name    = args.get("table")
    query    = args.get("query")
    interval = int(args.get("interval", 5))
    updated_since = parse_string_to_datetime(args.get("updated_since"))

    snow_client = client.Client(**instance_config)
    table_client = table.TableClient(snow_client)

    reported_records = {}
    while True:
        next_polling_time = datetime.datetime.now() + datetime.timedelta(seconds=interval)
        print(f"Polling for new records in {table_name} since {updated_since}")
        for record in table_client.list_records(table_name, query):
            await process_record(record, updated_since, queue, reported_records)

        updated_since = next_polling_time
        print(f"Sleeping for {interval} seconds")
        await asyncio.sleep(interval)


async def process_record(record, updated_since, queue, reported_records):
    if parse_string_to_datetime(record['sys_updated_on']) < updated_since:
        return

    if has_record_been_reported(record, reported_records):
        # We already reported this record during the last polling interval.
        # We wont accidentally report it again, so we can remove it from the reported_records
        # dict so that doesnt grow indefinitely.
        del reported_records[record['sys_id']]
    else:
        # We havent reported this record yet, so we need to store it in the reported_records dict
        # and send it to the queue.
        reported_records[record['sys_id']] = record['sys_updated_on']
        await queue.put(record)


def has_record_been_reported(record, reported_records):
    if record['sys_id'] in reported_records:
        if record['sys_updated_on'] == reported_records[record['sys_id']]:
            return True
    return False


def parse_string_to_datetime(date_string: str = None):
    format_string = "%Y-%m-%d %H:%M:%S"
    if date_string is None:
        return datetime.datetime.now()

    try:
        return datetime.datetime.strptime(date_string, format_string)
    except ValueError:
        raise ValueError(f"Invalid date string: {date_string}")


if __name__ == "__main__":
    class MockQueue:
        async def put(self, event):
            print(f"{event['sys_id']=} {event['sys_updated_on']=}")

    asyncio.run(main(MockQueue(), {"table": "change_request"}))
