import shutil
from pathlib import Path

from data.path_utils import get_top_dir
from data.backup_manager.constants import BACKUP_FILE_FORMAT
from data.backup_manager.actions.action import Action


class RestoreBackupAction(Action):
    def __call__(self, backup_filename: Path, world_path: Path):
        shutil.rmtree(world_path, True)
        shutil.unpack_archive(
            filename=backup_filename,
            extract_dir=get_top_dir(world_path),
            format=BACKUP_FILE_FORMAT,
        )
