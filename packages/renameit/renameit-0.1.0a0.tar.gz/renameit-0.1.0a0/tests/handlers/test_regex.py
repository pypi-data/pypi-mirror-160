import pytest

from renameit.core.models import FileObject
from renameit.handlers.regex import RegexHandler


class TestRegexHandler:
    @pytest.mark.parametrize(
        "match_pattern,replace_pattern,case_sensitive,old_file_object,expected_new_path",
        [
            (
                r"(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<file_name>.*)",
                r"year=\g<year>/month=\g<month>/day=\g<day>/\g<file_name>",
                True,
                FileObject("2022/01/01/file.txt"),
                "year=2022/month=01/day=01/file.txt",
            ),
            (
                r"year=(?P<year>\d+)/month=(?P<month>\d+)/day=(?P<day>\d+)/(?P<file_name>.*)",
                r"\g<year>/\g<month>/\g<day>/\g<file_name>",
                True,
                FileObject("year=2022/month=01/day=01/file.txt"),
                "2022/01/01/file.txt",
            ),
            (
                r"year=(?P<year>\d+)/month=(?P<month>\d+)/day=(?P<day>\d+)/(?P<file_name>.*)",
                r"\g<year>/\g<month>/\g<day>/\g<file_name>",
                False,
                FileObject("YEAR=2022/MONTH=01/DAY=01/file.txt"),
                "YEAR=2022/MONTH=01/DAY=01/file.txt",
            ),
        ],
    )
    def test_get_new_name(
        self, match_pattern, replace_pattern, case_sensitive, old_file_object, expected_new_path
    ):
        handler = RegexHandler(
            match_pattern=match_pattern,
            replace_pattern=replace_pattern,
            case_sensitive=case_sensitive,
        )
        new_file_object = handler.get_new_name(old_file_object)
        assert expected_new_path == new_file_object.path
