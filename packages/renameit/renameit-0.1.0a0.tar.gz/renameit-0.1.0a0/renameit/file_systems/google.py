import json
import logging
from typing import Dict, Iterable, Union

from google.cloud import storage

from renameit.core.exceptions import TargetContainerNotExistError
from renameit.core.models import FileObject
from renameit.core.util import add_slash
from renameit.file_systems.interfaces import IFileSystem


class FileSystemGoogleCloudStorage(IFileSystem):
    """Manage files on google cloud storage.

    Authenticating to google cloud storage uses service account credentials
    and looks for them in the following ordered places:

    - Checks `service_account_json` argument
    - Checks `service_account_info` argument
    - Environment variable called `GOOGLE_APPLICATION_CREDENTIALS`
        that points to json file that contains the credentials

    Args:
        source_bucket (str): Name of bucket that contains the original files.
        target_bucket (str): Name of bucket that should contain the new files.
            If bucket does not already exist an error will be raised, it will not
            be created automatically. Defaults to be the same as source_bucket.
        source_dir (str, optional): Directory path from where to start looking for files.
            If not provided defaults to source_bucket root.
        target_dir (str, optional): Directory path to where should the new files be written.
            If not provided defaults to target_bucket root.
        recursive (bool, optional): Decides whether to look for files recursively.
            Defaults to True.
        service_account_json (str, optional): File path to json file that contains service
            account credentials.
        service_account_info (Union[Dict[str, str], str], optional): Service account
            credentials as dict or a string representing a json object.
    """

    name = "google_cloud_storage"

    def __init__(
        self,
        source_bucket: str,
        target_bucket: str,
        source_dir: str = None,
        target_dir: str = None,
        recursive: bool = False,
        service_account_json: str = None,
        service_account_info: Union[Dict[str, str], str] = None,
    ):
        super().__init__()
        self.source_bucket = source_bucket
        self.target_bucket = target_bucket or source_bucket
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.recursive = recursive
        self.service_account_json = service_account_json
        self.service_account_info = (
            json.loads(service_account_info)
            if type(service_account_info) is str
            else service_account_info
        )

        if self.service_account_json:
            self.storage_client = storage.Client.from_service_account_json(
                self.service_account_json
            )

        elif self.service_account_info:
            self.storage_client = self.storage_client = storage.Client.from_service_account_info(
                self.service_account_info
            )

        else:
            self.storage_client = storage.Client()

        self.source_bucket_client = self.storage_client.bucket(self.source_bucket)
        self.target_bucket_client = self.storage_client.bucket(self.target_bucket)

        # TODO try to create it with the same configs as source_bucket
        # or using some user input.
        if not self.target_bucket_client.exists():
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
        if self.recursive:
            delimiter = None
        else:
            delimiter = "/"

        blobs = self.storage_client.list_blobs(
            self.source_bucket, prefix=self.source_dir, delimiter=delimiter
        )

        for blob in blobs:
            if not blob.name.endswith("/"):
                yield FileObject(
                    path=blob.name.removeprefix(self.source_dir), modified_date=blob.updated
                )

    def copy_object(self, source_obj: FileObject, target_obj: FileObject) -> None:
        source_blob = self.source_bucket_client.blob(self.source_dir + source_obj.path)
        target_blob = self.source_bucket_client.copy_blob(
            source_blob, self.target_bucket_client, self.target_dir + target_obj.path
        )
        logging.info(
            "Copied: "
            + f"blob {source_blob.name} in bucket {self.source_bucket}"
            + f"to blob {target_blob.name} in bucket {self.target_bucket}"
        )

    def rename_object(self, source_obj: FileObject, target_obj: FileObject) -> None:
        if self.source_bucket == self.target_bucket:
            self._rename_within_same_bucket(source_obj, target_obj)
        else:
            self._rename_across_different_buckets(source_obj, target_obj)

        logging.info(
            "Renamed: "
            + f"blob {self.source_dir + source_obj.path} in bucket {self.source_bucket}"
            + f"to blob {self.target_dir + target_obj.path} in bucket {self.target_bucket}"
        )

    def _rename_within_same_bucket(self, source_obj: FileObject, target_obj: FileObject) -> None:
        source_blob = self.source_bucket_client.blob(self.source_dir + source_obj.path)
        self.source_bucket_client.rename_blob(source_blob, self.target_dir + target_obj.path)

    def _rename_across_different_buckets(
        self, source_obj: FileObject, target_obj: FileObject
    ) -> None:
        self.copy_object(source_obj, target_obj)
        self.source_bucket_client.delete_blob(self.source_dir + source_obj.path)
