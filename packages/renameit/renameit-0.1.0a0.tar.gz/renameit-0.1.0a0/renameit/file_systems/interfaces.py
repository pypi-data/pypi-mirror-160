"""Module for the base file system interface."""

from importlib import import_module
from typing import Iterable, Optional

from renameit.core.models import FileObject
from renameit.core.util import get_implementations


class IFileSystem:
    """Base interface for implementing file systems.

    Expose specific operations needed to carry out file renaming over a certain type of file system.

    This abstract class leaves the init args open. As initializing different file systems
    have different requirements."""

    # Class name property that will be used to reference the file system type by users.
    name: Optional[str] = None

    def __init__(self) -> None:
        if self.name is None:
            raise AttributeError("`name` is not defined.")

    def list_objects(self) -> Iterable[FileObject]:
        """List files in a container. Should return/yield a generator of FileObject.

        Path of FileObject returned should be subpath relative to its parent path. Meaning, if
        a full path is `/parent_dir/subfoler_1/file1`, return value should be `subfoler_1/file1`.

        This is to prevent any modifications to parent containers outside the scope of this class.
        """
        raise NotImplementedError()

    def rename_object(self, source_obj: FileObject, target_obj: FileObject) -> None:
        """Rename implementation.

        Delete the source object and move it to the target object.

        Args:
            source_obj (FileObject): Original object returned by self.list_objects.
            target_obj (FileObject):New object with modified path provided by a
                renaming handler.
        """
        raise NotImplementedError()

    def copy_object(self, source_obj: FileObject, target_obj: FileObject) -> None:
        """Copy implementation.

        Keep the source object and create a new copy of it as the new target object.

        Args:
            source_obj (FileObject): Original object returned by self.list_objects.
            target_obj (FileObject): New object with modified path provided by a
                renaming handler.
        """
        raise NotImplementedError()


file_systems_map = get_implementations(import_module(__package__), IFileSystem)
