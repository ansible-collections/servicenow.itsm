import json
import mock
import contextlib

from ansible.module_utils._text import to_bytes


@contextlib.contextmanager
def set_module_args(args=None, add_instance=True):
    """
    Context manager that sets module arguments for AnsibleModule
    """
    if args is None:
        args = {}

    if "_ansible_remote_tmp" not in args:
        args["_ansible_remote_tmp"] = "/tmp"
    if "_ansible_keep_remote_files" not in args:
        args["_ansible_keep_remote_files"] = False

    if add_instance:
        args["instance"] = dict(
            host="https://my.host.name", username="user", password="pass"
        )

    try:
        from ansible.module_utils.testing import patch_module_args
    except ImportError:
        # Before data tagging support was merged (2.19), this was the way to go:
        from ansible.module_utils import basic

        serialized_args = to_bytes(json.dumps({"ANSIBLE_MODULE_ARGS": args}))
        with mock.patch.object(basic, "_ANSIBLE_ARGS", serialized_args):
            yield
    else:
        # With data tagging support, we have a new helper for this:
        with patch_module_args(args):
            yield
