"""BasicHandler"""

import pathlib

from renameit.core.models import FileObject
from renameit.handlers.interfaces import IHandler


# BasicHandler # noqa
class BasicHandler(IHandler):
    """Basic file name manipulation.

    Args:
        method (str): Specify how to modify the file name. Accepted values are
            (`add_prefix, add_suffix, remove_prefix, remove_suffix`).
        value (str): Value to add or remove from the file name.
    """

    name = "basic"

    def __init__(self, method: str, value: str):

        super().__init__()

        if method not in ["add_prefix", "add_suffix", "remove_prefix", "remove_suffix"]:
            raise ValueError(f"method: '{method}' is not supported.")

        self.method = method
        self.value = value

    def get_new_name(self, file_obj: FileObject) -> FileObject:
        path = pathlib.Path(file_obj.path)
        return FileObject(
            path=str(
                {
                    "add_prefix": path.with_name(self.value + path.name),
                    "add_suffix": path.with_name(path.stem + self.value + path.suffix),
                    "remove_prefix": path.with_name(path.name.removeprefix(self.value)),
                    "remove_suffix": path.with_name(
                        path.stem.removesuffix(self.value) + path.suffix
                    ),
                }[self.method]
            ),
            modified_date=file_obj.modified_date,
        )
