"""
Config classes, simply extending the pydantic BaseModel are defined here to provide
a contract for users to abide by. Schema definition, validation, serialization and
deserialization are all handled within these classes.

We can expose real object instances from within these contracts/configs that can be used
later by the app logic in other modules and functions.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Literal, Union

from pydantic import BaseModel, Field, validator

from renameit.file_systems.interfaces import IFileSystem, file_systems_map
from renameit.handlers.interfaces import IHandler, handlers_map

from ..job_runners import Job
from .parse import load_config


class ProjectConfig(BaseModel):
    """UserProjectConfig."""

    version: str = "0.1"
    jobs: List[JobConfig] = Field(default_factory=list)

    @classmethod
    def create_new(cls, config_path, config_dir=None) -> "ProjectConfig":
        return cls(**load_config(user_file_path=config_path, user_dir_path=config_dir))

    def get_jobs(self) -> List[Job]:
        """Get a list of Job objects from their corresponding list of JobConfig.

        Returns:
            List[Job]: List of Job objects
        """
        return [job for job_config in self.jobs if (job := job_config.get_job()) is not None]


class JobConfig(BaseModel):
    """JobConfig."""

    name: str
    operation: Literal["rename", "copy"]
    file_system_config: FileSystemConfig = Field(alias="file_system")
    rename_handler_config: RenameHandlerConfig = Field(alias="rename_handler")

    def get_job(self) -> Union[Job, None]:
        try:
            return Job(
                name=self.name,
                file_system=self.file_system_config.get_file_system(),
                rename_handler=self.rename_handler_config.get_handler(),
                operation=f"{self.operation}_object",
            )
        except (NotImplementedError, TypeError) as e:
            logging.warning(f"Skipping job {self.name}: {str(e)}")

            if isinstance(e, TypeError):
                logging.exception(str(e))

            return None


class FileSystemConfig(BaseModel):
    """FileSystemConfig."""

    type: str
    args: Dict[str, Any]

    @validator("type")
    def type_validation(cls, value) -> str:
        if value not in file_systems_map.keys():
            raise ValueError(
                f"Unknow type `{value}`, only allowed: {', '.join(file_systems_map.keys())}"
            )
        return value

    def get_file_system(self) -> IFileSystem:
        return file_systems_map[self.type](**self.args)  # type: ignore


class RenameHandlerConfig(BaseModel):
    """RenameHandlerConfig."""

    type: str
    args: Dict[str, Any]

    @validator("type")
    def type_validation(cls, value) -> str:
        if value not in handlers_map.keys():
            raise ValueError(
                f"Unknow type `{value}`, only allowed: {', '.join(handlers_map.keys())}"
            )
        return value

    def get_handler(self) -> IHandler:
        return handlers_map[self.type](**self.args)  # type: ignore


ProjectConfig.update_forward_refs()
JobConfig.update_forward_refs()
