import json
from pathlib import Path
from typing import Union, Any

from data.utils import get_default_mc_folder

SETTINGS_FILE = Path("settings.json")

DEFAULT_POOL_SIZE = 4
DEFAULT_MC_FOLDER = get_default_mc_folder()
DEFAULT_BACKUPS_FOLDER = Path("backups")


class Settings:
    __INSTANCE = None
    __INITIALIZED = False

    def __new__(cls):
        if Settings.__INSTANCE is None:
            Settings.__INSTANCE = super().__new__(cls)
        return Settings.__INSTANCE

    def __init__(self) -> None:
        if Settings.__INITIALIZED:
            return
        Settings.__INITIALIZED = True
        self._data: dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        try:
            with open(SETTINGS_FILE, encoding="utf-8") as file:
                self._data = json.load(file)
        except OSError:
            self.update_backup_folder(DEFAULT_BACKUPS_FOLDER)
            self.update_mc_folder(DEFAULT_MC_FOLDER)
            self.update_pool_size(DEFAULT_POOL_SIZE)

    def save(self) -> None:
        with open(
            SETTINGS_FILE,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(self._data, file, ensure_ascii=False, indent=4)

    def get_backup_folder(self) -> Path:
        if "backup_folder" not in self._data:
            self.update_backup_folder(DEFAULT_BACKUPS_FOLDER)
        return Path(self._data["backup_folder"]).absolute()

    def update_backup_folder(self, new_folder: Union[str, Path]) -> None:
        self._data["backup_folder"] = str(new_folder)
        self.save()

    def get_mc_folder(self) -> Path:
        if "mc_folder" not in self._data:
            self.update_mc_folder(DEFAULT_MC_FOLDER)
        return Path(self._data["mc_folder"]).absolute()

    def update_mc_folder(self, new_folder: Union[str, Path]) -> None:
        self._data["mc_folder"] = str(new_folder)
        self.save()

    def get_pool_size(self) -> int:
        if "pull_size" in self._data: # Compatibility with previous versions
            self._data["pool_size"] = self._data.pop("pull_size")

        if "pool_size" not in self._data:
            self.update_pool_size(DEFAULT_POOL_SIZE)
        return self._data["pool_size"]

    def update_pool_size(self, new_size: int):
        self._data["pool_size"] = new_size
        self.save()
