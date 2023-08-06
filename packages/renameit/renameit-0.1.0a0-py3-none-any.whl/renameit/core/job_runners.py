# pylint: disable=logging-fstring-interpolation
"""This module contains job runner classes that will run the renaming jobs

The module contains the following:

- `Job` - Class representing renaming job.
- `JobRunnerStandard` - Implementation for standard job runner.
"""


import logging
from typing import List

from ..file_systems.interfaces import IFileSystem
from ..handlers.interfaces import IHandler


class Job:
    """The job class that contains the processing details. Providing the central point
    for file systems and handlers interactions.

    Args:
        name (str): Name of the job.
        file_system (IFileSystem): Which file system to use.
        rename_handler (IHandler): Which renaming handler to use.
        operation (str): What operation to do on the matched files,
                        accepted values are (rename, copy) case sensitive.
    """

    def __init__(
        self,
        name: str,
        file_system: IFileSystem,
        rename_handler: IHandler,
        operation: str,
    ):

        if (
            file_system.__class__.copy_object == IFileSystem.copy_object
            and operation == "copy_object"
        ):
            raise NotImplementedError(
                f"FileSystem type `{file_system.name}` does not support copying objects."
            )
        if (
            file_system.__class__.rename_object == IFileSystem.rename_object
            and operation == "rename_object"
        ):
            raise NotImplementedError(
                f"FileSystem type `{file_system.name}` does not support renaming objects."
            )

        self.name = name
        self.file_system = file_system
        self.rename_handler = rename_handler
        self.operation = operation

    def run(self):
        """A job needs to run at some point."""

        logging.info(f"Running job {self.name}")

        for file_obj in self.file_system.list_objects():
            new_file_obj = self.rename_handler.get_new_name(file_obj=file_obj)

            if file_obj.path != new_file_obj.path:
                getattr(self.file_system, self.operation)(
                    source_obj=file_obj,
                    target_obj=self.rename_handler.get_new_name(file_obj=file_obj),
                )


class IJobRunner:
    """Interface for all job runner implementations. A job runner is responsible for
    the execution logic of multiple jobs.

    Args:
        jobs (List[Job])
    """

    def __init__(self, jobs: List[Job]) -> None:

        self.jobs = jobs

    def execute(self) -> None:
        """Provide a way to execute a list of jobs."""
        raise NotImplementedError()


class JobRunnerStandard(IJobRunner):
    """A simple implementation for executing jobs in sequence."""

    def execute(self) -> None:
        for job in self.jobs:
            job.run()
