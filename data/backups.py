import json
import shutil
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from data.utils import (
    convert_world_path_to_backup,
    convert_timestamp,
)


@dataclass
class Backup:
    name: str = ""
    title: str = ""
    created: int = 0
    pull_ignore: bool = True

    def __post_init__(self):
        if self.created == 0:
            self.created = int(datetime.now().timestamp())


class BackupManager:
    def __init__(self) -> None:
        self.backups: list[Backup] = []
        self.work_dir = Path()
        self.file_path = Path()
        self.world_path = Path()
        self.selected_backup = None

    def set_selected(self, selected: Optional[Backup]):
        self.selected_backup = selected

    def load(self, world_path: Path):
        self.backups.clear()
        self.world_path = world_path
        self.work_dir = convert_world_path_to_backup(world_path)
        self.file_path = self.work_dir.joinpath("backups.json")

        if not self.file_path.is_file():
            return

        try:
            data = json.loads(self.file_path.read_text("utf-8"))
        except json.decoder.JSONDecodeError:
            data = {}

        if not isinstance(data, dict):
            return
        for name, backup_data in data.items():
            if not self.work_dir.joinpath("backups", name).is_file():
                continue
            self.backups.append(self._load_backup(backup_data, name))
        self._check_backups_folder(data)

    def _check_backups_folder(self, data: dict):
        for path in self.work_dir.joinpath("backups").iterdir():
            if path.name not in data:
                self.backups.append(Backup(name=path.name))
        self.save()

    def save(self):
        self.work_dir.mkdir(exist_ok=True, parents=True)
        result = {}
        for backup in self.backups:
            result.update(**self._save_backup(backup))
        self.file_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=4), encoding="utf-8"
        )

    def delete(self):
        if self.selected_backup is None:
            return

        self.backups.remove(self.selected_backup)
        filepath = self.work_dir.joinpath("backups", self.selected_backup.name)
        if filepath.is_file():
            filepath.unlink()
        self.save()
        self.selected_backup = None

    def create(self, new_backup: Backup):
        if not self.world_path.is_dir():
            return
        filename = f"{new_backup.name} {convert_timestamp(new_backup.created)}"

        new_backup.name = f"{filename}.zip"

        top_dir = Path(*self.world_path.parts[:-1])

        shutil.make_archive(self.work_dir.joinpath("backups", filename), "zip", top_dir, self.world_path.name)  # type: ignore
        self.backups.append(new_backup)
        self.save()

    def restore(self, e):
        if self.selected_backup is None:
            return
        backup_file = self.work_dir.joinpath("backups", self.selected_backup.name)
        shutil.rmtree(self.world_path, True)
        top_dir = Path(*self.world_path.parts[:-1])
        shutil.unpack_archive(backup_file, top_dir, "zip")

    def _load_backup(self, backup_data: dict, name: str) -> Backup:
        result = Backup()
        result.name = name
        result.title = backup_data.get("title", "")
        result.created = backup_data.get("created", 0)
        result.pull_ignore = backup_data.get("pull_ignore", True)
        return result

    def _save_backup(self, backup: Backup) -> dict:
        result = {}
        result["title"] = backup.title
        result["created"] = backup.created
        result["pull_ignore"] = backup.pull_ignore
        return {backup.name: result}
