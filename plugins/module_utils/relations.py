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


def _extend_records_with_groups(records, groups):
    for record in records:
        sys_id = record.get("sys_id")
        sys_id_groups = groups.get(sys_id, set())
        existing = record.get("relationship_groups", set())
        record["relationship_groups"] = existing.union(sys_id_groups)

    return records


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


def _relations_to_groups(rel_records):
    groups = dict()

    extract_relation = dict(
        parent=_extract_parent_relation, child=_extract_child_relation
    )

    for rel_record in rel_records or list():
        for target in ("child", "parent"):
            t_extr_rel = extract_relation[target]
            sys_id, ci_name, ci_class, ci_rel_type = t_extr_rel(rel_record)

            if sys_id and ci_name and ci_rel_type and ci_class:
                rel_group = _format_group_name(ci_name, ci_rel_type)

                items = groups.setdefault(sys_id, set())
                items.add(rel_group)

    return groups


def enhance_records_with_rel_groups(records, rel_records):
    groups = _relations_to_groups(rel_records)
    records = _extend_records_with_groups(records, groups)

    return records


def _build_relationship_adjacency_maps(
    relationship_records: list, relationship_types=None
) -> tuple:
    """Build parent/child adjacency lists from cmdb_rel_ci relationship records.

    Args:
        relationship_records: List of relationship records from the cmdb_rel_ci table,
            each containing dot-walked fields (parent.sys_id, child.sys_id,
            type.name, etc.).
        relationship_types: Optional list of relationship type names (e.g.
            "Runs on::Runs") to include. When None, all types are included.

    Returns:
        A tuple of (child_to_parent, parent_to_child) dicts. Each maps a CI
        sys_id to a list of (neighbor_sys_id, neighbor_name,
        neighbor_sys_class_name, rel_type) tuples representing its adjacent
        nodes in that direction.
    """
    relationship_types_set = set(relationship_types) if relationship_types else None
    child_to_parent = {}
    parent_to_child = {}

    for rel_record in relationship_records or []:
        type_name = rel_record.get(RelationshipFields.TYPE_NAME.value, "")

        # check if this relationship is one that the user actually cares about
        if relationship_types_set and type_name not in relationship_types_set:
            continue

        parent_rel_type, child_rel_type = _extract_ci_rel_type(type_name)
        parent_sys_id = rel_record.get(RelationshipFields.PARENT_SYS_ID.value, "")
        child_sys_id = rel_record.get(RelationshipFields.CHILD_SYS_ID.value, "")

        if not (child_sys_id and parent_sys_id):
            continue

        child_to_parent.setdefault(child_sys_id, []).append(
            (
                parent_sys_id,
                rel_record.get(RelationshipFields.PARENT_NAME.value, ""),
                rel_record.get(RelationshipFields.PARENT_SYS_CLASS_NAME.value, ""),
                parent_rel_type,
            )
        )
        parent_to_child.setdefault(parent_sys_id, []).append(
            (
                child_sys_id,
                rel_record.get(RelationshipFields.CHILD_NAME.value, ""),
                rel_record.get(RelationshipFields.CHILD_SYS_CLASS_NAME.value, ""),
                child_rel_type,
            )
        )

    return child_to_parent, parent_to_child


def get_relationship_adjancency_map(
    direction: str, relationship_records: list, relationship_types: list = None
) -> dict:
    """Return a single adjacency map for the requested traversal direction.

    Builds the full parent/child adjacency maps via
    _build_relationship_adjacency_maps, then returns only the map matching
    the requested direction.

    Args:
        direction: Traversal direction. "up" returns child-to-parent edges,
            "down" returns parent-to-child edges, any other value merges both
            directions into one map.
        relationship_records: Raw cmdb_rel_ci records with dot-walked fields.
        relationship_types: Optional list of relationship type names to
            include. When None, all types are included.

    Returns:
        A dict mapping each CI sys_id to a list of
        (neighbor_sys_id, neighbor_name, neighbor_sys_class_name, rel_type)
        tuples for its neighbors in the requested direction.
    """
    child_to_parent, parent_to_child = _build_relationship_adjacency_maps(
        relationship_records=relationship_records, relationship_types=relationship_types
    )
    if direction == "up":
        return child_to_parent
    elif direction == "down":
        return parent_to_child

    # combine both up and down
    adjacency = {}
    for sys_id in set(list(child_to_parent.keys()) + list(parent_to_child.keys())):
        adjacency[sys_id] = child_to_parent.get(sys_id, []) + parent_to_child.get(
            sys_id, []
        )
    return adjacency


def _process_ids_at_depth(
    adjacent_relationships: dict,
    ids_at_current_depth: list,
    visited: set,
    ci_classes_set: set,
) -> tuple:
    """Process one BFS (breadth-first search) depth level and return the next level's IDs and any matching groups.

    All unvisited neighbors are added to the next depth for traversal. Only
    neighbors with valid name/class/rel_type that pass the ci_classes filter
    produce group names.

    Args:
        adjacent_relationships: Adjacency map from get_relationship_adjancency_map.
        ids_at_current_depth: CI sys_ids to expand at this depth.
        visited: Mutable set of already-seen sys_ids; updated in place.
        ci_classes_set: Optional set of CMDB CI class names to collect.
            When None, all classes are collected.

    Returns:
        A tuple of (ids_at_next_depth, groups) where ids_at_next_depth is a
        list of newly discovered sys_ids and groups is a set of formatted
        group name strings.
    """
    ids_at_next_depth = []
    groups = set()

    for current_id in ids_at_current_depth:
        for neighbor in adjacent_relationships.get(current_id, []):
            neighbor_id, neighbor_name, neighbor_class, rel_type = neighbor

            if neighbor_id in visited:
                continue

            visited.add(neighbor_id)
            ids_at_next_depth.append(neighbor_id)

            if not all([neighbor_name, rel_type, neighbor_class]):
                continue

            if ci_classes_set and neighbor_class not in ci_classes_set:
                continue

            groups.add(_format_group_name(neighbor_name, rel_type))

    return ids_at_next_depth, groups


def _transform_adjacent_relationships_into_groups(
    adjacent_relationships: dict,
    starting_sys_id: str,
    max_depth: int,
    ci_classes: list,
) -> set:
    """Perform a BFS (breadth-first search) from a single CI and return group names for matching neighbors.

    Traverses the adjacency map up to max_depth hops from starting_sys_id.
    All reachable nodes are walked through, but only those whose CI class
    passes the ci_classes filter produce group names in the result.

    Args:
        adjacent_relationships: Adjacency map from get_relationship_adjancency_map.
        starting_sys_id: The sys_id of the CI to traverse from.
        max_depth: Maximum number of hops to traverse.
        ci_classes: Optional list of CMDB CI class names to collect.
            When None, all classes are collected.

    Returns:
        A set of formatted group name strings for matching neighbors.
    """
    ci_classes_set = set(ci_classes) if ci_classes else None
    groups = set()
    visited = {starting_sys_id}
    ids_at_current_depth = [starting_sys_id]

    for _ in range(max_depth):
        if not ids_at_current_depth:
            break
        ids_at_current_depth, new_groups = _process_ids_at_depth(
            adjacent_relationships, ids_at_current_depth, visited, ci_classes_set
        )
        groups.update(new_groups)

    return groups


def enhance_records_with_multihop_groups(
    records: list,
    relationship_records: list,
    direction: str,
    max_depth: int,
    ci_classes: list,
    relationship_types: list,
) -> list:
    """Enrich inventory records with relationship groups discovered via multi-hop BFS (breadth-first search).

    Builds an adjacency map from the raw cmdb_rel_ci relationship records,
    then performs a breadth-first traversal up to max_depth hops from each
    record. Discovered neighbors are added as relationship_groups on each
    record (e.g. "myserver_Runs_on").

    Args:
        records: Inventory records to enrich. Each must contain a "sys_id" key.
        relationship_records: Raw cmdb_rel_ci records with dot-walked fields.
        direction: Traversal direction — "up" follows child-to-parent edges,
            "down" follows parent-to-child, any other value follows both.
        max_depth: Maximum number of hops to traverse from each source record.
        ci_classes: Optional list of CMDB CI class names (e.g.
            "cmdb_ci_server") to collect. When None, all classes are collected.
        relationship_types: Optional list of relationship type names to
            traverse. When None, all types are traversed.

    Returns:
        The input records list, with a "relationship_groups" set added or
        extended on each record.
    """
    adjacent_relationships = get_relationship_adjancency_map(
        direction=direction,
        relationship_records=relationship_records,
        relationship_types=relationship_types,
    )
    record_relationship_group_map = {}
    for record in records:
        record_sys_id = record.get("sys_id")
        if not record_sys_id:
            continue

        record_relationship_group_map[record_sys_id] = (
            _transform_adjacent_relationships_into_groups(
                adjacent_relationships=adjacent_relationships,
                starting_sys_id=record_sys_id,
                max_depth=max_depth,
                ci_classes=ci_classes,
            )
        )

    records = _extend_records_with_groups(records, record_relationship_group_map)

    return records
