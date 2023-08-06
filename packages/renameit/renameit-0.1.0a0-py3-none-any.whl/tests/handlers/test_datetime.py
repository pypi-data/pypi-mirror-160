from datetime import datetime

import pytest

from renameit.core.models import FileObject
from renameit.handlers.datetime import DateTimeHandler


class TestBasicHandler:
    @pytest.mark.parametrize(
        "dt_value,dt_format,add_as,old_file_object,expected_new_path",
        [
            (
                "modification_date",
                "%Y-%m-%d_",
                "prefix",
                FileObject("file.txt", modified_date=datetime(year=2022, month=1, day=1)),
                "2022-01-01_file.txt",
            ),
            (
                "modification_date",
                "_%Y-%m-%d",
                "suffix",
                FileObject("file.txt", modified_date=datetime(year=2022, month=1, day=1)),
                "file_2022-01-01.txt",
            ),
            (
                "now",
                "%Y-%m-%d_",
                "prefix",
                FileObject("file.txt", modified_date=datetime.utcnow()),
                f"{datetime.utcnow().date()}_file.txt",
            ),
            (
                "now",
                "_%Y-%m-%d",
                "suffix",
                FileObject("file.txt", modified_date=datetime.utcnow()),
                f"file_{datetime.utcnow().date()}.txt",
            ),
            pytest.param(
                "UNSUPPORTED_METHOD",
                "%Y-%m-%d_",
                "prefix",
                FileObject("file.txt"),
                "file.txt",
                marks=pytest.mark.xfail,
            ),
        ],
    )
    def test_get_new_name(self, dt_value, dt_format, add_as, old_file_object, expected_new_path):
        handler = DateTimeHandler(dt_value=dt_value, dt_format=dt_format, add_as=add_as)
        new_file_object = handler.get_new_name(old_file_object)
        assert expected_new_path == new_file_object.path
