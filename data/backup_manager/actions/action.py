from abc import ABC, abstractmethod

from data.backup_manager.backup_file import BackupFile


class Action(ABC):
    def __init__(self, backup_manager) -> None:
        self._backup_manager = backup_manager
        self.backup_file: BackupFile = backup_manager.backup_file

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass
