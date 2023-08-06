import json
import os
import pathlib
import tempfile
import uuid

import pytest
from google.cloud import storage

from renameit.core.models import FileObject
from renameit.file_systems.google import FileSystemGoogleCloudStorage

__TEST_ENV_VAR__ = "TEST_GOOGLE_APPLICATION_CREDENTIALS"

FILES = ["file1.txt", "folder/file2.txt", "folder/subfolder/file3.txt"]

RUN_ID = uuid.uuid4().hex
SOURCE_BUCKET = f"renameit-source-pytest-{RUN_ID}"
TARGET_BUCKET = f"renameit-target-pytest-{RUN_ID}"


@pytest.fixture(scope="class")
def google_credentials_json():

    env_var_content = os.environ[__TEST_ENV_VAR__]

    try:
        credentials = pathlib.Path(env_var_content).read_text()
    except FileNotFoundError:

        try:
            credentials = json.loads(env_var_content, strict=False)
        except json.decoder.JSONDecodeError:
            raise ValueError(
                f"Env var {__TEST_ENV_VAR__} provided is neither a "
                + "path to valid and existing json file "
                + "nor a string representation of a json object."
            )

    with tempfile.NamedTemporaryFile(suffix=".json") as _f:
        credentials_json = pathlib.Path(_f.name)
        credentials_json.write_text(credentials)
        yield str(credentials_json)


@pytest.fixture(scope="class", autouse=True)
def google_credentials_env(google_credentials_json):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials_json


@pytest.fixture(scope="class")
def storage_client():
    return storage.Client()


@pytest.fixture(scope="class")
def setup(storage_client, request):
    sampe_data = b"Sample data"

    source_bucket = storage_client.bucket(SOURCE_BUCKET)
    target_bucket = storage_client.bucket(TARGET_BUCKET)

    if not source_bucket.exists():
        storage_client.create_bucket(source_bucket)
    if not target_bucket.exists():
        storage_client.create_bucket(target_bucket)

    with tempfile.NamedTemporaryFile() as _f:
        pathlib.Path(_f.name).write_bytes(sampe_data)
        for file_path in FILES:
            blob = source_bucket.blob(file_path)
            blob.upload_from_filename(_f.name)

    def teardown():
        for bucket_name in [SOURCE_BUCKET, TARGET_BUCKET]:
            bucket = storage_client.bucket(bucket_name)
            if bucket.exists():
                bucket.delete(force=True)

    request.addfinalizer(teardown)


@pytest.fixture()
def filesystem(request):
    """Initializes a filesystem with the right params."""

    # Fixed params as there is no need for these to be variable
    params = {
        "source_bucket": SOURCE_BUCKET,
        "target_bucket": TARGET_BUCKET,
    }

    # This allows tests functions or other fixtures to parametarize the
    # creation of filesystem instance.
    # Input params are parsed here if parametrization was defined.
    for arg in {"source_dir", "recursive"}:
        params[arg] = getattr(request, "param", {}).get(arg, None)

    return FileSystemGoogleCloudStorage(**params)


@pytest.mark.skipif(
    not os.environ.get(__TEST_ENV_VAR__),
    reason=f"Env var {__TEST_ENV_VAR__} was not found",
)
@pytest.mark.usefixtures("setup")
class TestFileSystemGoogleStorage:
    """TestFileSystemGoogleStorage."""

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
            (FileObject("file1.txt"), FileObject("copied/file1.txt")),
            (FileObject("folder/file2.txt"), FileObject("copied/folder/file2.txt")),
        ],
    )
    def test_copy_object(self, storage_client, filesystem, source_obj, target_obj):
        filesystem.copy_object(source_obj, target_obj)
        assert (
            storage_client.bucket(SOURCE_BUCKET)
            .blob(filesystem.source_dir + source_obj.path)
            .exists()
        )
        assert (
            storage_client.bucket(TARGET_BUCKET)
            .blob(filesystem.target_dir + target_obj.path)
            .exists()
        )

    @pytest.mark.parametrize(
        ["source_obj", "target_obj"],
        [
            (FileObject("file1.txt"), FileObject("renamed/file1.txt")),
            (FileObject("folder/file2.txt"), FileObject("renamed/folder/file2.txt")),
        ],
    )
    def test_rename_object(self, storage_client, filesystem, source_obj, target_obj):
        filesystem.rename_object(source_obj, target_obj)
        assert (
            not storage_client.bucket(SOURCE_BUCKET)
            .blob(filesystem.source_dir + source_obj.path)
            .exists()
        )
        assert (
            storage_client.bucket(TARGET_BUCKET)
            .blob(filesystem.target_dir + target_obj.path)
            .exists()
        )
