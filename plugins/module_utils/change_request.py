# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


PAYLOAD_FIELDS_MAPPING = dict(
    priority=[("1", "critical"), ("2", "high"), ("3", "moderate"), ("4", "low")],
    risk=[("1", "very_high"), ("2", "high"), ("3", "moderate"), ("4", "low")],
    impact=[("1", "high"), ("2", "medium"), ("3", "low")],
    urgency=[("1", "high"), ("2", "medium"), ("3", "low")],
    state=[
        ("-5", "new"),
        ("-4", "assess"),
        ("-3", "authorize"),
        ("-2", "scheduled"),
        ("-1", "implement"),
        ("0", "review"),
        ("3", "closed"),
        ("4", "canceled"),
    ],
    on_hold=[("true", True), ("false", False)],
)
