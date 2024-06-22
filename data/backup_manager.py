import json
import shutil
import re
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from data.path_utils import convert_world_path_to_backup, get_top_dir
from data.utils import convert_timestamp, FILE_DATETIME_FORMAT
from data.settings import Settings

BACKUPS_FOLDER = Path("backups")
BACKUPS_FILE = Path("backups.json")
BACKUP_FILE_FORMAT = "zip"


@dataclass
class Backup:
    name: str = ""
    title: str = ""
    created: int = 0
    pool_ingore: bool = True
    path: Path = Path()

    def __post_init__(self):
        if self.created == 0:
            self.created = int(datetime.now().timestamp())

    def __eq__(self, other):
        if isinstance(other, Backup):
            return self.name == other.name
        if isinstance(other, str):
            return self.name == other


class SortKeys(Enum):
    NAME = "name"
    TITLE = "title"
    CREATED = "created"
    POOL_IGNORE = "pool_ingore"


def sort_backups(
    backups: list[Backup], key: SortKeys, reverse: bool = False
) -> list[Backup]:
    return sorted(backups, key=lambda e: getattr(e, key.value), reverse=reverse)


class BackupManager:
    def __init__(self) -> None:
        self.backups: list[Backup] = []
        self.work_dir = Path()
        self.file_path = Path()
        self.world_path = Path()

    def get_sorted_backups(self) -> list[Backup]:
        return sort_backups(self.backups, SortKeys.CREATED)

    def load(self, world_path: Path) -> None:
        self.backups.clear()
        self.world_path = world_path
        self.work_dir = convert_world_path_to_backup(world_path)
        self.file_path = self.work_dir.joinpath(BACKUPS_FILE)

        if not self.work_dir.joinpath(BACKUPS_FOLDER).is_dir():
            return

        try:
            data = json.loads(self.file_path.read_text("utf-8"))
        except (json.decoder.JSONDecodeError, OSError):
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
            file_name = path.name
            if file_name not in self.backups:
                self.backups.append(
                    Backup(
                        name=file_name,
                        created=self._get_timestamp_from_string(file_name),
                        pool_ingore=False,
                    )
                )

    def _get_timestamp_from_string(self, string: str) -> int:
        matched = re.match(r"\d{4}.\d{2}.\d{2}.\d{2}.\d{2}.\d{2}", string)
        if matched is None:
            return 0

        return int(datetime.strptime(matched.group(), FILE_DATETIME_FORMAT).timestamp())

    def save(self) -> None:
        self.work_dir.mkdir(exist_ok=True, parents=True)
        result = dict(self._save_backup(backup) for backup in self.backups)

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
        filename = f"{convert_timestamp(new_backup.created, FILE_DATETIME_FORMAT)}_{new_backup.name}"
        new_backup.path = self.work_dir.joinpath(BACKUPS_FOLDER)
        new_backup.name = f"{filename}.{BACKUP_FILE_FORMAT}"
        base_name = str(new_backup.path.joinpath(filename))

        shutil.make_archive(
            base_name=base_name,
            format=BACKUP_FILE_FORMAT,
            root_dir=get_top_dir(self.world_path),
            base_dir=self.world_path.name,
        )

        self.backups.append(new_backup)
        self.save()
        self._check_backup_pool()

    def restore(self, backup: Backup) -> None:
        backup_file = self.work_dir.joinpath(BACKUPS_FOLDER, backup.name)
        shutil.rmtree(self.world_path, True)
        shutil.unpack_archive(
            filename=backup_file,
            extract_dir=get_top_dir(self.world_path),
            format=BACKUP_FILE_FORMAT,
        )

    def _check_backup_pool(self) -> None:
        pool = [backup for backup in self.backups if not backup.pool_ingore]
        max_len = Settings().get_pool_size()
        if len(pool) <= max_len:
            return

        sorted_pool = sort_backups(pool, SortKeys.CREATED, True)
        for backup in sorted_pool[max_len:]:
            self.delete(backup)

    def _load_backup(self, backup_data: dict, name: str) -> Backup:
        result = Backup()
        result.name = name
        result.title = backup_data.get("title", "")
        result.created = backup_data.get("created", 0)
        if "pull_ignore" in backup_data:  # Compatibility with previous versions
            backup_data["pool_ignore"] = backup_data["pull_ignore"]

        result.pool_ingore = backup_data.get("pool_ignore", True)

        result.path = self.work_dir.joinpath(BACKUPS_FOLDER)
        return result

    def _save_backup(self, backup: Backup) -> tuple[str, dict]:
        result = {}
        result["title"] = backup.title
        result["created"] = backup.created
        result["pool_ignore"] = backup.pool_ingore
        return backup.name, result
