import logging
from typing import Iterable, Union

from azure.identity import ClientSecretCredential
from azure.storage.filedatalake import DataLakeServiceClient

from renameit.core.models import FileObject
from renameit.core.util import add_slash
from renameit.file_systems.interfaces import IFileSystem


# FileSystemAzureDatalakeStorage # noqa
class FileSystemAzureDatalakeStorage(IFileSystem):
    """Manage files on azure datalake storage gen2.

    Supports multiple authentication methods:

      - Storage account name and access keys
      - Storage account connection strings
      - Service principal with RBAC assignments

    Args:
        source_container (str): Name of storage account container with the original files.
        target_container (str): Name of storage account container that should contain new files.
            Defaults to be the same as source_container and it will be created automatically if it
            doesn't exist.
        source_dir (str, optional): Directory path from where to start looking for files.
            If not provided defaults to source_container root.
        target_dir (str, optional): Directory path to where should the new files be written.
            If not provided defaults to target_container root.
        secure_transfer (bool, optional): Whether to use https or not. Uses https by default.
        recursive (bool, optional): Whether Decides whether to look for files recursively.
            Defaults to True.
        connection_string (str, optional): The storage account connection string.
        storage_account_name (str, optional): Storage account name.
        storage_account_key (str, optional): Storage account access key.
        tenant_id (str, optional): Directory (tenant) ID of the service principal (app).
        client_id (str, optional): Application (client) ID of the service principal (app).
        client_secret (str, optional): The app password that it uses to authenticate itself.
        account_url (str, optional): Provided if the storage account was behind a custom
            domain name. Defaults to <protocol>://<storage_account_name>.dfs.core.windows.net.
    """

    name = "azure_datalake_storage"

    def __init__(
        self,
        source_container: str,
        target_container: str = None,
        source_dir: str = None,
        target_dir: str = None,
        secure_transfer: bool = True,
        recursive: bool = True,
        connection_string: str = None,
        storage_account_name: str = None,
        storage_account_key: str = None,
        tenant_id: str = None,
        client_id: str = None,
        client_secret: str = None,
        account_url: str = None,
    ):

        super().__init__()

        self.source_container = source_container
        self.target_container = target_container or source_container
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.protocol = "https" if secure_transfer else "http"
        self.recursive = recursive

        self.connection_string = connection_string
        self.storage_account_name = storage_account_name
        self.storage_account_key = storage_account_key
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret

        self.account_url = (
            account_url or f"{self.protocol}://{self.storage_account_name}.dfs.core.windows.net"
        )

        self.service_client = self._get_service_client()
        self.source_file_system_client = self.service_client.get_file_system_client(
            file_system=self.source_container
        )
        self.target_file_system_client = self.service_client.get_file_system_client(
            file_system=self.target_container
        )

        if not self.target_file_system_client.exists():
            self.target_file_system_client.create_file_system()

    def _get_service_client(self) -> DataLakeServiceClient:
        if self.connection_string:
            return DataLakeServiceClient.from_connection_string(self.connection_string)
        elif self.storage_account_name:

            credential: Union[ClientSecretCredential, str]

            if self.storage_account_key:
                credential = self.storage_account_key
            elif self.tenant_id and self.client_id and self.client_secret:
                credential = ClientSecretCredential(
                    tenant_id=self.tenant_id,
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                )
            else:
                raise ValueError(
                    "Not enough credentials provided in order to connect to azure storage service."
                )

            return DataLakeServiceClient(account_url=self.account_url, credential=credential)

        else:
            raise ValueError("Either 'connection_string' or 'storage_account_name' is required.")

    def list_objects(self) -> Iterable[FileObject]:
        paths = self.source_file_system_client.get_paths(
            path=self.source_dir, recursive=self.recursive
        )

        for path in paths:
            if not path.is_directory:
                yield FileObject(
                    path=path.name.removeprefix(add_slash(self.source_dir)),
                    modified_date=path.last_modified,
                )

    def rename_object(self, source_obj: FileObject, target_obj: FileObject) -> None:
        logging.info(
            "Renaming: "
            + f"{self.account_url}/{self.source_container}/"
            + f"{add_slash(self.source_dir)}{source_obj.path}"
            + " to "
            + f"{self.account_url}/{self.target_container}/"
            + f"{add_slash(self.target_dir)}{target_obj.path}"
        )

        full_target_path = add_slash(self.target_dir) + target_obj.path

        self.target_file_system_client.create_file(full_target_path)

        self.source_file_system_client.get_file_client(
            file_path=add_slash(self.source_dir) + source_obj.path
        ).rename_file(new_name=self.target_container + "/" + full_target_path)
