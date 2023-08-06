""" Module for the base handler interface."""


from abc import ABC, abstractmethod
from importlib import import_module
from typing import Optional

from renameit.core.models import FileObject
from renameit.core.util import get_implementations


class IHandler(ABC):
    """Base interface for implementing renaming handlers.

    Handler should be initialized with certain criteria for renaming file paths.
    """

    name: Optional[str] = None

    def __init__(self) -> None:
        if self.name is None:
            raise AttributeError("`name` is not defined.")

    @abstractmethod
    def get_new_name(self, file_obj: FileObject) -> FileObject:
        """Change the path of the file_obj according to the provided criteria.

        Args:
            file_obj (FileObject): File object with defined properties.

        Returns:
            FileObject: FileObject instance with modified path.
        """
        raise NotImplementedError()


handlers_map = get_implementations(import_module(__package__), IHandler)
