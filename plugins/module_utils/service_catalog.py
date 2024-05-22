# -*- coding: utf-8 -*-
# Copyright: 2024, Contributors to the Ansible project
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


SN_BASE_PATH = "api/sn_sc/servicecatalog"


class ItemContent(object):
    FULL = 1
    BRIEF = 2
    NONE = 3

    @classmethod
    def from_str(cls, s):
        if s == "full":
            return ItemContent.FULL
        if s == "brief":
            return ItemContent.BRIEF
        return ItemContent.NONE


class ServiceCatalogObject(object):
    def to_ansible(self):
        """Filters out the fields which we don't want to return like `header_icon`"""
        ansible_data = dict()
        for key in self.DISPLAY_FIELDS:
            if key in self.data:
                if isinstance(self.data[key], ServiceCatalogObject):
                    ansible_data[key] = self.data[key].to_ansible()
                    continue
                if isinstance(self.data[key], list):
                    ansible_data[key] = []
                    for item in self.data[key]:
                        if isinstance(item, ServiceCatalogObject):
                            ansible_data[key].append(item.to_ansible())
                        else:
                            ansible_data[key].append(item)
                    continue
                ansible_data[key] = self.data[key]
        return ansible_data

    @property
    def sys_id(self):
        return self.data["sys_id"] if "sys_id" in self.data else ""


class Catalog(ServiceCatalogObject):
    DISPLAY_FIELDS = [
        "sys_id",
        "description",
        "title",
        "has_categories",
        "has_items",
        "categories",
        "sn_items",
    ]

    def __init__(self, data=None):
        if not data:
            self.data = dict()
        else:
            self.data = data
        self._categories = []
        self._items = []

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, categories):
        self._categories = categories

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, items):
        self._items = items

    def to_ansible(self):
        self.data["categories"] = self.categories
        self.data["sn_items"] = self.items
        return super(Catalog, self).to_ansible()


class Category(ServiceCatalogObject):
    DISPLAY_FIELDS = [
        "sys_id",
        "description",
        "title",
        "full_description",
        "subcategories",
    ]

    def __init__(self, data=None):
        if not data:
            self.data = dict()
        else:
            self.data = data


class Item(ServiceCatalogObject):
    DISPLAY_FIELDS = [
        "sys_id",
        "short_description",
        "description",
        "availability",
        "mandatory_attachment",
        "request_method",
        "type",
        "sys_class_name",
        "catalogs",
        "name",
        "category",
        "order",
        "categories",
        "variables",
    ]

    def __init__(self, data=None):
        if not data:
            self.data = dict()
        else:
            self.data = data


class ServiceCatalogClient(object):
    """Wraps the generic client with Service Catalog specific methods"""

    def __init__(self, generic_client):
        if not generic_client:
            raise ValueError("generic client cannot be none")
        self.generic_client = generic_client

    def get_catalogs(self):
        """Returns the list of all catalogs"""
        records = self.generic_client.list_records("/".join([SN_BASE_PATH, "catalogs"]))
        if records:
            return [Catalog(record) for record in records]
        return []

    def get_catalog(self, id):
        """Returns the catalog identified by id"""
        if not id:
            raise ValueError("catalog sys_id is missing")
        record = self.generic_client.get_record_by_sys_id(
            "/".join([SN_BASE_PATH, "catalogs"]), id
        )
        if record:
            return Catalog(record)
        return None

    def get_categories(self, catalog_id):
        """Returns the list of all categories of the catalog `catalog_id`"""
        if not id:
            raise ValueError("catalog sys_id is missing")
        records = self.generic_client.list_records(
            "/".join([SN_BASE_PATH, "catalogs", catalog_id, "categories"])
        )
        if records:
            return [Category(record) for record in records]
        return []

    def get_items(self, catalog_id, query=None, batch_size=1000):
        """Returns the list of all items of the catalog `catalog_id`"""
        if not id:
            raise ValueError("catalog sys_id is missing")
        _query = dict(sysparm_catalog=catalog_id)
        if query:
            _query.update(query)
        self.generic_client.batch_size = batch_size
        records = self.generic_client.list_records(
            "/".join([SN_BASE_PATH, "items"]), _query
        )
        if records:
            return [Item(record) for record in records]
        return []

    def get_item(self, id):
        if not id:
            raise ValueError("item sys_id is missing")
        return Item(
            self.generic_client.get_record_by_sys_id(
                "/".join([SN_BASE_PATH, "items"]), id
            )
        )
