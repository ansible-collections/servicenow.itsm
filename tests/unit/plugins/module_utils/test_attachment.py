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
}

FILE_DICT_LIST = [
    FILE_DICT,
    {
        "path": "some/path/another_file_name.txt",
        "type": "text/plain",
    },
]


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
        assert attachment.build_query({}, FILE_DICT) == {
            "file_name": "attachment_name",
            "content_type": "text/markdown",
        }

    def test_name_omitted(self):
        fd = FILE_DICT.copy()
        fd["name"] = None
        assert attachment.build_query({}, fd) == {
            "file_name": "file_name",
            "content_type": "text/markdown",
        }

    def test_type_omitted(self):
        fd = FILE_DICT.copy()
        fd["type"] = None
        assert attachment.build_query({}, fd) == {
            "file_name": "attachment_name",
            "content_type": "text/plain",
        }

    def test_additional_payload(self):
        assert attachment.build_query(
            {
                "some": "data",
                "more": "payload",
            },
            FILE_DICT,
        ) == {
            "file_name": "attachment_name",
            "content_type": "text/markdown",
            "some": "data",
            "more": "payload",
        }


class TestAttachmentFileHash:
    def test_hash(self):
        fd, path = mkstemp()
        with os.fdopen(fd, "w") as f:
            f.write("file_content")
        assert (
            attachment.file_hash(path)
            == "76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff"
        )


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

    def test_empty_response_file(self, client):
        client.request_binary.return_value = Response(200, "", {"X-Total-Count": "0"})
        a = attachment.AttachmentClient(client)

        records = a.list_records(sys_id="1234", file=True)

        assert "" == records
        client.request_binary.assert_called_once_with(
            "GET", "attachment/1234/file", "*/*", accept_type="*/*"
        )

    def test_non_empty_response_meta(self, client):
        client.get.return_value = Response(
            200, '{"result": [{"a": 3, "b": "sys_id"}]}', {"X-Total-Count": "1"}
        )
        a = attachment.AttachmentClient(client)

        records = a.list_records()

        assert [dict(a=3, b="sys_id")] == records

    def test_non_empty_response_file(self, client):
        client.request_binary.return_value = Response(
            200, "binary_data", {"X-Total-Count": "1"}
        )
        a = attachment.AttachmentClient(client)

        records = a.list_records(sys_id="1234", file=True)

        assert "binary_data" == records

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

    def test_query_sys_id_passing_meta(self, client):
        client.get.return_value = Response(
            200, '{"result": []}', {"X-Total-Count": "0"}
        )
        a = attachment.AttachmentClient(client)

        a.list_records(dict(a="b"), "1234")

        client.get.assert_called_once_with(
            "attachment/1234",
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


class TestAttachmentListFullRecords:
    def test_empty_file_list(self, client):
        a = attachment.AttachmentClient(client)
        record = a.list_full_records(file_dict_list=[])
        assert record is None
        client.get.assert_not_called()

    def test_single_match(self, client):
        client.get.return_value = Response(
            200,
            '{"result": [{"property": "something", "sys_id": "1234"}]}',
            {"X-Total-Count": "1"},
        )
        client.request_binary.return_value = Response(
            200, "file_content", {"X-Total-Count": "1"}
        )
        a = attachment.AttachmentClient(client)

        record = a.list_full_records()

        assert [
            {"property": "something", "sys_id": "1234", "data": "file_content"}
        ] == record
        client.get.assert_called_with(
            "attachment",
            query=dict(
                sysparm_limit=10000,
                sysparm_offset=0,
            ),
        )
        client.request_binary.assert_called_with(
            "GET", "attachment/1234/file", "*/*", accept_type="*/*"
        )

    def test_single_match_with_query(self, client):
        client.get.return_value = Response(
            200,
            '{"result": [{"property": "something", "sys_id": "1234"}]}',
            {"X-Total-Count": "1"},
        )
        client.request_binary.return_value = Response(
            200, "file_content", {"X-Total-Count": "1"}
        )
        a = attachment.AttachmentClient(client)

        record = a.list_full_records(dict(our="query"))

        assert [
            {"property": "something", "sys_id": "1234", "data": "file_content"}
        ] == record
        client.get.assert_called_with(
            "attachment",
            query=dict(
                our="query",
                sysparm_limit=10000,
                sysparm_offset=0,
            ),
        )
        client.request_binary.assert_called_with(
            "GET", "attachment/1234/file", "*/*", accept_type="*/*"
        )

    def test_single_match_with_sys_id(self, client):
        client.get.return_value = Response(
            200,
            '{"result": [{"property": "something", "sys_id": "4444"}]}',
            {"X-Total-Count": "1"},
        )
        client.request_binary.return_value = Response(
            200, "file_content", {"X-Total-Count": "1"}
        )
        a = attachment.AttachmentClient(client)

        record = a.list_full_records(sys_id="4444")

        assert [
            {"property": "something", "sys_id": "4444", "data": "file_content"}
        ] == record
        client.get.assert_called_with(
            "attachment/4444",
            query=dict(
                sysparm_limit=10000,
                sysparm_offset=0,
            ),
        )
        client.request_binary.assert_called_with(
            "GET", "attachment/4444/file", "*/*", accept_type="*/*"
        )

    def test_multiple_matches(self, client):
        client.get.return_value = Response(
            200,
            '{"result": [{"property": "something", "sys_id": "1234"}, {"property": "something", "sys_id": "4444"}]}',
            {"X-Total-Count": "2"},
        )
        client.request_binary.side_effect = [
            Response(200, "file_content1", {"X-Total-Count": "1"}),
            Response(200, "file_content2", {"X-Total-Count": "1"}),
        ]
        a = attachment.AttachmentClient(client)

        record = a.list_full_records()

        assert [
            {"property": "something", "sys_id": "1234", "data": "file_content1"},
            {"property": "something", "sys_id": "4444", "data": "file_content2"},
        ] == record
        client.get.assert_called_with(
            "attachment",
            query=dict(
                sysparm_limit=10000,
                sysparm_offset=0,
            ),
        )
        client.request_binary.assert_called_with(
            "GET", "attachment/4444/file", "*/*", accept_type="*/*"
        )

    def test_no_matches(self, client):
        client.get.return_value = Response(
            200,
            '{"result": []}',
            {"X-Total-Count": "1"},
        )
        a = attachment.AttachmentClient(client)

        record = a.list_full_records()

        assert [] == record
        client.get.assert_called_with(
            "attachment",
            query=dict(
                sysparm_limit=10000,
                sysparm_offset=0,
            ),
        )
        client.request_binary.assert_not_called()

    def test_query_matches(self, client):
        client.get.return_value = Response(
            200,
            '{"result": []}',
            {"X-Total-Count": "1"},
        )
        a = attachment.AttachmentClient(client)

        record = a.list_full_records(file_dict_list=FILE_DICT_LIST)

        assert [] == record
        client.get.assert_called_with(
            "attachment",
            query=dict(
                file_name="attachment_name^ORanother_file_name",
                sysparm_limit=10000,
                sysparm_offset=0,
            ),
        )
        client.request_binary.assert_not_called()


class TestAttachmentCreateRecord:
    def test_normal_mode(self, client):
        client.request_binary.return_value = Response(
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
        client.request_binary.assert_called_with(
            "POST",
            "attachment/file",
            "text/plain",
            bin_data="file_content",
            payload={"some": "property"},
        )

    def test_check_mode(self, client):
        client.request_binary.return_value = Response(
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
        client.request_binary.assert_not_called()


class TestAttachmentUploadRecord:
    def test_normal_mode(self, client):
        client.request_binary.return_value = Response(
            201, '{"result": {"a": 3, "b": "sys_id"}}'
        )
        a = attachment.AttachmentClient(client)

        fd, path = mkstemp()
        with os.fdopen(fd, "w") as f:
            f.write("file_content")
        mfd = FILE_DICT.copy()
        mfd.update({"path": path})

        record = a.upload_record(dict(some="property"), mfd, check_mode=False)

        assert dict(a=3, b="sys_id") == record
        client.request_binary.assert_called_with(
            "POST",
            "attachment/file",
            "text/markdown",
            bin_data=b"file_content",
            payload={
                "some": "property",
                "file_name": "attachment_name",
            },
        )

    def test_normal_mode_passing_encryption_context(self, client):
        client.request_binary.return_value = Response(
            201, '{"result": {"a": 3, "b": "sys_id"}}'
        )
        a = attachment.AttachmentClient(client)

        fd, path = mkstemp()
        with os.fdopen(fd, "w") as f:
            f.write("file_content")
        mfd = FILE_DICT.copy()
        mfd.update({"path": path, "encryption_context": "context"})

        record = a.upload_record(dict(some="property"), mfd, check_mode=False)

        assert dict(a=3, b="sys_id") == record
        client.request_binary.assert_called_with(
            "POST",
            "attachment/file",
            "text/markdown",
            bin_data=b"file_content",
            payload={
                "some": "property",
                "file_name": "attachment_name",
                "encryption_context": "context",
            },
        )

    def test_check_mode(self, client):
        client.request_binary.return_value = Response(
            201, '{"result": {"a": 3, "b": "sys_id"}}'
        )
        a = attachment.AttachmentClient(client)

        record = a.upload_record(dict(some="property"), FILE_DICT, check_mode=True)

        assert (
            dict(
                some="property",
                file_name="attachment_name",
            )
            == record
        )
        client.request_binary.assert_not_called()


class TestAttachmentUploadRecords:
    def test_normal_mode(self, client):
        client.request_binary.side_effect = [
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

        mfdl = list(FILE_DICT_LIST)
        mfdl[0].update({"path": path1})
        mfdl[1].update({"path": path2})

        record = a.upload_records(dict(some="property"), mfdl, check_mode=False)

        assert [dict(a=3, b="sys_id"), dict(a=4, b="sys_idn")] == record
        assert 2 == client.request_binary.call_count
        client.request_binary.assert_any_call(
            "POST",
            "attachment/file",
            "text/markdown",
            bin_data=b"file_content1",
            payload={
                "some": "property",
                "file_name": "attachment_name",
            },
        )
        client.request_binary.assert_any_call(
            "POST",
            "attachment/file",
            "text/plain",
            bin_data=b"file_content2",
            payload={
                "some": "property",
                "file_name": os.path.splitext(os.path.basename(path2))[0],
            },
        )

    def test_check_mode(self, client):
        client.request_binary.side_effect = [
            Response(201, '{"result": {"a": 3, "b": "sys_id"}}'),
            Response(201, '{"result": {"a": 4, "b": "sys_idn"}}'),
        ]
        a = attachment.AttachmentClient(client)

        mfdl = list(FILE_DICT_LIST)
        mfdl[1].update({"path": "some/path/to/file.txt"})

        record = a.upload_records(dict(some="property"), mfdl, check_mode=True)

        assert [
            dict(
                some="property",
                file_name="attachment_name",
            ),
            dict(
                some="property",
                file_name="file",
            ),
        ] == record
        client.request_binary.assert_not_called()


class TestAttachmentDeleteRecord:
    def test_normal_mode(self, client):
        client.delete.return_value = Response(204, "")
        a = attachment.AttachmentClient(client)
        a.delete_record(dict(sys_id="1234"), False)

        client.delete.assert_called_with("attachment/1234")

    def test_normal_mode_missing_ignore(self, client):
        a = attachment.AttachmentClient(client)
        record = a.delete_record(None, False, True)

        assert {"changed": False, "msg": "Skipped. Record doesn't exist."} == record

    def test_normal_mode_missing(self, client):
        client.delete.side_effect = errors.UnexpectedAPIResponse(404, "")
        a = attachment.AttachmentClient(client)

        assert a.delete_record(dict(sys_id="1234"), False) == {"changed": False}

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

        a.delete_attached_records(dict(table_name="table", table_sys_id=5555), False)

        assert client.delete.call_count == 2
        client.delete.assert_any_call("attachment/1234")
        client.delete.assert_any_call("attachment/4321")

    def test_normal_mode_missing(self, client):
        client.get.return_value = Response(
            200,
            '{"result": [{"a": 3, "sys_id": "1234"}, {"a": 4, "sys_id": "4321"}]}',
            {"X-Total-Count": "2"},
        )
        client.delete.side_effect = errors.UnexpectedAPIResponse(404, "")
        a = attachment.AttachmentClient(client)

        assert a.delete_attached_records(
            dict(table_name="table", table_sys_id=5555), False
        ) == [{"changed": False}, {"changed": False}]

    def test_check_mode(self, client):
        client.get.return_value = Response(
            200,
            '{"result": [{"a": 3, "sys_id": "1234"}, {"a": 4, "sys_id": "4321"}]}',
            {"X-Total-Count": "2"},
        )
        client.delete.return_value = Response(204, "")
        a = attachment.AttachmentClient(client)

        a.delete_attached_records(dict(table_name="table", table_sys_id=5555), True)
        client.delete.assert_not_called()


class TestAttachmentIsChanged:
    def test_unchanged(self, client):
        client.get.return_value = Response(
            200,
            '{"result": [{"hash": "76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff", "b": "sys_id"}]}',
            {"X-Total-Count": "1"},
        )
        a = attachment.AttachmentClient(client)

        fd, path = mkstemp()
        with os.fdopen(fd, "w") as f:
            f.write("file_content")

        mfd = FILE_DICT.copy()
        mfd.update({"path": path})

        assert not a.is_changed(dict(some="payload"), mfd)

    def test_changed(self, client):
        client.get.return_value = Response(
            200,
            '{"result": [{"hash": "76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff", "b": "sys_id"}]}',
            {"X-Total-Count": "1"},
        )
        a = attachment.AttachmentClient(client)

        fd, path = mkstemp()
        with os.fdopen(fd, "w") as f:
            f.write("file_contents")

        mfd = FILE_DICT.copy()
        mfd.update({"path": path})

        assert a.is_changed(dict(some="payload"), mfd)


class TestAttachmentAreChanged:
    def test_unchanged(self, client):
        client.get.side_effect = [
            Response(
                200,
                '{"result": [{"hash": "76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff"}]}',
                {"X-Total-Count": "1"},
            ),
            Response(
                200,
                '{"result": [{"hash": "3d849a08ee8758d7b66cc9d62b21059ac07e897084933f4c3c66f4583b5f8c94"}]}',
                {"X-Total-Count": "1"},
            ),
        ]
        a = attachment.AttachmentClient(client)

        fd1, path1 = mkstemp()
        with os.fdopen(fd1, "w") as f:
            f.write("file_content")
        fd2, path2 = mkstemp()
        with os.fdopen(fd2, "w") as f:
            f.write("another_file_content")

        mfdl = list(FILE_DICT_LIST)
        mfdl[0].update({"path": path1})
        mfdl[1].update({"path": path2})

        assert a.are_changed(dict(some="payload"), mfdl) == [False, False]

    def test_changed(self, client):
        client.get.side_effect = [
            Response(
                200,
                '{"result": [{"hash": "76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff"}]}',
                {"X-Total-Count": "1"},
            ),
            Response(
                200,
                '{"result": [{"hash": "3d849a08ee8758d7b66cc9d62b21059ac07e897084933f4c3c66f4583b5f8c94"}]}',
                {"X-Total-Count": "1"},
            ),
        ]
        a = attachment.AttachmentClient(client)

        fd1, path1 = mkstemp()
        with os.fdopen(fd1, "w") as f:
            f.write("file_contents")
        fd2, path2 = mkstemp()
        with os.fdopen(fd2, "w") as f:
            f.write("another_file_contents")

        mfdl = list(FILE_DICT_LIST)
        mfdl[0].update({"path": path1})
        mfdl[1].update({"path": path2})

        assert a.are_changed(dict(some="payload"), mfdl) == [True, True]


class TestAttachmentUpdateRecord:
    def test_unchanged_normal_mode(self, client):
        client.get.return_value = Response(
            200,
            '{"result": [{"hash": "76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff", "b": "sys_id"}]}',
            {"X-Total-Count": "1"},
        )
        a = attachment.AttachmentClient(client)

        fd, path = mkstemp()
        with os.fdopen(fd, "w") as f:
            f.write("file_content")

        mfd = FILE_DICT.copy()
        mfd.update({"path": path})

        assert {
            "changed": False,
            "msg": "Skipped. Hash matches remote.",
            "hash": "76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff",
            "b": "sys_id",
        } == a.update_record(dict(some="payload"), mfd)

    def test_changed_normal_mode(self, client):
        client.get.return_value = Response(
            200,
            '{"result": [{"hash": "76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff", "sys_id": "b"}]}',
            {"X-Total-Count": "1"},
        )
        client.request_binary.return_value = Response(
            201, '{"result": {"a": 3, "sys_id": "b"}}'
        )
        client.delete.return_value = Response(204, "")
        a = attachment.AttachmentClient(client)

        fd, path = mkstemp()
        with os.fdopen(fd, "w") as f:
            f.write("file_contents")

        mfd = FILE_DICT.copy()
        mfd.update({"path": path})

        assert {
            "changed": True,
            "msg": "Changes detected, hash doesn't match remote. Remote updated.",
            "a": 3,
            "sys_id": "b",
        } == a.update_record(dict(some="payload"), mfd)

    def test_unchanged_check_mode(self, client):
        client.get.return_value = Response(
            200,
            '{"result": [{"hash": "76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff", "b": "sys_id"}]}',
            {"X-Total-Count": "1"},
        )
        a = attachment.AttachmentClient(client)

        fd, path = mkstemp()
        with os.fdopen(fd, "w") as f:
            f.write("file_content")

        mfd = FILE_DICT.copy()
        mfd.update({"path": path})

        assert {
            "changed": False,
            "msg": "Skipped. Hash matches remote.",
            "hash": "76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff",
            "b": "sys_id",
        } == a.update_record(dict(some="payload"), mfd, True)

    def test_changed_check_mode(self, client):
        client.get.return_value = Response(
            200,
            '{"result": [{"hash": "76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff", "sys_id": "b"}]}',
            {"X-Total-Count": "1"},
        )
        client.request_binary.return_value = Response(
            201, '{"result": {"a": 3, "sys_id": "b"}}'
        )
        client.delete.return_value = Response(204, "")
        a = attachment.AttachmentClient(client)

        fd, path = mkstemp()
        with os.fdopen(fd, "w") as f:
            f.write("file_contents")

        mfd = FILE_DICT.copy()
        mfd.update({"path": path})

        assert {
            "changed": True,
            "msg": "Changes detected, hash doesn't match remote. Remote updated.",
            "some": "payload",
            "file_name": "attachment_name",
        } == a.update_record(dict(some="payload"), mfd, True)


class TestAttachmentUpdateRecords:
    def test_unchanged_normal_mode(self, client):
        rone = Response(
            200,
            '{"result": [{"hash": "76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff", "b": "sys_id"}]}',
            {"X-Total-Count": "1"},
        )
        rtwo = Response(
            200,
            '{"result": [{"hash": "3d849a08ee8758d7b66cc9d62b21059ac07e897084933f4c3c66f4583b5f8c94"}]}',
            {"X-Total-Count": "1"},
        )
        client.get.side_effect = [rone, rone, rtwo, rtwo]
        a = attachment.AttachmentClient(client)

        fd1, path1 = mkstemp()
        with os.fdopen(fd1, "w") as f:
            f.write("file_content")
        fd2, path2 = mkstemp()
        with os.fdopen(fd2, "w") as f:
            f.write("another_file_content")

        mfdl = list(FILE_DICT_LIST)
        mfdl[0].update({"path": path1})
        mfdl[1].update({"path": path2})

        assert [
            {
                "changed": False,
                "msg": "Skipped. Hash matches remote.",
                "hash": "76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff",
                "b": "sys_id",
            },
            {
                "changed": False,
                "msg": "Skipped. Hash matches remote.",
                "hash": "3d849a08ee8758d7b66cc9d62b21059ac07e897084933f4c3c66f4583b5f8c94",
            },
        ] == a.update_records(dict(some="payload"), mfdl)

    def test_changed_normal_mode(self, client):
        rone = Response(
            200,
            '{"result": [{"hash": "76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff", "sys_id": "a"}]}',
            {"X-Total-Count": "1"},
        )
        rtwo = Response(
            200,
            '{"result": [{"hash": "3d849a08ee8758d7b66cc9d62b21059ac07e897084933f4c3c66f4583b5f8c94", "sys_id": "b"}]}',
            {"X-Total-Count": "1"},
        )
        client.get.side_effect = [rone, rone, rtwo, rtwo]
        client.request_binary.side_effect = [
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

        mfdl = list(FILE_DICT_LIST)
        mfdl[0].update({"path": path1})
        mfdl[1].update({"path": path2})

        assert [
            {
                "changed": True,
                "msg": "Changes detected, hash doesn't match remote. Remote updated.",
                "a": 1,
                "sys_id": "a",
            },
            {
                "changed": True,
                "msg": "Changes detected, hash doesn't match remote. Remote updated.",
                "a": 2,
                "sys_id": "b",
            },
        ] == a.update_records(dict(some="payload"), mfdl)

    def test_unchanged_check_mode(self, client):
        rone = Response(
            200,
            '{"result": [{"hash": "76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff", "b": "sys_id"}]}',
            {"X-Total-Count": "1"},
        )
        rtwo = Response(
            200,
            '{"result": [{"hash": "3d849a08ee8758d7b66cc9d62b21059ac07e897084933f4c3c66f4583b5f8c94"}]}',
            {"X-Total-Count": "1"},
        )
        client.get.side_effect = [rone, rone, rtwo, rtwo]
        a = attachment.AttachmentClient(client)

        fd1, path1 = mkstemp()
        with os.fdopen(fd1, "w") as f:
            f.write("file_content")
        fd2, path2 = mkstemp()
        with os.fdopen(fd2, "w") as f:
            f.write("another_file_content")

        mfdl = list(FILE_DICT_LIST)
        mfdl[0].update({"path": path1})
        mfdl[1].update({"path": path2})

        assert [
            {
                "changed": False,
                "msg": "Skipped. Hash matches remote.",
                "hash": "76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff",
                "b": "sys_id",
            },
            {
                "changed": False,
                "msg": "Skipped. Hash matches remote.",
                "hash": "3d849a08ee8758d7b66cc9d62b21059ac07e897084933f4c3c66f4583b5f8c94",
            },
        ] == a.update_records(dict(some="payload"), mfdl, True)

    def test_changed_check_mode(self, client):
        rone = Response(
            200,
            '{"result": [{"hash": "76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff", "sys_id": "a"}]}',
            {"X-Total-Count": "1"},
        )
        rtwo = Response(
            200,
            '{"result": [{"hash": "3d849a08ee8758d7b66cc9d62b21059ac07e897084933f4c3c66f4583b5f8c94", "sys_id": "b"}]}',
            {"X-Total-Count": "1"},
        )
        client.get.side_effect = [rone, rone, rtwo, rtwo]
        client.request_binary.side_effect = [
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

        mfdl = list(FILE_DICT_LIST)
        mfdl[0].update({"path": path1})
        mfdl[1].update({"path": path2})

        assert [
            {
                "changed": True,
                "msg": "Changes detected, hash doesn't match remote. Remote updated.",
                "some": "payload",
                "file_name": "attachment_name",
            },
            {
                "changed": True,
                "msg": "Changes detected, hash doesn't match remote. Remote updated.",
                "some": "payload",
                "file_name": os.path.splitext(os.path.basename(path2))[0],
            },
        ] == a.update_records(dict(some="payload"), mfdl, True)