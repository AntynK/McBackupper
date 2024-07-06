from enum import Enum
from data.backup_manager.backup import Backup


class SortKeys(Enum):
    NAME = "name"
    TITLE = "title"
    CREATED = "created"
    POOL_IGNORE = "pool_ingore"


def sort_backups(
    backups: list[Backup], key: SortKeys, reverse: bool = False
) -> list[Backup]:
    return sorted(
        backups, key=lambda backup: getattr(backup, key.value), reverse=reverse
    )
