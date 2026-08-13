# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import re
from enum import Enum

REL_TABLE = "cmdb_rel_ci"


# sysparm_fields to be used when querying REL_TABLE. Uses dot-walking
# notation to extract fields from linked tables in a single REST API call.
# https://docs.servicenow.com/bundle/tokyo-application-development/page/integrate/inbound-rest/concept/c_RESTAPI.html
class RelationshipFields(Enum):
    SYS_ID = "sys_id"
    TYPE_NAME = "type.name"
    PARENT_SYS_ID = "parent.sys_id"
    PARENT_NAME = "parent.name"
    PARENT_SYS_CLASS_NAME = "parent.sys_class_name"
    CHILD_SYS_ID = "child.sys_id"
    CHILD_NAME = "child.name"
    CHILD_SYS_CLASS_NAME = "child.sys_class_name"


REL_FIELDS = set([r.value for r in RelationshipFields])

# Similar as above but for sysparm_query
REL_QUERY = None


def _extract_ci_rel_type(type_name):
    # type_name is of form "Parent description::Child description".
    # Return the value of form (Parent_description, Child_description).
    type_name = type_name or "__"
    type_name = re.sub(r"\s|:", "_", type_name)
    ci_rel_type = tuple(type_name.split("__"))

    return ci_rel_type


def _extract_parent_relation(rel_record):
    sys_id = rel_record.get(RelationshipFields.PARENT_SYS_ID.value, "")
    ci_name = rel_record.get(RelationshipFields.CHILD_NAME.value, "")
    ci_class = rel_record.get(RelationshipFields.CHILD_SYS_CLASS_NAME.value, "")
    type_name = rel_record.get(RelationshipFields.TYPE_NAME.value, "")
    ci_rel_type = _extract_ci_rel_type(type_name)[1]

    return sys_id, ci_name, ci_class, ci_rel_type


def _extract_child_relation(rel_record):
    sys_id = rel_record.get(RelationshipFields.CHILD_SYS_ID.value, "")
    ci_name = rel_record.get(RelationshipFields.PARENT_NAME.value, "")
    ci_class = rel_record.get(RelationshipFields.PARENT_SYS_CLASS_NAME.value, "")
    type_name = rel_record.get(RelationshipFields.TYPE_NAME.value, "")
    ci_rel_type = _extract_ci_rel_type(type_name)[0]

    return sys_id, ci_name, ci_class, ci_rel_type


def _format_group_name(ci_name: str, rel_type: str) -> str:
    """Format a CI name and relationship type into an Ansible group name."""
    return "{0}_{1}".format(ci_name, rel_type)


class RecordRelationshipEnhancer:
    """Enrich inventory records with CMDB relationship group names.

    Parses cmdb_rel_ci relationship records into single-hop groups and,
    when max_hop_depth > 1, builds an adjacency map for BFS traversal to
    discover multi-hop relationship groups.

    Args:
        relationship_records: Raw cmdb_rel_ci records with dot-walked fields
            (parent.sys_id, child.sys_id, type.name, etc.).
        max_hop_depth: Maximum number of hops to traverse. 1 means single-hop only.
        multi_hop_direction: Traversal direction for multi-hop — "up" follows
            child-to-parent edges, "down" follows parent-to-child, "both"
            follows both.
        multi_hop_relationship_types: Optional list of relationship type names (e.g.
            "Runs on::Runs") to include in multi-hop traversal. When None,
            all types are followed.
        multi_hop_ci_classes: Optional list of CMDB CI class names (e.g.
            "cmdb_ci_service_auto") to collect during multi-hop traversal.
            When None, all classes are collected.
    """

    def __init__(
        self,
        relationship_records: list = None,
        max_hop_depth: int = 1,
        multi_hop_direction: str = "both",
        multi_hop_relationship_types: list = None,
        multi_hop_ci_classes: list = None,
    ):
        self.relationships = relationship_records or list()
        self.multi_hop_relationship_types = (
            set(multi_hop_relationship_types) if multi_hop_relationship_types else None
        )
        self.multi_hop_ci_classes = (
            set(multi_hop_ci_classes) if multi_hop_ci_classes else None
        )
        self.max_hop_depth = max_hop_depth
        self.multi_hop_direction = multi_hop_direction

        self._adjacent_relationships_map = (
            {}
        )  # type: dict[str, list[tuple[str, str, str, str]]]
        self._single_hop_groups = {}  # type: dict[str, set[str]]

        self._parse_relationships()

    def enhance_records_with_relationship_groups(self, records: list) -> list:
        """Add a ``relationship_groups`` set to each inventory record.

        Merges single-hop groups (always present) with multi-hop groups
        (computed via BFS when max_hop_depth > 1) for each record's sys_id.

        Args:
            records: Inventory records to enrich. Each must contain a
                "sys_id" key.

        Returns:
            The input records list with "relationship_groups" added to
            each record.
        """
        for record in records:
            sys_id = record.get("sys_id")
            if not sys_id:
                continue
            single_hop = self._single_hop_groups.get(sys_id, set())
            multi_hop = set()
            if self.max_hop_depth > 1:
                multi_hop = self._transform_adjacent_relationships_into_groups(
                    starting_sys_id=sys_id,
                )
            record["relationship_groups"] = single_hop | multi_hop

        return records

    def _parse_relationships(self) -> None:
        """Parse relationship records into single-hop groups and adjacency maps.

        Iterates over all relationship records once. Single-hop groups are
        always built. The adjacency map is only built when max_hop_depth > 1.
        """
        for rel_record in self.relationships:
            self._parse_single_hop_groups(rel_record)
            if self.max_hop_depth > 1:
                self._map_relationship_adjacency(relationship=rel_record)

    def _parse_single_hop_groups(self, rel_record: dict) -> None:
        """Extract single-hop group names from a relationship record.

        For each relationship, both the parent and child CI sys_ids receive
        a group name derived from the opposite end's name and relationship
        type.
        """
        extract_func = dict(
            parent=_extract_parent_relation, child=_extract_child_relation
        )
        for target in ("child", "parent"):
            sys_id, ci_name, ci_class, ci_rel_type = extract_func[target](rel_record)
            if sys_id and ci_name and ci_rel_type and ci_class:
                self._single_hop_groups.setdefault(sys_id, set()).add(
                    _format_group_name(ci_name, ci_rel_type)
                )

    def _map_relationship_adjacency(self, relationship: dict) -> None:
        """Add a relationship record's edges to the adjacency map.

        Edges are filtered by multi_hop_relationship_types and added in the
        direction(s) specified by self.multi_hop_direction. Records missing either
        parent or child sys_id are skipped.
        """
        parent_sys_id, child_name, child_class, child_rel_type = (
            _extract_parent_relation(relationship)
        )
        child_sys_id, parent_name, parent_class, parent_rel_type = (
            _extract_child_relation(relationship)
        )

        if not (child_sys_id and parent_sys_id):
            return

        type_name = relationship.get(RelationshipFields.TYPE_NAME.value, "")
        if (
            self.multi_hop_relationship_types
            and type_name not in self.multi_hop_relationship_types
        ):
            return

        if self.multi_hop_direction in ("up", "both"):
            self._adjacent_relationships_map.setdefault(child_sys_id, []).append(
                (parent_sys_id, parent_name, parent_class, parent_rel_type)
            )

        if self.multi_hop_direction in ("down", "both"):
            self._adjacent_relationships_map.setdefault(parent_sys_id, []).append(
                (child_sys_id, child_name, child_class, child_rel_type)
            )

    def _process_ids_at_depth(
        self,
        ids_at_current_depth: list,
        visited: set,
    ) -> tuple:
        """Process one BFS depth level and return the next level's IDs and any matching groups.

        All unvisited neighbors are added to the next depth for traversal.
        Only neighbors with valid name/class/rel_type that pass the
        multi_hop_ci_classes filter produce group names.

        Args:
            ids_at_current_depth: CI sys_ids to expand at this depth.
            visited: Mutable set of already-seen sys_ids; updated in place.

        Returns:
            A tuple of (ids_at_next_depth, groups) where ids_at_next_depth
            is a list of newly discovered sys_ids and groups is a set of
            formatted group name strings.
        """
        ids_at_next_depth = []
        groups = set()

        for current_id in ids_at_current_depth:
            for neighbor in self._adjacent_relationships_map.get(current_id, []):
                neighbor_id, neighbor_name, neighbor_class, rel_type = neighbor

                if neighbor_id in visited:
                    continue

                visited.add(neighbor_id)
                ids_at_next_depth.append(neighbor_id)

                if not all([neighbor_name, rel_type, neighbor_class]):
                    continue

                if (
                    self.multi_hop_ci_classes
                    and neighbor_class not in self.multi_hop_ci_classes
                ):
                    continue

                groups.add(_format_group_name(neighbor_name, rel_type))

        return ids_at_next_depth, groups

    def _transform_adjacent_relationships_into_groups(
        self,
        starting_sys_id: str,
    ) -> set:
        """BFS from a single CI, returning group names for matching neighbors.

        Traverses the adjacency map up to max_hop_depth hops from
        starting_sys_id. All reachable nodes are walked, but only those
        whose CI class passes the multi_hop_ci_classes filter produce group names.

        Args:
            starting_sys_id: The sys_id of the CI to traverse from.

        Returns:
            A set of formatted group name strings for matching neighbors.
        """
        groups = set()
        visited = {starting_sys_id}
        ids_at_current_depth = [starting_sys_id]

        for _ in range(self.max_hop_depth):  # pylint: disable=disallowed-name
            if not ids_at_current_depth:
                break
            ids_at_current_depth, new_groups = self._process_ids_at_depth(
                ids_at_current_depth, visited
            )
            groups.update(new_groups)

        return groups
