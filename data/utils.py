import sys
import subprocess
from datetime import datetime
from pathlib import Path


FILE_DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"
UI_DATETIME_FORMAT = "%Y.%m.%d %H:%M:%S"


def open_with_explorer(path: Path) -> None:
    if sys.platform == "win32":
        subprocess.Popen(["explorer", path])
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    elif sys.platform == "linux":
        subprocess.Popen(["xdg-open", path])


def convert_timestamp(timestamp: int, time_format: str) -> str:
    return datetime.fromtimestamp(timestamp).strftime(time_format)


def get_default_mc_folder() -> Path:
    base_path = Path().home()
    if sys.platform == "win32":
        return base_path.joinpath("AppData", "Roaming", ".minecraft")
    elif sys.platform == "darwin":
        return base_path.joinpath("Library", "Application Support", "minecraft")
    elif sys.platform == "linux":
        return base_path.joinpath(".minecraft")
