import pathlib
from datetime import datetime
from typing import Optional

from renameit.core.models import FileObject
from renameit.handlers.interfaces import IHandler


class DateTimeHandler(IHandler):
    """Add datetime values to file names.

    Args:
        dt_value (str): Specify where to get date & time values from:

            - `modification_date` uses the file's latest modification datetime
            - `now` uses the current utc datetime

        dt_format (str): How to format the `dt_value` when placing it in the file name.
            Refer to https://strftime.org/ for more info about accepted format directives.
        add_as (str): Where to add `dt_value` in the file name.
            Either "prefix" or "suffix".
    """

    name = "datetime"

    def __init__(self, dt_value: str, dt_format: str, add_as: str):

        super().__init__()

        if dt_value not in ["modification_date", "now"]:
            raise ValueError(
                f"Wrong value `{dt_value}` provided in `dt_value`, "
                + "should be either `now` or `modification_date`."
            )

        if add_as not in ["prefix", "suffix"]:
            raise ValueError(
                f"Wrong value `{add_as}` provided in `add_as`, "
                + "should be either `prefix` or `suffix`."
            )

        self.dt: Optional[datetime] = datetime.utcnow()
        self.dt_value = dt_value
        self.dt_format = dt_format
        self.add_as = add_as

    def get_new_name(self, file_obj: FileObject) -> FileObject:
        path = pathlib.Path(file_obj.path)

        if self.dt_value == "modification_date":
            self.dt = file_obj.modified_date

        if self.dt is not None:
            return FileObject(
                path=str(
                    {
                        "prefix": path.with_name(self.dt.strftime(self.dt_format) + path.name),
                        "suffix": path.with_name(
                            path.stem + self.dt.strftime(self.dt_format) + path.suffix
                        ),
                    }[self.add_as]
                ),
                modified_date=file_obj.modified_date,
            )
        else:
            return file_obj
