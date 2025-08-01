# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


PAYLOAD_FIELDS_MAPPING = dict(
    state=[
        ("-5", "pending"),
        ("1", "open"),
        ("2", "work_in_progress"),
        ("3", "closed_complete"),
        ("4", "closed_incomplete"),
        ("5", "closed_skipped"),
    ],
)
