import sys
import subprocess
from pathlib import Path


def open_with_explorer(path: Path) -> None:
    if sys.platform == "win32":
        subprocess.Popen(["explorer", path])
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    elif sys.platform == "linux":
        subprocess.Popen(["xdg-open", path])


def get_default_mc_folder() -> Path:
    base_path = Path().home()
    if sys.platform == "win32":
        return base_path.joinpath("AppData", "Roaming", ".minecraft")
    elif sys.platform == "darwin":
        return base_path.joinpath("Library", "Application Support", "minecraft")
    elif sys.platform == "linux":
        return base_path.joinpath(".minecraft")


DEFAULT_MC_FOLDER = get_default_mc_folder()
DEFAULT_BACKUPS_FOLDER = Path("backups")
