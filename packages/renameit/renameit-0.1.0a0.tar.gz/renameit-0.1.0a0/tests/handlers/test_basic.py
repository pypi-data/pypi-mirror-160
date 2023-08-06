import pytest

from renameit.core.models import FileObject
from renameit.handlers.basic import BasicHandler


class TestBasicHandler:
    @pytest.mark.parametrize(
        "method,value,old_file_object,expected_new_path",
        [
            ("add_prefix", "prefix_value_", FileObject("file.txt"), "prefix_value_file.txt"),
            ("add_suffix", "_suffix_value", FileObject("file.txt"), "file_suffix_value.txt"),
            ("remove_prefix", "prefix_value_", FileObject("prefix_value_file.txt"), "file.txt"),
            ("remove_suffix", "_suffix_value", FileObject("file_suffix_value.txt"), "file.txt"),
            pytest.param(
                "UNSUPPORTED_METHOD",
                "value",
                FileObject("file.txt"),
                "file.txt",
                marks=pytest.mark.xfail,
            ),
        ],
    )
    def test_get_new_name(self, method, value, old_file_object, expected_new_path):
        handler = BasicHandler(method=method, value=value)
        new_file_object = handler.get_new_name(old_file_object)
        assert expected_new_path == new_file_object.path
