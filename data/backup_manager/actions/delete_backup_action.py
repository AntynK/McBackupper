from pathlib import Path

from data.backup_manager.constants import BACKUPS_FOLDER
from data.backup_manager.actions.action import Action
from data.backup_manager.backup import Backup


class DeleteBackupAction(Action):
    def __call__(self, backup: Backup, work_dir: Path):
        self.backup_file.remove_backup(backup)
        filepath = work_dir.joinpath(BACKUPS_FOLDER, backup.name)
        if filepath.is_file():
            filepath.unlink()
