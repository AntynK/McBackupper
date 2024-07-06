from pathlib import Path

from data.path_utils import convert_world_path_to_backup
from data.backup_manager.backup import Backup
from data.backup_manager.backup_file import BackupFile
from data.backup_manager.constants import BACKUPS_FOLDER

from data.backup_manager.actions.create_backup_action import CreateBackupAction
from data.backup_manager.actions.restore_backup_action import RestoreBackupAction
from data.backup_manager.actions.delete_backup_action import DeleteBackupAction
from data.backup_manager.actions.load_backups_action import LoadBackupsAction


class BackupManager:
    def __init__(self) -> None:
        self.work_dir = Path()
        self.file_path = Path()
        self.world_path = Path()
        self.backup_file = BackupFile()

        self._create_backup = CreateBackupAction(self)
        self._restore_backup = RestoreBackupAction(self)
        self._delete_backup = DeleteBackupAction(self)
        self._load_backups = LoadBackupsAction(self)

    def get_backups(self) -> list[Backup]:
        return self.backup_file.get_backups()

    def save(self):
        self.backup_file.save()

    def load(self, world_path: Path) -> None:
        self.world_path = world_path
        self.work_dir = convert_world_path_to_backup(world_path)
        self._load_backups(self.work_dir)

    def delete(self, backup: Backup) -> None:
        self._delete_backup(backup, self.work_dir)

    def create(self, new_backup: Backup) -> None:
        if not self.world_path.is_dir():
            return

        self._create_backup(new_backup, self.work_dir, self.world_path)

    def restore(self, backup: Backup) -> None:
        backup_filename = self.work_dir.joinpath(BACKUPS_FOLDER, backup.name)
        if not backup_filename.is_file():
            return

        self._restore_backup(backup_filename, self.world_path)
