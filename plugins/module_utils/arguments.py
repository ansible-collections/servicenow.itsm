# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


SHARED_SPECS = dict(
    instance=dict(
        type="dict",
        apply_defaults=True,
        options=dict(
            host=dict(
                type="str",
                required=True,
            ),
            username=dict(
                type="str",
                required=True,
            ),
            password=dict(
                type="str",
                required=True,
                no_log=True,
            ),
            client_id=dict(
                type="str",
            ),
            client_secret=dict(
                type="str",
                no_log=True,
            ),
        ),
        required_together=[("client_id", "client_secret")],
    )
)


def get_spec(*param_names):
    return dict((p, SHARED_SPECS[p]) for p in param_names)
