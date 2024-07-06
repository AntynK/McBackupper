import shutil
from pathlib import Path

from data.settings import Settings
from data.utils import convert_timestamp, FILE_DATETIME_FORMAT
from data.path_utils import get_top_dir
from data.backup_manager.constants import BACKUP_FILE_FORMAT, BACKUPS_FOLDER
from data.backup_manager.backup import Backup
from data.backup_manager.sorting import SortKeys, sort_backups
from data.backup_manager.actions.action import Action


class CreateBackupAction(Action):
    def __call__(self, new_backup: Backup, work_dir: Path, world_path: Path):
        filename = f"{convert_timestamp(new_backup.created, FILE_DATETIME_FORMAT)}_{new_backup.name}"
        new_backup.path = work_dir.joinpath(BACKUPS_FOLDER)
        new_backup.name = f"{filename}.{BACKUP_FILE_FORMAT}"
        base_name = str(new_backup.path.joinpath(filename))

        shutil.make_archive(
            base_name=base_name,
            format=BACKUP_FILE_FORMAT,
            root_dir=get_top_dir(world_path),
            base_dir=world_path.name,
        )

        self.backup_file.add_backup(new_backup)
        self._check_backup_pool()

    def _check_backup_pool(self) -> None:
        pool = [backup for backup in self.backup_file.get_backups() if not backup.pool_ingore]
        max_len = Settings().get_pool_size()
        if len(pool) <= max_len:
            return

        sorted_pool = sort_backups(pool, SortKeys.CREATED, True)
        for backup in sorted_pool[max_len:]:
            self._backup_manager.delete(backup)
