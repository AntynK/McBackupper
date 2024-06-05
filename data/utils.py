import sys
import subprocess
from pathlib import Path
from datetime import datetime

TIME_FORMAT = "%Y.%m.%d %H-%M-%S"


def open_with_explorer(path: Path) -> None:
    if sys.platform == "win32":
        subprocess.Popen(["explorer", path])
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    elif sys.platform == "linux":
        subprocess.Popen(["xdg-open", path])


def get_mc_folder() -> Path:
    base_path = Path().home()
    if sys.platform == "win32":
        return base_path.joinpath("AppData", "Roaming", ".minecraft")
    elif sys.platform == "darwin":
        return base_path.joinpath("Library", "Application Support", "minecraft")
    elif sys.platform == "linux":
        return base_path.joinpath(".minecraft")


def get_rel_path(path: Path) -> Path:
    return path.relative_to(get_mc_folder())


def get_backups_folder() -> Path:
    return Path("backups")


def convert_world_path_to_backup(path: Path):
    return get_backups_folder().joinpath(get_rel_path(path))


def convert_timestamp(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime(TIME_FORMAT)
