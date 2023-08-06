from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class FileObject:
    """This class represents common file metadata."""

    path: str
    modified_date: Optional[datetime] = None

    def __repr__(self) -> str:
        return self.path
