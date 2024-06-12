import json
import shutil
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

from data.path_utils import convert_world_path_to_backup, get_top_dir
from data.utils import convert_timestamp
from data.settings import Settings

BACKUPS_FOLDER = Path("backups")
BACKUPS_FILE = Path("backups.json")
BACKUP_FILE_FORMAT = "zip"


@dataclass
class Backup:
    name: str = ""
    title: str = ""
    created: int = 0
    pull_ignore: bool = True
    path: Path = Path()

    def __post_init__(self):
        if self.created == 0:
            self.created = int(datetime.now().timestamp())

    def __eq__(self, other):
        if isinstance(other, Backup):
            return self.name == other.name
        if isinstance(other, str):
            return self.name == other


class BackupManager:
    def __init__(self) -> None:
        self.backups: list[Backup] = []
        self.work_dir = Path()
        self.file_path = Path()
        self.world_path = Path()

    def load(self, world_path: Path) -> None:
        self.backups.clear()
        self.world_path = world_path
        self.work_dir = convert_world_path_to_backup(world_path)
        self.file_path = self.work_dir.joinpath(BACKUPS_FILE)

        if not self.file_path.is_file():
            return

        try:
            data = json.loads(self.file_path.read_text("utf-8"))
        except json.decoder.JSONDecodeError:
            data = {}

        if not isinstance(data, dict):
            return
        for name, backup_data in data.items():
            if not self.work_dir.joinpath(BACKUPS_FOLDER, name).is_file():
                continue
            self.backups.append(self._load_backup(backup_data, name))
        self._check_backups_folder()
        self.save()

    def _check_backups_folder(self) -> None:
        for path in self.work_dir.joinpath(BACKUPS_FOLDER).iterdir():
            if path.name not in self.backups:
                self.backups.append(Backup(name=path.name))

    def save(self) -> None:
        self.work_dir.mkdir(exist_ok=True, parents=True)
        result = {}
        for backup in self.backups:
            result.update(**self._save_backup(backup))
        self.file_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=4), encoding="utf-8"
        )

    def delete(self, backup: Backup) -> None:
        self.backups.remove(backup)
        filepath = self.work_dir.joinpath(BACKUPS_FOLDER, backup.name)
        if filepath.is_file():
            filepath.unlink()
        self.save()

    def create(self, new_backup: Backup) -> None:
        if not self.world_path.is_dir():
            return
        filename = f"{new_backup.name} {convert_timestamp(new_backup.created)}"

        new_backup.name = f"{filename}.{BACKUP_FILE_FORMAT}"
        base_name = str(self.work_dir.joinpath(BACKUPS_FOLDER, filename))

        shutil.make_archive(
            base_name=base_name,
            format=BACKUP_FILE_FORMAT,
            root_dir=get_top_dir(self.world_path),
            base_dir=self.world_path.name,
        )

        self.backups.append(new_backup)
        self.save()
        self._check_backup_pull()

    def restore(self, backup: Backup) -> None:
        backup_file = self.work_dir.joinpath(BACKUPS_FOLDER, backup.name)
        shutil.rmtree(self.world_path, True)
        shutil.unpack_archive(
            filename=backup_file,
            extract_dir=get_top_dir(self.world_path),
            format=BACKUP_FILE_FORMAT,
        )

    def update(self, backup: Backup):
        index = self.backups.index(backup)
        self.backups[index] = backup
        self.save()

    def _check_backup_pull(self) -> None:
        pull = [backup for backup in self.backups if not backup.pull_ignore]
        max_len = Settings().get_pull_size()
        if len(pull) <= max_len:
            return
        pull.sort(key=lambda backup: backup.created, reverse=True)
        for backup in pull[max_len:]:
            self.delete(backup)

    def _load_backup(self, backup_data: dict, name: str) -> Backup:
        result = Backup()
        result.name = name
        result.title = backup_data.get("title", "")
        result.created = backup_data.get("created", 0)
        result.pull_ignore = backup_data.get("pull_ignore", True)
        result.path = self.work_dir.joinpath(BACKUPS_FOLDER)
        return result

    def _save_backup(self, backup: Backup) -> dict:
        result = {}
        result["title"] = backup.title
        result["created"] = backup.created
        result["pull_ignore"] = backup.pull_ignore
        return {backup.name: result}
