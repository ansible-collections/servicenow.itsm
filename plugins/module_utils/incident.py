# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


PAYLOAD_FIELDS_MAPPING = dict(
    impact=[("1", "high"), ("2", "medium"), ("3", "low")],
    urgency=[("1", "high"), ("2", "medium"), ("3", "low")],
    state=[
        ("1", "new"),
        ("2", "in_progress"),
        ("3", "on_hold"),
        ("6", "resolved"),
        ("7", "closed"),
        ("8", "canceled"),
    ],
    hold_reason=[
        ("", ""),  # Reason not set
        ("1", "awaiting_caller"),
        ("3", "awaiting_problem"),
        ("4", "awaiting_vendor"),
        ("5", "awaiting_change"),
    ],
    close_code=[
        ("Solved (Work Around)", "Solved (Work Around)"),
        ("Solved (Permanently)", "Solved (Permanently)"),
        ("Solved Remotely (Work Around)", "Solved Remotely (Work Around)"),
        ("Solved Remotely (Permanently)", "Solved Remotely (Permanently)"),
        ("Not Solved (Not Reproducible)", "Not Solved (Not Reproducible)"),
        ("Not Solved (Too Costly)", "Not Solved (Too Costly)"),
        ("Closed/Resolved by Caller", "Closed/Resolved by Caller"),
    ],
)
