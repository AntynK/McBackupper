import sys
import subprocess
from datetime import datetime
from pathlib import Path

DATE_FORMAT = "%Y.%m.%d"
TIME_FORMAT = "%H-%M-%S"
DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"


def open_with_explorer(path: Path) -> None:
    if sys.platform == "win32":
        subprocess.Popen(["explorer", path])
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    elif sys.platform == "linux":
        subprocess.Popen(["xdg-open", path])


def convert_timestamp(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime(DATETIME_FORMAT)

def get_default_mc_folder() -> Path:
    base_path = Path().home()
    if sys.platform == "win32":
        return base_path.joinpath("AppData", "Roaming", ".minecraft")
    elif sys.platform == "darwin":
        return base_path.joinpath("Library", "Application Support", "minecraft")
    elif sys.platform == "linux":
        return base_path.joinpath(".minecraft")
