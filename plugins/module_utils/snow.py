# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Red Hat
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import gc
import logging

from . import errors

logger = logging.getLogger(__name__)


class SNowClient:
    def __init__(self, client, batch_size=1000, memory_efficient=False):
        self.client = client
        self.batch_size = batch_size
        self.memory_efficient = memory_efficient
        self._memory_cleanup_interval = 50  # More frequent cleanup
        self._batch_count = 0
        self._response_objects = []  # Track response objects for cleanup
        self._max_response_objects = 100  # Maximum tracked responses

    def _cleanup_memory(self):
        """Force garbage collection to free memory"""
        # Clean up tracked response objects
        for response in self._response_objects:
            if hasattr(response, "clear_cache"):
                response.clear_cache()
        self._response_objects.clear()

        # Force garbage collection multiple times
        for _ in range(3):
            gc.collect()
        logger.debug("Memory cleanup performed")

    def cleanup_responses(self):
        """Explicitly clean up all tracked response objects"""
        cleaned_count = 0
        for response in self._response_objects:
            if hasattr(response, "clear_cache"):
                response.clear_cache()
                cleaned_count += 1
        self._response_objects.clear()
        logger.debug("Cleaned up %d response objects", cleaned_count)

    def list(self, api_path, query=None):
        if self.memory_efficient:
            return self.list_generator(api_path, query)
        else:
            return self._list_accumulate(api_path, query)

    def _list_accumulate(self, api_path, query=None):
        """Original list method that accumulates all results"""
        base_query = self._sanitize_query(query)
        base_query["sysparm_limit"] = self.batch_size

        offset = 0
        total = 1  # Dummy value that ensures loop executes at least once
        result = []

        while offset < total:
            response = self.client.get(
                api_path,
                query=dict(base_query, sysparm_offset=offset),
            )

            # Track response for cleanup
            self._response_objects.append(response)
            if len(self._response_objects) > self._max_response_objects:
                old_response = self._response_objects.pop(0)
                if hasattr(old_response, "clear_cache"):
                    old_response.clear_cache()

            result.extend(response.json["result"])
            # This is a header only for Table API.
            # When using this client for generic api, the header is not present anymore
            # and we need to find a new method to break from the loop
            # It can be removed from Table API but for it's better to keep it for now.
            if "x-total-count" in response.headers:
                total = int(response.headers["x-total-count"])
            else:
                if len(response.json["result"]) == 0:
                    break

            offset += self.batch_size

            # Memory cleanup
            self._batch_count += 1
            if self._batch_count % self._memory_cleanup_interval == 0:
                self._cleanup_memory()

        return result

    def list_generator(self, api_path, query=None):
        """Memory-efficient generator-based listing"""
        base_query = self._sanitize_query(query)
        base_query["sysparm_limit"] = self.batch_size

        offset = 0
        total = 1  # Dummy value that ensures loop executes at least once

        while offset < total:
            response = self.client.get(
                api_path,
                query=dict(base_query, sysparm_offset=offset),
            )

            # Track response for cleanup
            self._response_objects.append(response)
            if len(self._response_objects) > self._max_response_objects:
                old_response = self._response_objects.pop(0)
                if hasattr(old_response, "clear_cache"):
                    old_response.clear_cache()

            # Yield records one by one
            yield from response.json["result"]

            # This is a header only for Table API.
            # When using this client for generic api, the header is not present anymore
            # and we need to find a new method to break from the loop
            # It can be removed from Table API but for it's better to keep it for now.
            if "x-total-count" in response.headers:
                total = int(response.headers["x-total-count"])
            else:
                if len(response.json["result"]) == 0:
                    break

            offset += self.batch_size

            # Memory cleanup
            self._batch_count += 1
            if self._batch_count % self._memory_cleanup_interval == 0:
                self._cleanup_memory()

    def get(self, api_path, query, must_exist=False):
        records = self.list(api_path, query)

        if len(records) > 1:
            raise errors.ServiceNowError(
                "{0} {1} records match the {2} query.".format(
                    len(records), api_path, query
                )
            )

        if must_exist and not records:
            raise errors.ServiceNowError(
                "No {0} records match the {1} query.".format(api_path, query)
            )

        return records[0] if records else None

    def get_by_sys_id(self, api_path, sys_id, must_exist=False):
        response = self.client.get("/".join([api_path.rstrip("/"), sys_id]))

        # Track response for cleanup
        self._response_objects.append(response)
        if len(self._response_objects) > self._max_response_objects:
            old_response = self._response_objects.pop(0)
            if hasattr(old_response, "clear_cache"):
                old_response.clear_cache()

        record = response.json.get("result", None)
        if must_exist and not record:
            raise errors.ServiceNowError(
                "No {0} records match the sys_id {1}.".format(api_path, sys_id)
            )

        return record

    def create(self, api_path, payload, query=None):
        response = self.client.post(
            api_path, payload, query=self._sanitize_query(query)
        )

        # Track response for cleanup
        self._response_objects.append(response)
        if len(self._response_objects) > self._max_response_objects:
            old_response = self._response_objects.pop(0)
            if hasattr(old_response, "clear_cache"):
                old_response.clear_cache()

        return response.json["result"]

    def update(self, api_path, sys_id, payload, query=None):
        response = self.client.patch(
            "/".join((api_path.rstrip("/"), sys_id)),
            payload,
            query=self._sanitize_query(query),
        )

        # Track response for cleanup
        self._response_objects.append(response)
        if len(self._response_objects) > self._max_response_objects:
            old_response = self._response_objects.pop(0)
            if hasattr(old_response, "clear_cache"):
                old_response.clear_cache()

        return response.json["result"]

    def delete(self, api_path, sys_id):
        response = self.client.delete("/".join((api_path.rstrip("/"), sys_id)))

        # Track response for cleanup
        self._response_objects.append(response)
        if len(self._response_objects) > self._max_response_objects:
            old_response = self._response_objects.pop(0)
            if hasattr(old_response, "clear_cache"):
                old_response.clear_cache()

    def _sanitize_query(self, query):
        query = query or dict()
        query.setdefault("sysparm_exclude_reference_link", "true")
        return query
