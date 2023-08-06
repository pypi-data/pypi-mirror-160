"""This module contains tests for the main cli entry point.

It uses the local file system by default, this does not mean that the local
file system is fully tested here. Look into tests/file_systems/test_local.py for full tests.

This only tries to test the main program workflow and makes sure core components are working as
expected.
"""


import json
import os
import pathlib
import tempfile

import pytest

from renameit.core.cli import renameit
from renameit.core.config.project import (
    FileSystemConfig,
    JobConfig,
    ProjectConfig,
    RenameHandlerConfig,
)

FILES = ["file1.txt", "folder/file1.txt"]
__FIXED__ = {"PREFIX": "TEST_PREFIX_", "SOURCE_DIR": "source_dir", "TARGET_DIR": "target_dir"}


@pytest.fixture(autouse=True)
def cleandir():
    with tempfile.TemporaryDirectory() as newpath:
        old_cwd = os.getcwd()
        os.chdir(newpath)
        yield
        os.chdir(old_cwd)


@pytest.fixture(autouse=True)
def create_files():
    source_dir = pathlib.Path(__FIXED__["SOURCE_DIR"])
    source_dir.mkdir()
    for file_path in FILES:
        (source_dir / pathlib.Path(file_path).parent).mkdir(parents=True, exist_ok=True)
        (source_dir / file_path).touch()


@pytest.fixture()
def config_file_path(request):
    operation = request.param.get("operation", "rename")
    file_system_config = request.param["file_system_config"]
    rename_handler_config = request.param["rename_handler_config"]

    config_file_path = pathlib.Path("config.json")
    config_file_path.write_text(
        json.dumps(
            ProjectConfig(
                jobs=[
                    JobConfig(
                        name="TEST_JOB",
                        operation=operation,
                        file_system=file_system_config,
                        rename_handler=rename_handler_config,
                    )
                ]
            ).dict(by_alias=True)
        )
    )
    return config_file_path


def _generate_test_parameters():
    return [
        # recursive local rename
        (
            # config_file_path
            {
                "operation": "rename",
                "file_system_config": FileSystemConfig(
                    type="local",
                    args={
                        "source_dir": __FIXED__["SOURCE_DIR"],
                        "target_dir": __FIXED__["TARGET_DIR"],
                        "recursive": True,
                    },
                ),
                "rename_handler_config": RenameHandlerConfig(
                    type="basic", args={"method": "add_prefix", "value": __FIXED__["PREFIX"]}
                ),
            },
            # expected_source_files
            [],
            # expected_target_files
            [
                f"{__FIXED__['TARGET_DIR']}/{__FIXED__['PREFIX']}file1.txt",
                f"{__FIXED__['TARGET_DIR']}/folder/{__FIXED__['PREFIX']}file1.txt",
            ],
        ),
        # recursive local copy
        (
            # config_file_path
            {
                "operation": "copy",
                "file_system_config": FileSystemConfig(
                    type="local",
                    args={
                        "source_dir": __FIXED__["SOURCE_DIR"],
                        "target_dir": __FIXED__["TARGET_DIR"],
                        "recursive": True,
                    },
                ),
                "rename_handler_config": RenameHandlerConfig(
                    type="basic", args={"method": "add_prefix", "value": __FIXED__["PREFIX"]}
                ),
            },
            # expected_source_files
            [__FIXED__["SOURCE_DIR"] + "/" + file for file in FILES],
            # expected_target_files
            [
                f"{__FIXED__['TARGET_DIR']}/{__FIXED__['PREFIX']}file1.txt",
                f"{__FIXED__['TARGET_DIR']}/folder/{__FIXED__['PREFIX']}file1.txt",
            ],
        ),
        # non recursive local rename
        (
            # config_file_path
            {
                "operation": "rename",
                "file_system_config": FileSystemConfig(
                    type="local",
                    args={
                        "source_dir": __FIXED__["SOURCE_DIR"],
                        "target_dir": __FIXED__["TARGET_DIR"],
                        "recursive": False,
                    },
                ),
                "rename_handler_config": RenameHandlerConfig(
                    type="basic", args={"method": "add_prefix", "value": __FIXED__["PREFIX"]}
                ),
            },
            # expected_source_files
            [f"{__FIXED__['SOURCE_DIR']}/folder/file1.txt"],
            # expected_target_files
            [
                f"{__FIXED__['TARGET_DIR']}/{__FIXED__['PREFIX']}file1.txt",
            ],
        ),
        # non recursive local copy
        (
            # config_file_path
            {
                "operation": "copy",
                "file_system_config": FileSystemConfig(
                    type="local",
                    args={
                        "source_dir": __FIXED__["SOURCE_DIR"],
                        "target_dir": __FIXED__["TARGET_DIR"],
                        "recursive": False,
                    },
                ),
                "rename_handler_config": RenameHandlerConfig(
                    type="basic", args={"method": "add_prefix", "value": __FIXED__["PREFIX"]}
                ),
            },
            # expected_source_files
            [__FIXED__["SOURCE_DIR"] + "/" + file for file in FILES],
            # expected_target_files
            [
                f"{__FIXED__['TARGET_DIR']}/{__FIXED__['PREFIX']}file1.txt",
            ],
        ),
        # non recursive local copy - regex handler
        # We are using regex handler here to force a certains use-case
        # which is making sure the new file name stays the same as old
        # and expecting it to be skipped and not cause any problems or
        # some unexpected output.
        (
            # config_file_path
            {
                "operation": "copy",
                "file_system_config": FileSystemConfig(
                    type="local",
                    args={
                        "source_dir": __FIXED__["SOURCE_DIR"],
                        "target_dir": __FIXED__["TARGET_DIR"],
                        "recursive": False,
                    },
                ),
                "rename_handler_config": RenameHandlerConfig(
                    type="regex",
                    # Make sure the args provided result in old_file and new_file to be the same
                    args={"match_pattern": r"(?P<name>\*+)", "replace_pattern": "\\g<name>"},
                ),
            },
            # expected_source_files
            [__FIXED__["SOURCE_DIR"] + "/" + file for file in FILES],
            # expected_target_files
            [],
        ),
    ]


@pytest.mark.parametrize(
    ["config_file_path", "expected_source_files", "expected_target_files"],
    _generate_test_parameters(),
    indirect=["config_file_path"],
)
def test_renameit(config_file_path, expected_source_files, expected_target_files):
    _SOURCE_DIR_ = pathlib.Path(__FIXED__["SOURCE_DIR"])
    _TARGET_DIR_ = pathlib.Path(__FIXED__["TARGET_DIR"])

    renameit(config_path=config_file_path)

    assert list(str(p) for p in _SOURCE_DIR_.glob("**/*.txt")) == expected_source_files
    assert list(str(p) for p in _TARGET_DIR_.glob("**/*.txt")) == expected_target_files
