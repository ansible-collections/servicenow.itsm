# -*- coding: utf-8 -*-
# Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest
from ansible_collections.servicenow.itsm.plugins.module_utils import relations
from ansible_collections.servicenow.itsm.plugins.module_utils.relations import (
    RecordRelationshipEnhancer,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestExtractRelation:
    @pytest.mark.parametrize(
        "record,expected",
        [
            (dict(), ("", "", "", "")),
            (dict(some_key="value"), ("", "", "", "")),
            ({"parent.sys_id": "s1"}, ("s1", "", "", "")),
            ({"child.name": "cn"}, ("", "cn", "", "")),
            ({"child.sys_class_name": "cscn"}, ("", "", "cscn", "")),
            ({"type.name": "par::ch"}, ("", "", "", "ch")),
            (
                {
                    "parent.sys_id": "s1",
                    "child.name": "child_name",
                    "child.sys_class_name": "child_sys_class_name",
                    "type.name": "Parent desc::Child desc",
                },
                ("s1", "child_name", "child_sys_class_name", "Child_desc"),
            ),
        ],
    )
    def test_extract_parent_relation(self, record, expected):
        actual = relations._extract_parent_relation(record)
        assert actual == expected

    @pytest.mark.parametrize(
        "record,expected",
        [
            (dict(), ("", "", "", "")),
            (dict(some_key="value"), ("", "", "", "")),
            ({"child.sys_id": "s1"}, ("s1", "", "", "")),
            ({"parent.name": "pn"}, ("", "pn", "", "")),
            ({"parent.sys_class_name": "pscn"}, ("", "", "pscn", "")),
            ({"type.name": "par::ch"}, ("", "", "", "par")),
            (
                {
                    "child.sys_id": "s1",
                    "parent.name": "parent_name",
                    "parent.sys_class_name": "parent_sys_class_name",
                    "type.name": "Parent desc::Child desc",
                },
                ("s1", "parent_name", "parent_sys_class_name", "Parent_desc"),
            ),
        ],
    )
    def test_extract_child_relation(self, record, expected):
        actual = relations._extract_child_relation(record)
        assert actual == expected


class TestGetRelationType:
    @pytest.mark.parametrize(
        "type_name,expected",
        [
            (None, ("", "")),
            ("", ("", "")),
            ("Parent::Child", ("Parent", "Child")),
            (
                "Par ent desc ription::Child description",
                ("Par_ent_desc_ription", "Child_description"),
            ),
        ],
    )
    def test_extract_rel_ci_type_empty(self, type_name, expected):
        actual = relations._extract_ci_rel_type(type_name)
        assert actual == expected


class TestRecordRelationshipEnhancer:
    REL_RECORDS = [
        {
            "parent.sys_id": "p1",
            "child.name": "cn1",
            "child.sys_class_name": "cscn1",
            "child.sys_id": "c1",
            "parent.name": "pn1",
            "parent.sys_class_name": "pscn1",
            "type.name": "parent1::child1",
        },
        {
            "parent.sys_id": "p1",
            "child.name": "cn2",
            "child.sys_class_name": "cscn2",
            "child.sys_id": "c2",
            "parent.name": "pn1",
            "parent.sys_class_name": "pscn1",
            "type.name": "parent1::child2",
        },
    ]

    MULTIHOP_REL_RECORDS = [
        {
            "parent.sys_id": "p1",
            "child.name": "cn1",
            "child.sys_class_name": "cmdb_ci_server",
            "child.sys_id": "c1",
            "parent.name": "pn1",
            "parent.sys_class_name": "cmdb_ci_app",
            "type.name": "Runs on::Runs",
        },
        {
            "parent.sys_id": "c1",
            "child.name": "cn2",
            "child.sys_class_name": "cmdb_ci_db",
            "child.sys_id": "c2",
            "parent.name": "cn1",
            "parent.sys_class_name": "cmdb_ci_server",
            "type.name": "Runs on::Runs",
        },
    ]

    def test_empty_inputs(self):
        enhancer = RecordRelationshipEnhancer(relationship_records=[], max_hop_depth=1)
        records = []
        result = enhancer.enhance_records_with_relationship_groups(records=records)
        assert result == []

    def test_single_hop_groups(self):
        enhancer = RecordRelationshipEnhancer(
            relationship_records=self.REL_RECORDS, max_hop_depth=1
        )
        records = [dict(sys_id="p1"), dict(sys_id="c1"), dict(sys_id="c2")]
        enhancer.enhance_records_with_relationship_groups(records=records)

        assert records[0]["relationship_groups"] == {"cn1_child1", "cn2_child2"}
        assert records[1]["relationship_groups"] == {"pn1_parent1"}
        assert records[2]["relationship_groups"] == {"pn1_parent1"}

    def test_record_without_matching_sys_id(self):
        enhancer = RecordRelationshipEnhancer(
            relationship_records=self.REL_RECORDS, max_hop_depth=1
        )
        records = [dict(sys_id="unknown")]
        enhancer.enhance_records_with_relationship_groups(records=records)

        assert records[0]["relationship_groups"] == set()

    def test_record_without_sys_id_skipped(self):
        enhancer = RecordRelationshipEnhancer(
            relationship_records=self.REL_RECORDS, max_hop_depth=1
        )
        records = [dict(name="no_sys_id")]
        enhancer.enhance_records_with_relationship_groups(records=records)

        assert "relationship_groups" not in records[0]

    def test_multihop_direction_up(self):
        enhancer = RecordRelationshipEnhancer(
            relationship_records=self.MULTIHOP_REL_RECORDS,
            max_hop_depth=3,
            multi_hop_direction="up",
        )
        records = [dict(sys_id="c2")]
        enhancer.enhance_records_with_relationship_groups(records=records)

        groups = records[0]["relationship_groups"]
        assert "cn1_Runs_on" in groups
        assert "pn1_Runs_on" in groups

    def test_multihop_direction_down(self):
        enhancer = RecordRelationshipEnhancer(
            relationship_records=self.MULTIHOP_REL_RECORDS,
            max_hop_depth=3,
            multi_hop_direction="down",
        )
        records = [dict(sys_id="p1")]
        enhancer.enhance_records_with_relationship_groups(records=records)

        groups = records[0]["relationship_groups"]
        assert "cn1_Runs" in groups
        assert "cn2_Runs" in groups

    def test_multihop_direction_both(self):
        enhancer = RecordRelationshipEnhancer(
            relationship_records=self.MULTIHOP_REL_RECORDS,
            max_hop_depth=3,
            multi_hop_direction="both",
        )
        records = [dict(sys_id="c1")]
        enhancer.enhance_records_with_relationship_groups(records=records)

        groups = records[0]["relationship_groups"]
        assert "pn1_Runs_on" in groups
        assert "cn2_Runs" in groups

    def test_multihop_relationship_types_filter(self):
        mixed_rel_records = self.MULTIHOP_REL_RECORDS + [
            {
                "parent.sys_id": "c1",
                "child.name": "cn3",
                "child.sys_class_name": "cmdb_ci_net",
                "child.sys_id": "c3",
                "parent.name": "cn1",
                "parent.sys_class_name": "cmdb_ci_server",
                "type.name": "Contains::Contained by",
            },
        ]

        enhancer = RecordRelationshipEnhancer(
            relationship_records=mixed_rel_records,
            max_hop_depth=3,
            multi_hop_direction="down",
            multi_hop_relationship_types=["Runs on::Runs"],
        )
        records = [dict(sys_id="p1")]
        enhancer.enhance_records_with_relationship_groups(records=records)

        groups = records[0]["relationship_groups"]
        assert "cn1_Runs" in groups
        assert "cn2_Runs" in groups
        assert "cn3_Contained_by" not in groups

    def test_multihop_ci_classes_filter(self):
        enhancer = RecordRelationshipEnhancer(
            relationship_records=self.MULTIHOP_REL_RECORDS,
            max_hop_depth=3,
            multi_hop_direction="up",
            multi_hop_ci_classes=["cmdb_ci_app"],
        )
        records = [dict(sys_id="c2")]
        enhancer.enhance_records_with_relationship_groups(records=records)

        groups = records[0]["relationship_groups"]
        assert "pn1_Runs_on" in groups
        assert "cn1_Runs_on" in groups

    def test_one_sided_sys_id_produces_single_hop_group(self):
        rel_records = [
            {
                "parent.sys_id": "p1",
                "child.name": "cn1",
                "child.sys_class_name": "cscn1",
                "child.sys_id": "",
                "parent.name": "pn1",
                "parent.sys_class_name": "pscn1",
                "type.name": "parent1::child1",
            },
        ]
        enhancer = RecordRelationshipEnhancer(
            relationship_records=rel_records, max_hop_depth=2
        )
        records = [dict(sys_id="p1")]
        enhancer.enhance_records_with_relationship_groups(records=records)

        assert "cn1_child1" in records[0]["relationship_groups"]
