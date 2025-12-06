# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json


class ServiceNowError(Exception):
    def to_module_fail_json_output(self):
        return {
            "msg": str(self),
        }

    def _is_jsonable(self, x):
        try:
            _ = json.dumps(x)  # pylint: disable=unused-variable
            return True
        except Exception:
            return False


class AuthError(ServiceNowError):
    pass


class UnexpectedAPIResponse(ServiceNowError):
    def __init__(self, status, data):
        self.message = "Unexpected response - {0} {1}".format(status, data)
        super(UnexpectedAPIResponse, self).__init__(self.message)


class ApiCommunicationError(ServiceNowError):
    def __init__(self, exception, message = None, **kwargs):
        self.message = message or "An unexpected error occurred while communicating with the ServiceNow API."
        self.exception = exception
        self.kwargs = kwargs

    def to_module_fail_json_output(self):
        return {
            "msg": self.message,
            "exception_info": {
                "message": str(self.exception),
                "type": self.exception.__class__.__name__,
            },
            "debug_info": {k: v for k, v in self.kwargs.items() if self._is_jsonable(v)},
        }
