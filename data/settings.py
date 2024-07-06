import json
from pathlib import Path
from typing import Union, Any

from data.utils import get_default_mc_folder

SETTINGS_FILE = Path("settings.json")

DEFAULT_POOL_SIZE = 4
DEFAULT_MC_FOLDER = get_default_mc_folder()
DEFAULT_BACKUPS_FOLDER = Path("backups")
DEFAULT_LANGUAGE = "en"


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
        except (OSError, json.JSONDecodeError):
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
        path = self._get_value("backup_folder", str(DEFAULT_BACKUPS_FOLDER.absolute()), str)
        return Path(path).absolute()

    def update_backup_folder(self, new_folder: Union[str, Path]) -> None:
        self._handle_update("backup_folder", str(new_folder))

    def get_mc_folder(self) -> Path:
        path = self._get_value("mc_folder", str(DEFAULT_MC_FOLDER.absolute()), str)
        return Path(path).absolute()

    def update_mc_folder(self, new_folder: Union[str, Path]) -> None:
        self._handle_update("mc_folder", str(new_folder))

    def get_pool_size(self) -> int:
        if "pull_size" in self._data:  # Compatibility with previous versions
            self.update_pool_size(self._data.pop("pull_size"))

        return self._get_value("pool_size", DEFAULT_POOL_SIZE, int)

    def update_pool_size(self, new_size: int) -> None:
        self._handle_update("pool_size", new_size)

    def get_language(self) -> str:
        return self._get_value("lang", DEFAULT_LANGUAGE, str)

    def update_language(self, new_lang: str) -> None:
        self._handle_update("lang", new_lang)

    def _handle_update(self, key: str, value: Any) -> None:
        self._data[key] = value
        self.save()

    def _get_value(self, key: str, default: Any, expected_type: Any) -> Any:
        if key not in self._data or not isinstance(self._data[key], expected_type):
            self._handle_update(key, default)

        return self._data[key]
