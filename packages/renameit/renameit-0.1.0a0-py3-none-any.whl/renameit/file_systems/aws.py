from typing import Iterable

import boto3

from renameit.core.exceptions import TargetContainerNotExistError
from renameit.core.models import FileObject
from renameit.core.util import add_slash
from renameit.file_systems.interfaces import IFileSystem


class FileSystemAwsS3(IFileSystem):
    """Manage files on aws s3.

    Args:
        source_bucket (str): Name of bucket that contains the original files.
        target_bucket (str, optional): Name of bucket that should contain the new files.
            If bucket does not already exist an error will be raised, it will not
            be created automatically. Defaults to be the same as source_bucket.
        source_dir (str, optional): Directory path from where to start looking for files.
            If not provided defaults to source_bucket root.
        target_dir (str, optional): Directory path to where should the new files be written.
            If not provided defaults to target_bucket root.
        recursive (bool, optional): Decides whether to look for files recursively.
            Defaults to True.
        aws_access_key_id (str, optional): The access key to use when creating
            the s3 resource. If not provided, the credentials configured for the session
            will be used.
        aws_secret_access_key (str, optional): The secret key to use when creating
            the s3 resource. Same semantics as aws_access_key_id above.
        region_name (str, optional):  The name of the region associated with the resource.
            If not provided, it will be obtained from the default boto3 session.
    """

    name = "aws_s3"

    def __init__(
        self,
        source_bucket: str,
        target_bucket: str = None,
        source_dir: str = None,
        target_dir: str = None,
        recursive: bool = False,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        region_name: str = None,
    ):
        super().__init__()

        self.source_bucket = source_bucket
        self.target_bucket = target_bucket or source_bucket
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.recursive = recursive
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name or boto3.session.Session().region_name

        self.s3 = boto3.resource(
            "s3",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name,
        )

        self.s3_client = self.s3.meta.client

        # TODO try to create it with the same configs as source_bucket
        # or using some user input.
        if self.s3.Bucket(self.target_bucket).creation_date is None:
            raise TargetContainerNotExistError(
                f"Target bucket `{self.target_bucket}` does not exist "
                + "or you do not have enough permissions to access it."
            )

    @property
    def source_dir(self):
        return self._source_dir

    @source_dir.setter
    def source_dir(self, value):
        self._source_dir = add_slash(value)

    @property
    def target_dir(self):
        return self._target_dir

    @target_dir.setter
    def target_dir(self, value):
        self._target_dir = add_slash(value)

    def list_objects(self) -> Iterable[FileObject]:
        continuation_token = None
        kwargs = {
            "Bucket": self.source_bucket,
            "Prefix": self.source_dir,
            "StartAfter": self.source_dir,
        }

        # This will group all subdirectories in the response's CommonPrefixes
        # thus, their files will not be included in the reponse's Content.
        if not self.recursive:
            kwargs["Delimiter"] = "/"

        while True:

            if continuation_token:
                kwargs["ContinuationToken"] = continuation_token

            response = self.s3_client.list_objects_v2(**kwargs)

            for obj in response["Contents"]:
                yield FileObject(
                    path=obj["Key"].removeprefix(self.source_dir),
                    modified_date=obj["LastModified"],
                )

            if response["IsTruncated"]:
                continuation_token = response["NextContinuationToken"]
            else:
                break

    def copy_object(self, source_obj: FileObject, target_obj: FileObject) -> None:
        print(self.source_dir + source_obj.path, "->", self.target_dir + target_obj.path)

        copy_source = {"Bucket": self.source_bucket, "Key": self.source_dir + source_obj.path}
        s3_target_bucket = self.s3.Bucket(self.target_bucket)
        s3_target_bucket.copy(copy_source, self.target_dir + target_obj.path)
