"""RegexHandler"""

import re

from renameit.core.models import FileObject
from renameit.handlers.interfaces import IHandler


# RegexHandler # noqa
class RegexHandler(IHandler):
    """Manipulate file paths using regular expressions.

    It works by using matching pattern with named groups and then using those groups
    into a replacement string template passed on to the re.sub method.

    Example:
    ```
    match_pattern = r"(?P<year>\\d+)/(?P<month>\\d+)/(?P<day>\\d+)/(?P<file_name>.*)".
    replace_pattern = "year=\\g<year>/month=\\g<month>/day=\\g<day>/\\g<file_name>".
    transforms "2022/01/01/file1.csv" to "year=2022/month=01/day=01/file1.csv".
    ```

    Args:
        match_pattern (str): Regular expressiong with named capturing groups.
        replace_pattern (str): String that contains the named replacement syntax for the
                            caught named groups if there is a match.
        case_sensitive (bool, optional): Applies case sensitive matching. Defaults to True.
    """

    name = "regex"

    def __init__(self, match_pattern: str, replace_pattern: str, case_sensitive: bool = True):

        super().__init__()

        self.match_pattern = match_pattern
        self.replace_pattern = replace_pattern
        self.case_sensitive = case_sensitive

        if case_sensitive:
            self.match_pattern_compiled = re.compile(match_pattern, re.IGNORECASE)
        else:
            self.match_pattern_compiled = re.compile(match_pattern)

    def get_new_name(self, file_obj: FileObject) -> FileObject:
        return FileObject(
            path=self.match_pattern_compiled.sub(self.replace_pattern, file_obj.path),
            modified_date=file_obj.modified_date,
        )
