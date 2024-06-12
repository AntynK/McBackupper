from datetime import datetime

import flet as ft

from data.backup_manager import Backup
from data.controls.time_picker import TimePicker
from data.controls.date_picker import DatePicker


class BackupEntry(ft.Column):
    def __init__(self, backup: Backup):
        super().__init__(expand=True)
        self.result = backup

        self.name_field = ft.TextField(
            label="File name", value=backup.name, expand=True
        )
        self.title_field = ft.TextField(label="Title", value=backup.title, expand=True)

        self.pull_ignore_checkbox = ft.Checkbox(
            label="Pull ignore", value=backup.pull_ignore
        )
        creation_time = datetime.fromtimestamp(self.result.created)
        self.time_picker = TimePicker(creation_time)
        self.date_picker = DatePicker(creation_time)

        self.controls = [
            self.name_field,
            self.title_field,
            self.pull_ignore_checkbox,
            self.time_picker,
            self.date_picker,
        ]

    def get_backup(self) -> Backup:
        self.result.name = self.name_field.value  # type: ignore
        self.result.title = self.title_field.value  # type: ignore
        self.result.pull_ignore = self.pull_ignore_checkbox.value  # type: ignore
        self.result.created = int(
            datetime.combine(self.date_picker.get(), self.time_picker.get()).timestamp()
        )

        return self.result
