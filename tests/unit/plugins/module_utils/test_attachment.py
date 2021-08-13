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


class TestAttachmentFileHash:
    def test_hash(self):
        fd, path = mkstemp()
        with os.fdopen(fd, "w") as f:
            f.write("file_content")
        assert (
            attachment.file_hash(path)
            == "76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff"
        )


class TestAttachmentGetHash:
    def test_hash(self):
        assert (
            attachment.get_hash(b"file_content")
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
            bytes="file_content"
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
                "hash": "76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff",
            },
            headers={"Accept": "application/json", "Content-type": "text/markdown"},
            bytes=b"file_content"
        )

    def test_normal_mode_passing_encryption_context(self, client):
        client.request.return_value = Response(
            201, '{"result": {"a": 3, "b": "sys_id"}}'
        )
        a = attachment.AttachmentClient(client)

        fd, path = mkstemp()
        with os.fdopen(fd, "w") as f:
            f.write("file_content")
        mfd = FILE_DICT.copy()
        mfd.update({"path": path, "encryption_context": "context"})

        record = a.upload_record("table", "1234", mfd, check_mode=False)

        assert dict(a=3, b="sys_id") == record
        client.request.assert_called_with(
            "POST",
            "attachment/file",
            query={
                "table_name": "table",
                "table_sys_id": "1234",
                "file_name": "attachment_name",
                "encryption_context": "context",
                "hash": "76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff",
            },
            headers={"Accept": "application/json", "Content-type": "text/markdown"},
            bytes=b"file_content"
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

        assert (
            dict(
                table_name="table",
                table_sys_id="1234",
                file_name="attachment_name",
                hash="76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff",
            )
            == record
        )
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

        mfdl = list(FILE_DICT_LIST)
        mfdl[0].update({"path": path1})
        mfdl[1].update({"path": path2})

        record = a.upload_records("table", "1234", mfdl, check_mode=False)

        assert [dict(a=3, b="sys_id"), dict(a=4, b="sys_idn")] == record
        assert 2 == client.request.call_count
        client.request.assert_any_call(
            "POST",
            "attachment/file",
            query={
                "table_name": "table",
                "table_sys_id": "1234",
                "file_name": "attachment_name",
                "hash": "290d3cdb3c4d8ba8cf79b84d2d59b15a6b6f350899f0aee9b8ccc52450457d7a",
            },
            headers={"Accept": "application/json", "Content-type": "text/markdown"},
            bytes=b"file_content1"
        )
        client.request.assert_any_call(
            "POST",
            "attachment/file",
            query={
                "table_name": "table",
                "table_sys_id": "1234",
                "file_name": os.path.splitext(os.path.basename(path2))[0],
                "hash": "6aba215fac895ced736daa52a9d387dfe7ced17681b91add072136891011205d",
            },
            headers={"Accept": "application/json", "Content-type": "text/plain"},
            bytes=b"file_content2"
        )

    def test_check_mode(self, client):
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

        mfdl = list(FILE_DICT_LIST)
        mfdl[0].update({"path": path1})
        mfdl[1].update({"path": path2})

        record = a.upload_records("table", "1234", mfdl, check_mode=True)

        assert [
            {
                "table_name": "table",
                "table_sys_id": "1234",
                "file_name": "attachment_name",
                "hash": "290d3cdb3c4d8ba8cf79b84d2d59b15a6b6f350899f0aee9b8ccc52450457d7a",
            },
            {
                "table_name": "table",
                "table_sys_id": "1234",
                "file_name": os.path.splitext(os.path.basename(path2))[0],
                "hash": "6aba215fac895ced736daa52a9d387dfe7ced17681b91add072136891011205d",
            },
        ] == record
        client.request.assert_not_called()

    def test_missing_file(self, client):
        a = attachment.AttachmentClient(client)
        with pytest.raises(errors.ServiceNowError, match="Cannot open {0}".format(FILE_DICT_LIST[0]["path"])):
            a.upload_records("table", "1234", FILE_DICT_LIST, True)


class TestAttachmentDeleteRecord:
    def test_normal_mode(self, client):
        client.delete.return_value = Response(204, "")
        a = attachment.AttachmentClient(client)
        a.delete_record(dict(sys_id="1234"), False)

        client.delete.assert_called_with("attachment/1234")

    def test_normal_mode_missing(self, client):
        client.delete.side_effect = errors.UnexpectedAPIResponse(404, "Record not found")
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
        client.delete.side_effect = errors.UnexpectedAPIResponse(404, "Record not found")
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

        assert not a.is_changed("table", "1234", mfd)

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

        assert a.is_changed("table", "1234", mfd)


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

        assert a.are_changed("table", "1234", mfdl) == [False, False]

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

        assert a.are_changed("table", "1234", mfdl) == [True, True]


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
        } == a.update_record("table", "1234", mfd)

    def test_changed_normal_mode(self, client):
        client.get.return_value = Response(
            200,
            '{"result": [{"hash": "76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff", "sys_id": "b"}]}',
            {"X-Total-Count": "1"},
        )
        client.request.return_value = Response(
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
        } == a.update_record("table", "1234", mfd)

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
        } == a.update_record("table", "1234", mfd, True)

    def test_changed_check_mode(self, client):
        client.get.return_value = Response(
            200,
            '{"result": [{"hash": "76951a390776ef5126f5724222c912e1bb53f546ffed0fd89a758c6dcf1619ff", "sys_id": "b"}]}',
            {"X-Total-Count": "1"},
        )
        client.request.return_value = Response(
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
            "table_name": "table",
            "table_sys_id": "1234",
            "file_name": "attachment_name",
            "hash": "bf96094e7d9020306b1b61313a7429b3b0368b992a96b673c8397c2d2a57b35b",
        } == a.update_record("table", "1234", mfd, True)


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
        ] == a.update_records("table", "1234", mfdl)

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
        ] == a.update_records("table", "1234", mfdl)

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
        ] == a.update_records("table", "1234", mfdl, True)

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

        mfdl = list(FILE_DICT_LIST)
        mfdl[0].update({"path": path1})
        mfdl[1].update({"path": path2})

        assert [
            {
                "changed": True,
                "msg": "Changes detected, hash doesn't match remote. Remote updated.",
                "table_name": "table",
                "table_sys_id": "1234",
                "file_name": "attachment_name",
                "hash": "bf96094e7d9020306b1b61313a7429b3b0368b992a96b673c8397c2d2a57b35b",
            },
            {
                "changed": True,
                "msg": "Changes detected, hash doesn't match remote. Remote updated.",
                "table_name": "table",
                "table_sys_id": "1234",
                "file_name": os.path.splitext(os.path.basename(path2))[0],
                "hash": "60e55075c46f4d8ade1c6dfbb120c87025ea8051add153f289b93438daf2c8d0",
            },
        ] == a.update_records("table", "1234", mfdl, True)
