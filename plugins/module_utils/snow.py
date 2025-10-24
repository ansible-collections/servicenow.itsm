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
    def __init__(self, client, batch_size=1000, memory_efficient=True):
        self.client = client
        self.batch_size = batch_size
        self.memory_efficient = memory_efficient
        self._memory_cleanup_interval = 10  # Cleanup every 10 batches
        self._batch_count = 0

    def list(self, api_path, query=None):
        """List records with memory-efficient processing"""
        if self.memory_efficient:
            return list(self.list_generator(api_path, query))
        else:
            return self._list_accumulate(api_path, query)
    
    def _list_accumulate(self, api_path, query=None):
        """Original list method that accumulates all results in memory"""
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

        return result

    def list_generator(self, api_path, query=None):
        """Generator that yields records one at a time instead of accumulating"""
        base_query = self._sanitize_query(query)
        base_query["sysparm_limit"] = self.batch_size
        
        offset = 0
        total = 1
        
        while offset < total:
            try:
                response = self.client.get(
                    api_path,
                    query=dict(base_query, sysparm_offset=offset),
                )
                
                # Yield each record individually
                for record in response.json["result"]:
                    yield record
                
                # Memory cleanup every few batches
                self._batch_count += 1
                if self._batch_count % self._memory_cleanup_interval == 0:
                    self._cleanup_memory()
                
                # Check if we have more data
                if "x-total-count" in response.headers:
                    total = int(response.headers["x-total-count"])
                else:
                    if len(response.json["result"]) == 0:
                        break
                        
                offset += self.batch_size
                
            except Exception as e:
                logger.error(f"Error in list_generator: {e}")
                break
    
    def _cleanup_memory(self):
        """Cleanup memory and force garbage collection"""
        try:
            gc.collect()
            logger.debug("Memory cleanup performed")
        except Exception as e:
            logger.warning(f"Error during memory cleanup: {e}")

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

        record = response.json.get("result", None)
        if must_exist and not record:
            raise errors.ServiceNowError(
                "No {0} records match the sys_id {1}.".format(api_path, sys_id)
            )

        return record

    def create(self, api_path, payload, query=None):
        return self.client.post(
            api_path, payload, query=self._sanitize_query(query)
        ).json["result"]

    def update(self, api_path, sys_id, payload, query=None):
        return self.client.patch(
            "/".join((api_path.rstrip("/"), sys_id)),
            payload,
            query=self._sanitize_query(query),
        ).json["result"]

    def delete(self, api_path, sys_id):
        self.client.delete("/".join((api_path.rstrip("/"), sys_id)))

    def _sanitize_query(self, query):
        query = query or dict()
        query.setdefault("sysparm_exclude_reference_link", "true")
        return query
