import pathlib

import pytest

from renameit.core.models import FileObject
from renameit.file_systems.local import FileSystemLocal

SOURCE_DIR = "source_files"
TARGET_DIR = "target_files"


@pytest.fixture
def create_sample_files():
    for file in ["file.txt", "subfolder/file.txt"]:
        p = pathlib.Path(SOURCE_DIR) / file
        p.parent.mkdir()
        p.touch()


@pytest.mark.usefixtures("cleandir", "create_sample_files")
class TestFileSystemLocal:
    """TestFileSystemLocal."""

    fs_local = FileSystemLocal(source_dir=SOURCE_DIR, target_dir=TARGET_DIR)

    def test_list_objects(self):
        file_objects = self.fs_local.list_objects()
        assert [obj.path for obj in file_objects] == ["file.txt"]
        self.fs_local.recursive = True
        file_objects = self.fs_local.list_objects()
        assert [obj.path for obj in file_objects] == ["file.txt", "subfolder/file.txt"]

    @pytest.mark.parametrize(
        "source_obj,target_obj",
        [
            (FileObject("file.txt"), FileObject("file_renamed.txt")),
            (FileObject("subfolder/file.txt"), FileObject("subfolder/file_renamed.txt")),
        ],
    )
    def test_rename_object(self, source_obj, target_obj):
        self.fs_local.rename_object(source_obj=source_obj, target_obj=target_obj)
        assert [
            str(p.relative_to(TARGET_DIR)) for p in pathlib.Path(TARGET_DIR).rglob("*.txt")
        ] == [target_obj.path]
        assert source_obj.path not in [
            str(p.relative_to(SOURCE_DIR)) for p in pathlib.Path(SOURCE_DIR).rglob("*.txt")
        ]

    @pytest.mark.parametrize(
        "source_obj,target_obj",
        [
            (FileObject("file.txt"), FileObject("file_copied.txt")),
            (FileObject("subfolder/file.txt"), FileObject("subfolder/file_copied.txt")),
        ],
    )
    def test_copy_object(self, source_obj, target_obj):
        self.fs_local.copy_object(source_obj=source_obj, target_obj=target_obj)
        assert [
            str(p.relative_to(TARGET_DIR)) for p in pathlib.Path(TARGET_DIR).rglob("*.txt")
        ] == [target_obj.path]
        assert source_obj.path in [
            str(p.relative_to(SOURCE_DIR)) for p in pathlib.Path(SOURCE_DIR).rglob("*.txt")
        ]
