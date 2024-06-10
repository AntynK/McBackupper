from datetime import datetime
from pathlib import Path

from data.settings import Settings

TIME_FORMAT = "%Y.%m.%d %H-%M-%S"


def get_rel_path(path: Path) -> Path:
    return path.relative_to(Settings().get_mc_folder())


def convert_world_path_to_backup(path: Path) -> Path:
    return Settings().get_backup_folder().joinpath(get_rel_path(path))


def convert_timestamp(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime(TIME_FORMAT)


def is_mc_folder(folder: Path) -> bool:
    for sub_folder in ("saves", "versions"):
        if not folder.joinpath(sub_folder).is_dir():
            return False
    return True
