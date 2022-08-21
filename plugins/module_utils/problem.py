# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re

STATE_MAPPING = [
    ("101", "new"),
    ("102", "assess"),
    ("103", "root_cause_analysis"),
    ("104", "fix_in_progress"),
    ("106", "resolved"),
    ("107", "closed"),
]

PAYLOAD_FIELDS_MAPPING = dict(
    impact=[("1", "high"), ("2", "medium"), ("3", "low")],
    urgency=[("1", "high"), ("2", "medium"), ("3", "low")],
    problem_state=STATE_MAPPING,
    state=STATE_MAPPING,
)


class ProblemClient:
    def __init__(self, client, base_api_path):
        self.client = client
        self.base_api_path = re.sub(r"/+", "/", "/{0}/".format(base_api_path))

    def update_record(self, problem_number, data):
        new_state = data["state"]
        path = "{0}{1}/new_state/{2}".format(
            self.base_api_path, problem_number, new_state
        )
        return self.client.patch(path, data, query=dict(sysparm_exclude_reference_link=True)).json["result"]
