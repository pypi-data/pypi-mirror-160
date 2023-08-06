import os
import uuid
from io import BytesIO

import boto3
import pytest
from moto import mock_s3

from renameit.core.models import FileObject
from renameit.file_systems.aws import FileSystemAwsS3

KEYS = ["file1.txt", "folder/file2.txt", "folder/subfolder/file3.txt"]

RUN_ID = uuid.uuid4().hex
SOURCE_BUCKET = f"renameit-source-bucket-{RUN_ID}"
TARGET_BUCKET = f"renameit-target-bucket-{RUN_ID}"


@pytest.fixture(scope="class", autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-2"


@pytest.fixture(autouse=True, scope="class")
def mock_s3_context():
    """This fixture creates the moto mock context for s3"""
    mock_s3_context = mock_s3()
    mock_s3_context.start()
    yield mock_s3_context
    mock_s3_context.stop()


@pytest.fixture(scope="class")
def s3():
    """This fixture creates a mock s3 resource"""
    return boto3.resource("s3")


@pytest.fixture(scope="class")
def setup(s3):
    # Create source bucket
    s3.create_bucket(
        Bucket=SOURCE_BUCKET,
        CreateBucketConfiguration={"LocationConstraint": "us-east-2"},
    )

    # Create target bucket
    s3.create_bucket(
        Bucket=TARGET_BUCKET,
        CreateBucketConfiguration={"LocationConstraint": "us-east-2"},
    )

    # Populate source bucket
    for key in KEYS:
        with BytesIO(b"Sample data") as bytes_io:
            s3.Object(SOURCE_BUCKET, key).upload_fileobj(bytes_io)


@pytest.fixture()
def filesystem(request):
    """
    Initializes a filesystem with the right params within the context
    of the mock s3 resource.
    """

    # Fixed params as there is no need for these to be variable
    params = {"source_bucket": SOURCE_BUCKET, "target_bucket": TARGET_BUCKET}

    # This allows tests functions or other fixtures to parametarize the
    # creation of filesystem instance.
    # Input params are parsed here if parametrization was defined.
    for arg in {
        "source_dir",
        "target_dir",
        "recursive",
        "aws_access_key_id",
        "aws_secret_access_key",
    }:
        params[arg] = getattr(request, "param", {}).get(arg, None)

    return FileSystemAwsS3(**params)


@pytest.mark.usefixtures("setup")
class TestFileSystemAwsS3:
    @pytest.mark.parametrize(
        ["filesystem", "expected_list_result"],
        [
            ({"recursive": False}, ["file1.txt"]),
            ({"recursive": True}, KEYS),
            ({"source_dir": "folder", "recursive": False}, ["file2.txt"]),
            ({"source_dir": "folder", "recursive": True}, ["file2.txt", "subfolder/file3.txt"]),
            (
                {"aws_access_key_id": "test_key", "aws_secret_access_key": "test_secret"},
                ["file1.txt"],
            ),
        ],
        indirect=["filesystem"],
    )
    def test_list_objects(self, filesystem, expected_list_result):
        file_objects = filesystem.list_objects()
        assert [obj.path for obj in file_objects] == expected_list_result

    @pytest.mark.parametrize(
        ["source_obj", "target_obj"],
        [
            (FileObject("file1.txt"), FileObject("copy_of_file1.txt")),
            (FileObject("folder/file2.txt"), FileObject("folder/copy_of_file2.txt")),
        ],
    )
    def test_copy_object(self, s3, filesystem, source_obj, target_obj):
        filesystem.copy_object(source_obj, target_obj)

        # Access the mock `s3` resource in order to load
        # the original and copied keys and make sure they exist.

        # We expect the `source_obj` to exist in
        # s3://SOURCE_BUCKET/source_obj.path
        s3.Bucket(SOURCE_BUCKET).Object(source_obj.path).load()

        # We expect the `target_obj` to exist in
        # s3://TARGET_BUCKET/target_obj
        s3.Bucket(TARGET_BUCKET).Object(target_obj.path).load()
