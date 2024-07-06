import re
from pathlib import Path
from datetime import datetime

from data.utils import FILE_DATETIME_FORMAT
from data.backup_manager.constants import BACKUPS_FOLDER
from data.backup_manager.actions.action import Action
from data.backup_manager.backup import Backup


class LoadBackupsAction(Action):
    def __call__(self, work_dir: Path):
        self.backup_file.load(work_dir)

        if not work_dir.joinpath(BACKUPS_FOLDER).is_dir():
            return

        self._check_backups_folder(work_dir)

    def _check_backups_folder(self, work_dir: Path) -> None:
        for path in work_dir.joinpath(BACKUPS_FOLDER).iterdir():
            file_name = path.name
            if file_name not in self.backup_file.get_backups():
                self.backup_file.add_backup(
                    Backup(
                        name=file_name,
                        created=self._get_timestamp_from_string(file_name),
                        pool_ingore=False,
                    )
                )

    def _get_timestamp_from_string(self, string: str) -> int:
        matched = re.match(r"\d{4}.\d{2}.\d{2}.\d{2}.\d{2}.\d{2}", string)
        if matched is None:
            return 0

        return int(datetime.strptime(matched.group(), FILE_DATETIME_FORMAT).timestamp())
