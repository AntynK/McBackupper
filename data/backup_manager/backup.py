from datetime import datetime
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Backup:
    name: str = ""
    title: str = ""
    created: int = 0
    pool_ingore: bool = True
    path: Path = Path()

    def __post_init__(self):
        if self.created == 0:
            self.created = int(datetime.now().timestamp())

    def __eq__(self, other):
        if isinstance(other, Backup):
            return self.name == other.name
        if isinstance(other, str):
            return self.name == other
