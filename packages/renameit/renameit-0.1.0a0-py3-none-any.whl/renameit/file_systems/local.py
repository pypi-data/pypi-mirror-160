import logging
import pathlib
import shutil
from datetime import datetime
from functools import wraps
from typing import Iterable

from renameit.core.models import FileObject
from renameit.file_systems.interfaces import IFileSystem


def _create_target_dirs(_fn):
    """Decorator to use on FileSystemLocal methods in order to create
    target directories if needed."""

    @wraps(_fn)
    def wrapper(self, *args, **kwargs):
        if "target_obj" in kwargs:
            (self.target_dir / kwargs["target_obj"].path).parent.mkdir(parents=True, exist_ok=True)
        return _fn(self, *args, **kwargs)

    return wrapper


# FileSystemLocal # noqa
class FileSystemLocal(IFileSystem):
    """Manage files on the local operating system.

    Args:
        source_dir (str): Source directory to iterate files from.
        target_dir (str): Target directory to copy/rename files to.
        recursive (bool, optional): Decides if listing source_dir should be recursive or not.
    """

    name = "local"

    def __init__(self, source_dir: str, target_dir: str, recursive: bool = False) -> None:

        super().__init__()

        self.source_dir = pathlib.Path(source_dir)
        self.target_dir = pathlib.Path(target_dir)
        self.recursive = recursive

    def list_objects(self) -> Iterable[FileObject]:
        if self.recursive:
            glob_method = self.source_dir.rglob
        else:
            glob_method = self.source_dir.glob

        for path in glob_method("*"):
            if path.is_file():
                yield FileObject(
                    path=str(path.relative_to(self.source_dir)),
                    modified_date=datetime.fromtimestamp((path.stat().st_mtime)),
                )

    @_create_target_dirs
    def rename_object(self, source_obj: FileObject, target_obj: FileObject) -> None:
        logging.info(
            "Renaming: "
            + str(self.source_dir / source_obj.path)
            + " to "
            + str(self.target_dir / target_obj.path)
        )

        (self.source_dir / source_obj.path).rename(self.target_dir / target_obj.path)

    @_create_target_dirs
    def copy_object(self, source_obj: FileObject, target_obj: FileObject) -> None:
        logging.info(
            "Copying: "
            + str(self.source_dir / source_obj.path)
            + " to "
            + str(self.target_dir / target_obj.path)
        )

        shutil.copy(self.source_dir / source_obj.path, self.target_dir / target_obj.path)
