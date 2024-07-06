import json
from pathlib import Path
from typing import Any

from data.backup_manager.backup import Backup
from data.backup_manager.constants import BACKUPS_FOLDER


BACKUPS_FILE = Path("backups.json")


class BackupFile:
    def __init__(self) -> None:
        self.filepath = Path()
        self.world_path = Path()
        self.backups: list[Backup] = []

    def get_backups(self) -> list[Backup]:
        return self.backups

    def add_backup(self, backup: Backup):
        self.backups.append(backup)
        self.save()

    def remove_backup(self, backup: Backup):
        self.backups.remove(backup)
        self.save()

    def clear(self) -> None:
        self.backups.clear()
        self.save()

    def load(self, work_dir: Path):
        self.work_dir = work_dir
        self.filepath = work_dir.joinpath(BACKUPS_FILE)
        self.backups.clear()

        try:
            data = json.loads(self.filepath.read_text("utf-8"))
        except (json.decoder.JSONDecodeError, OSError):
            data = {}

        if not isinstance(data, dict):
            return

        for name, backup_data in data.items():
            if not self.work_dir.joinpath(BACKUPS_FOLDER, name).is_file():
                continue
            self.backups.append(self._load_backup(backup_data, name))
        self.save()

    def save(self):
        self.work_dir.mkdir(exist_ok=True, parents=True)
        result = dict(self._save_backup(backup) for backup in self.backups)

        self.filepath.write_text(
            json.dumps(result, ensure_ascii=False, indent=4), encoding="utf-8"
        )

    def _load_backup(self, backup_data: dict, name: str):
        result = Backup()
        result.name = name
        result.title = self._get_value(backup_data, "title", "", str)
        result.created = self._get_value(backup_data, "created", 0, int)
        if "pull_ignore" in backup_data:  # Compatibility with previous versions
            backup_data["pool_ignore"] = backup_data["pull_ignore"]

        result.pool_ingore = self._get_value(backup_data, "pool_ignore", True, bool)

        result.path = self.work_dir.joinpath(BACKUPS_FOLDER)
        return result

    def _save_backup(self, backup: Backup) -> tuple[str, dict]:
        result = {}
        result["title"] = backup.title
        result["created"] = backup.created
        result["pool_ignore"] = backup.pool_ingore
        return backup.name, result

    def _get_value(self, data: dict, key: str, default: Any, expected_type: Any) -> Any:
        if key not in data or not isinstance(data[key], expected_type):
            return default

        return data[key]
