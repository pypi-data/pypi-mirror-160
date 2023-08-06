import os
import uuid

import pytest
from azure.storage.filedatalake import DataLakeServiceClient

from renameit.core.models import FileObject
from renameit.file_systems.azure import FileSystemAzureDatalakeStorage

__TEST_ENV_VAR__ = "TEST_AZURE_CONN_STRING"

FILES = ["file1.txt", "folder/file2.txt", "folder/subfolder/file3.txt"]

RUN_ID = uuid.uuid4().hex
SOURCE_CONTAINER = f"renameit-source-pytest-{RUN_ID}"
TARGET_CONTAINER = f"renameit-target-pytest-{RUN_ID}"


@pytest.fixture(scope="class")
def conn_string():
    return os.environ[__TEST_ENV_VAR__]


@pytest.fixture(scope="class")
def service_client(conn_string):
    return DataLakeServiceClient.from_connection_string(conn_string)


@pytest.fixture(scope="class")
def setup(service_client, request):
    sampe_data = b"Sample data"

    fs_client = service_client.get_file_system_client(SOURCE_CONTAINER)
    fs_client.create_file_system()

    for file_path in FILES:
        file_client = fs_client.create_file(file_path)
        file_client.append_data(data=sampe_data, offset=0, length=len(sampe_data))
        file_client.flush_data(len(sampe_data))

    def teardown():
        for file_system_name in [SOURCE_CONTAINER, TARGET_CONTAINER]:
            file_system = service_client.get_file_system_client(file_system_name)
            if file_system.exists():
                file_system.delete_file_system()

    request.addfinalizer(teardown)


@pytest.fixture()
def filesystem(conn_string, request):
    """Initializes a filesystem with the right params."""

    # Fixed params as there is no need for these to be variable
    params = {
        "source_container": SOURCE_CONTAINER,
        "target_container": TARGET_CONTAINER,
        "connection_string": conn_string,
    }

    # This allows tests functions or other fixtures to parametarize the
    # creation of filesystem instance.
    # Input params are parsed here if parametrization was defined.
    for arg in {
        "source_dir",
        "target_dir",
        "recursive",
    }:
        params[arg] = getattr(request, "param", {}).get(arg, None)

    return FileSystemAzureDatalakeStorage(**params)


@pytest.mark.skipif(
    not os.environ.get(__TEST_ENV_VAR__),
    reason=f"Env var {__TEST_ENV_VAR__} was not found",
)
@pytest.mark.usefixtures("setup")
class TestAzureDatalakeStorage:
    """TestAzureDatalakeStorage."""

    @pytest.mark.parametrize(
        ["filesystem", "expected_list_result"],
        [
            ({"recursive": False}, ["file1.txt"]),
            ({"recursive": True}, FILES),
            ({"source_dir": "folder", "recursive": False}, ["file2.txt"]),
            ({"source_dir": "folder", "recursive": True}, ["file2.txt", "subfolder/file3.txt"]),
        ],
        indirect=["filesystem"],
    )
    def test_list_objects(self, filesystem, expected_list_result):
        file_objects = filesystem.list_objects()
        assert [obj.path for obj in file_objects] == expected_list_result

    @pytest.mark.parametrize(
        ["source_obj", "target_obj"],
        [
            (FileObject("file1.txt"), FileObject("renamed/file1.txt")),
            (FileObject("folder/file2.txt"), FileObject("renamed/folder/file2.txt")),
        ],
    )
    def test_rename_object(self, service_client, filesystem, source_obj, target_obj):
        filesystem.rename_object(source_obj, target_obj)
        assert (
            not service_client.get_file_system_client(SOURCE_CONTAINER)
            .get_file_client(source_obj.path)
            .exists()
        )
        assert (
            service_client.get_file_system_client(TARGET_CONTAINER)
            .get_file_client(target_obj.path)
            .exists()
        )
