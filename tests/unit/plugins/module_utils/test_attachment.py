# -*- coding: utf-8 -*-
# Copyright: (c) 2021, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import sys

import pytest

from tempfile import mkstemp

from ansible_collections.servicenow.itsm.plugins.module_utils import errors, attachment
from ansible_collections.servicenow.itsm.plugins.module_utils.client import Response

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)

FILE_DICT = {
    "path": "some/path/file_name.txt",
    "name": "attachment_name",
    "type": "text/markdown",
    "hash": "hash",
}

FILE_DICT_DICT = {
    "attachment_name": {
        "path": "some/path/file_name.txt",
        "type": "text/markdown",
        "hash": "hash",
    },
    "another_file_name": {
        "path": "some/path/another_file_name.txt",
        "type": "text/plain",
        "hash": "hash",
    },
}


class TestAttachmentGetFileName:
    def test_name_specified(self):
        assert attachment.get_file_name(FILE_DICT) == "attachment_name"

    def test_name_omitted(self):
        fd = FILE_DICT.copy()
        fd["name"] = None
        assert attachment.get_file_name(fd) == "file_name"


class TestAttachmentGetFileType:
    def test_type_specified(self):
        assert attachment.get_file_type(FILE_DICT) == "text/markdown"

    def test_type_omitted(self):
        fd = FILE_DICT.copy()
        fd["type"] = None
        assert attachment.get_file_type(fd) == "text/plain"


class TestAttachmentBuildQuery:
    def test_name_type_specified(self):
        assert attachment.build_query("table", "1234", FILE_DICT) == {
            "file_name": "attachment_name",
            "content_type": "text/markdown",
            "table_name": "table",
            "table_sys_id": "1234",
        }

    def test_name_omitted(self):
        fd = FILE_DICT.copy()
        fd["name"] = None
        assert attachment.build_query("table", "1234", fd) == {
            "file_name": "file_name",
            "content_type": "text/markdown",
            "table_name": "table",
            "table_sys_id": "1234",
        }

    def test_type_omitted(self):
        fd = FILE_DICT.copy()
        fd["type"] = None
        assert attachment.build_query("table", "1234", fd) == {
            "file_name": "attachment_name",
            "content_type": "text/plain",
            "table_name": "table",
            "table_sys_id": "1234",
        }


class TestAttachmentTransformMetadataList:
    META_LIST = [
        {
            "path": "some/path/another_file_name.txt",
            "type": "text/plain",
        },
        {
            "path": "some/path/file_name.txt",
            "name": "attachment_name",
            "type": "text/markdown",
        },
    ]

    def test_normal(self, create_module):
        module = create_module(
            params=dict(some="param"),
        )
        module.sha256.return_value = "some_hash"

        ml = list(self.META_LIST)

        fd1, path1 = mkstemp()
        with os.fdopen(fd1, "w") as f:
            f.write("file_contents")
        fd2, path2 = mkstemp()
        with os.fdopen(fd2, "w") as f:
            f.write("another_file_contents")

        ml[0].update({"path": path1})
        ml[1].update({"path": path2})

        assert attachment.transform_metadata_list(ml, module.sha256) == {
            os.path.splitext(os.path.basename(path1))[0]: {
                "path": path1,
                "type": "text/plain",
                "hash": "some_hash",
            },
            "attachment_name": {
                "path": path2,
                "type": "text/markdown",
                "hash": "some_hash",
            },
        }

    def test_same_file_different_name(self, create_module):
        module = create_module(
            params=dict(some="param"),
        )
        module.sha256.return_value = "some_hash"

        ml = list(self.META_LIST)

        fd, path = mkstemp()
        with os.fdopen(fd, "w") as f:
            f.write("file_contents")

        ml[0].update({"path": path})
        ml[1].update({"path": path})

        assert attachment.transform_metadata_list(ml, module.sha256) == {
            os.path.splitext(os.path.basename(path))[0]: {
                "path": path,
                "type": "text/plain",
                "hash": "some_hash",
            },
            "attachment_name": {
                "path": path,
                "type": "text/markdown",
                "hash": "some_hash",
            },
        }

    def test_duplicate(self, create_module):
        module = create_module(
            params=dict(some="param"),
        )
        module.sha256.return_value = "some_hash"

        ml = list(self.META_LIST)

        fd1, path1 = mkstemp()
        with os.fdopen(fd1, "w") as f:
            f.write("file_contents")
        fd2, path2 = mkstemp()
        with os.fdopen(fd2, "w") as f:
            f.write("another_file_contents")

        ml[0].update({"path": path1, "name": "attachment_name"})
        ml[1].update({"path": path2})

        with pytest.raises(
            errors.ServiceNowError,
            match="Found 1 duplicates - cannot upload multiple attachments with the same name.",
        ):
            attachment.transform_metadata_list(ml, module.sha256)


class TestAttachmentAreChanged:
    def test_unchanged(self):
        records = [
            {"hash": "hash", "file_name": "attachment_name"},
            {"hash": "hash", "file_name": "another_file_name"},
        ]
        assert attachment.are_changed(records, FILE_DICT_DICT) == [False, False]

    def test_changed(self):
        records = [
            {"hash": "oldhash", "file_name": "attachment_name"},
            {"hash": "oldhash", "file_name": "another_file_name"},
        ]
        assert attachment.are_changed(records, FILE_DICT_DICT) == [True, True]


class TestAttachmentListRecords:
    def test_empty_response_meta(self, client):
        client.get.return_value = Response(
            200, '{"result": []}', {"X-Total-Count": "0"}
        )
        a = attachment.AttachmentClient(client)

        records = a.list_records()

        assert [] == records
        client.get.assert_called_once_with(
            "attachment",
            query=dict(
                sysparm_limit=10000,
                sysparm_offset=0,
            ),
        )

    def test_non_empty_response_meta(self, client):
        client.get.return_value = Response(
            200, '{"result": [{"a": 3, "b": "sys_id"}]}', {"X-Total-Count": "1"}
        )
        a = attachment.AttachmentClient(client)

        records = a.list_records()

        assert [dict(a=3, b="sys_id")] == records

    def test_query_passing_meta(self, client):
        client.get.return_value = Response(
            200, '{"result": []}', {"X-Total-Count": "0"}
        )
        a = attachment.AttachmentClient(client)

        a.list_records(dict(a="b"))

        client.get.assert_called_once_with(
            "attachment",
            query=dict(
                a="b",
                sysparm_limit=10000,
                sysparm_offset=0,
            ),
        )

    def test_pagination_meta(self, client):
        client.get.side_effect = (
            Response(
                200, '{"result": [{"a": 3, "b": "sys_id"}]}', {"X-Total-Count": "2"}
            ),
            Response(
                200, '{"result": [{"a": 2, "b": "sys_ie"}]}', {"X-Total-Count": "2"}
            ),
        )
        a = attachment.AttachmentClient(client, batch_size=1)

        records = a.list_records()

        assert [dict(a=3, b="sys_id"), dict(a=2, b="sys_ie")] == records
        assert 2 == len(client.get.mock_calls)
        client.get.assert_any_call(
            "attachment",
            query=dict(sysparm_limit=1, sysparm_offset=0),
        )
        client.get.assert_any_call(
            "attachment",
            query=dict(sysparm_limit=1, sysparm_offset=1),
        )


class TestAttachmentGetRecord:
    def test_single_match_meta(self, client):
        client.get.return_value = Response(
            200, '{"result": [{"a": 3, "b": "sys_id"}]}', {"X-Total-Count": "1"}
        )
        a = attachment.AttachmentClient(client)

        record = a.get_record(dict(our="query"))

        assert dict(a=3, b="sys_id") == record
        client.get.assert_called_with(
            "attachment",
            query=dict(
                our="query",
                sysparm_limit=10000,
                sysparm_offset=0,
            ),
        )

    def test_multiple_matches(self, client):
        client.get.return_value = Response(
            200, '{"result": [{"a": 3}, {"b": 4}]}', {"X-Total-Count": "1"}
        )
        a = attachment.AttachmentClient(client)

        with pytest.raises(errors.ServiceNowError, match="2"):
            a.get_record(dict(our="query"))

    def test_zero_matches(self, client):
        client.get.return_value = Response(
            200, '{"result": []}', {"X-Total-Count": "0"}
        )
        a = attachment.AttachmentClient(client)

        assert a.get_record(dict(our="query")) is None

    def test_zero_matches_fail(self, client):
        client.get.return_value = Response(
            200, '{"result": []}', {"X-Total-Count": "0"}
        )
        a = attachment.AttachmentClient(client)

        with pytest.raises(errors.ServiceNowError, match="No"):
            a.get_record(dict(our="query"), must_exist=True)


class TestAttachmentCreateRecord:
    def test_normal_mode(self, client):
        client.request.return_value = Response(
            201, '{"result": {"a": 3, "b": "sys_id"}}'
        )
        a = attachment.AttachmentClient(client)

        record = a.create_record(
            dict(some="property"),
            "file_content",
            check_mode=False,
            mime_type="text/plain",
        )

        assert dict(a=3, b="sys_id") == record
        client.request.assert_called_with(
            "POST",
            "attachment/file",
            query={"some": "property"},
            headers={"Accept": "application/json", "Content-type": "text/plain"},
            bytes="file_content",
        )

    def test_check_mode(self, client):
        client.request.return_value = Response(
            201, '{"result": {"a": 3, "b": "sys_id"}}'
        )
        a = attachment.AttachmentClient(client)

        record = a.create_record(
            dict(some="property"),
            "file_content",
            check_mode=True,
            mime_type="text/plain",
        )

        assert dict(some="property") == record
        client.request.assert_not_called()


class TestAttachmentUploadRecord:
    def test_normal_mode(self, client):
        client.request.return_value = Response(
            201, '{"result": {"a": 3, "b": "sys_id"}}'
        )
        a = attachment.AttachmentClient(client)

        fd, path = mkstemp()
        with os.fdopen(fd, "w") as f:
            f.write("file_content")
        mfd = FILE_DICT.copy()
        mfd.update({"path": path})

        record = a.upload_record("table", "1234", mfd, check_mode=False)

        assert dict(a=3, b="sys_id") == record
        client.request.assert_called_with(
            "POST",
            "attachment/file",
            query={
                "table_name": "table",
                "table_sys_id": "1234",
                "file_name": "attachment_name",
                "content_type": "text/markdown",
                "hash": "hash",
            },
            headers={"Accept": "application/json", "Content-type": "text/markdown"},
            bytes=b"file_content",
        )

    def test_check_mode(self, client):
        client.request.return_value = Response(
            201, '{"result": {"a": 3, "b": "sys_id"}}'
        )
        a = attachment.AttachmentClient(client)

        fd, path = mkstemp()
        with os.fdopen(fd, "w") as f:
            f.write("file_content")
        mfd = FILE_DICT.copy()
        mfd.update({"path": path})

        record = a.upload_record("table", "1234", mfd, check_mode=True)

        assert {
            "table_name": "table",
            "table_sys_id": "1234",
            "file_name": "attachment_name",
            "content_type": "text/markdown",
            "hash": "hash",
        } == record
        client.request.assert_not_called()


class TestAttachmentUploadRecords:
    def test_normal_mode(self, client):
        client.request.side_effect = [
            Response(201, '{"result": {"a": 3, "b": "sys_id"}}'),
            Response(201, '{"result": {"a": 4, "b": "sys_idn"}}'),
        ]
        a = attachment.AttachmentClient(client)

        fd1, path1 = mkstemp()
        with os.fdopen(fd1, "w") as f:
            f.write("file_content1")
        fd2, path2 = mkstemp()
        with os.fdopen(fd2, "w") as f:
            f.write("file_content2")

        mfdd = dict(FILE_DICT_DICT)
        mfdd["attachment_name"].update({"path": path1})
        mfdd["another_file_name"].update({"path": path2})

        record = a.upload_records("table", "1234", mfdd, check_mode=False)

        assert [dict(a=3, b="sys_id"), dict(a=4, b="sys_idn")] == record
        assert 2 == client.request.call_count
        client.request.assert_any_call(
            "POST",
            "attachment/file",
            query={
                "table_name": "table",
                "table_sys_id": "1234",
                "file_name": "attachment_name",
                "content_type": "text/markdown",
                "hash": "hash",
            },
            headers={"Accept": "application/json", "Content-type": "text/markdown"},
            bytes=b"file_content1",
        )
        client.request.assert_any_call(
            "POST",
            "attachment/file",
            query={
                "table_name": "table",
                "table_sys_id": "1234",
                "file_name": "another_file_name",
                "content_type": "text/plain",
                "hash": "hash",
            },
            headers={"Accept": "application/json", "Content-type": "text/plain"},
            bytes=b"file_content2",
        )

    def test_check_mode(self, client):
        client.request.return_value = Response(
            201, '{"result": {"a": 1, "sys_id": "1"}}'
        )
        a = attachment.AttachmentClient(client)

        fd1, path1 = mkstemp()
        with os.fdopen(fd1, "w") as f:
            f.write("file_content1")
        fd2, path2 = mkstemp()
        with os.fdopen(fd2, "w") as f:
            f.write("file_content2")

        mfdd = dict(FILE_DICT_DICT)
        mfdd["attachment_name"].update({"path": path1})
        mfdd["another_file_name"].update({"path": path2})

        record = a.upload_records("table", "1234", mfdd, check_mode=True)

        assert [
            {
                "table_name": "table",
                "table_sys_id": "1234",
                "file_name": "another_file_name",
                "content_type": "text/plain",
                "hash": "hash",
            },
            {
                "table_name": "table",
                "table_sys_id": "1234",
                "file_name": "attachment_name",
                "content_type": "text/markdown",
                "hash": "hash",
            },
        ] == sorted(record, key=lambda k: k["file_name"])
        client.request.assert_not_called()

    def test_missing_file(self, client):
        a = attachment.AttachmentClient(client)
        with pytest.raises(errors.ServiceNowError, match="Cannot open"):
            a.upload_records("table", "1234", FILE_DICT_DICT, True)


class TestAttachmentDeleteRecord:
    def test_normal_mode(self, client):
        client.delete.return_value = Response(204, "")
        a = attachment.AttachmentClient(client)
        a.delete_record(dict(sys_id="1234"), False)

        client.delete.assert_called_with("attachment/1234")

    def test_normal_mode_missing(self, client):
        client.delete.side_effect = errors.UnexpectedAPIResponse(
            404, "Record not found"
        )
        a = attachment.AttachmentClient(client)

        with pytest.raises(errors.UnexpectedAPIResponse, match="not found"):
            a.delete_record(dict(sys_id="1234"), False)

    def test_check_mode(self, client):
        client.delete.return_value = Response(204, "")
        a = attachment.AttachmentClient(client)
        a.delete_record(dict(sys_id="id"), True)

        client.delete.assert_not_called()


class TestAttachmentDeleteRecords:
    def test_normal_mode(self, client):
        client.get.return_value = Response(
            200,
            '{"result": [{"a": 3, "sys_id": "1234"}, {"a": 4, "sys_id": "4321"}]}',
            {"X-Total-Count": "2"},
        )
        client.delete.return_value = Response(204, "")
        a = attachment.AttachmentClient(client)

        a.delete_attached_records("table", 5555, False)

        assert client.delete.call_count == 2
        client.delete.assert_any_call("attachment/1234")
        client.delete.assert_any_call("attachment/4321")

    def test_normal_mode_missing(self, client):
        client.get.return_value = Response(
            200,
            '{"result": [{"a": 3, "sys_id": "1234"}, {"a": 4, "sys_id": "4321"}]}',
            {"X-Total-Count": "2"},
        )
        client.delete.side_effect = errors.UnexpectedAPIResponse(
            404, "Record not found"
        )
        a = attachment.AttachmentClient(client)

        with pytest.raises(errors.UnexpectedAPIResponse, match="not found"):
            a.delete_attached_records("table", 5555, False)

    def test_check_mode(self, client):
        client.get.return_value = Response(
            200,
            '{"result": [{"a": 3, "sys_id": "1234"}, {"a": 4, "sys_id": "4321"}]}',
            {"X-Total-Count": "2"},
        )
        client.delete.return_value = Response(204, "")
        a = attachment.AttachmentClient(client)

        a.delete_attached_records("table", 5555, True)
        client.delete.assert_not_called()


class TestAttachmentUpdateRecords:
    def test_unchanged_normal_mode(self, client):
        a = attachment.AttachmentClient(client)

        fd1, path1 = mkstemp()
        with os.fdopen(fd1, "w") as f:
            f.write("file_content")
        fd2, path2 = mkstemp()
        with os.fdopen(fd2, "w") as f:
            f.write("another_file_content")

        mfdd = dict(FILE_DICT_DICT)
        mfdd["attachment_name"].update({"path": path1})
        mfdd["another_file_name"].update({"path": path2})

        record = [
            {"hash": "hash", "sys_id": "1", "file_name": "attachment_name"},
            {"hash": "hash", "sys_id": "2", "file_name": "another_file_name"},
        ]

        changes = a.update_records("table", "1234", mfdd, record)

        assert [
            {
                "hash": "hash",
                "sys_id": "2",
                "file_name": "another_file_name",
            },
            {
                "hash": "hash",
                "sys_id": "1",
                "file_name": "attachment_name",
            },
        ] == sorted(changes, key=lambda k: k["file_name"])

    def test_changed_normal_mode(self, client):
        client.request.side_effect = [
            Response(201, '{"result": {"a": 1, "sys_id": "a"}}'),
            Response(201, '{"result": {"a": 2, "sys_id": "b"}}'),
        ]
        client.delete.return_value = Response(204, "")
        a = attachment.AttachmentClient(client)

        fd1, path1 = mkstemp()
        with os.fdopen(fd1, "w") as f:
            f.write("file_contents")
        fd2, path2 = mkstemp()
        with os.fdopen(fd2, "w") as f:
            f.write("another_file_contents")

        mfdd = dict(FILE_DICT_DICT)
        mfdd["attachment_name"].update({"path": path1})
        mfdd["another_file_name"].update({"path": path2})

        record = [
            {"hash": "oldhash", "sys_id": "1", "file_name": "attachment_name"},
            {"hash": "oldhash", "sys_id": "2", "file_name": "another_file_name"},
        ]

        changes = a.update_records("table", "1234", mfdd, record)

        assert [
            {
                "a": 1,
                "sys_id": "a",
            },
            {
                "a": 2,
                "sys_id": "b",
            },
        ] == changes

    def test_unchanged_check_mode(self, client):
        a = attachment.AttachmentClient(client)

        fd1, path1 = mkstemp()
        with os.fdopen(fd1, "w") as f:
            f.write("file_content")
        fd2, path2 = mkstemp()
        with os.fdopen(fd2, "w") as f:
            f.write("another_file_content")

        mfdd = dict(FILE_DICT_DICT)
        mfdd["attachment_name"].update({"path": path1})
        mfdd["another_file_name"].update({"path": path2})

        record = [
            {"hash": "hash", "sys_id": "1", "file_name": "attachment_name"},
            {"hash": "hash", "sys_id": "2", "file_name": "another_file_name"},
        ]

        changes = a.update_records("table", "1234", mfdd, record, True)

        assert [
            {
                "hash": "hash",
                "sys_id": "2",
                "file_name": "another_file_name",
            },
            {
                "hash": "hash",
                "sys_id": "1",
                "file_name": "attachment_name",
            },
        ] == sorted(changes, key=lambda k: k["file_name"])

    def test_changed_check_mode(self, client):
        client.request.side_effect = [
            Response(201, '{"result": {"a": 1, "sys_id": "a"}}'),
            Response(201, '{"result": {"a": 2, "sys_id": "b"}}'),
        ]
        client.delete.return_value = Response(204, "")
        a = attachment.AttachmentClient(client)

        fd1, path1 = mkstemp()
        with os.fdopen(fd1, "w") as f:
            f.write("file_contents")
        fd2, path2 = mkstemp()
        with os.fdopen(fd2, "w") as f:
            f.write("another_file_contents")

        mfdd = dict(FILE_DICT_DICT)
        mfdd["attachment_name"].update({"path": path1})
        mfdd["another_file_name"].update({"path": path2})

        record = [
            {"hash": "oldhash", "sys_id": "1", "file_name": "attachment_name"},
            {"hash": "oldhash", "sys_id": "2", "file_name": "another_file_name"},
        ]

        record = a.update_records("table", "1234", mfdd, record, True)

        assert [
            {
                "table_name": "table",
                "table_sys_id": "1234",
                "content_type": "text/plain",
                "hash": "hash",
                "file_name": "another_file_name",
            },
            {
                "table_name": "table",
                "table_sys_id": "1234",
                "content_type": "text/markdown",
                "hash": "hash",
                "file_name": "attachment_name",
            },
        ] == sorted(record, key=lambda k: k["file_name"])
