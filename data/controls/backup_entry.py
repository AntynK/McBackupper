from datetime import datetime

import flet as ft

from data.backup_manager.backup import Backup
from data.controls.time_picker import TimePicker
from data.controls.date_picker import DatePicker
from data.localization import Localization, Domains

_ = Localization().get_handler(Domains.CONTROLS)


class BackupEntry(ft.Column):
    def __init__(self, backup: Backup, disable_name_field: bool = False):
        super().__init__(expand=True)
        self.result = backup

        self.name_field = ft.TextField(
            label=_("File name"),
            value=backup.name,
            expand=True,
            disabled=disable_name_field,
        )
        self.title_field = ft.TextField(
            label=_("Title"), value=backup.title, expand=True
        )

        self.pool_ignore_checkbox = ft.Checkbox(
            label=_("Pool ignore"), value=backup.pool_ingore
        )
        creation_time = datetime.fromtimestamp(self.result.created)
        self.time_picker = TimePicker(creation_time)
        self.date_picker = DatePicker(creation_time)

        self.controls = [
            self.name_field,
            self.title_field,
            self.pool_ignore_checkbox,
            self.time_picker,
            self.date_picker,
        ]

    def get_backup(self) -> Backup:
        self.result.name = self.name_field.value  # type: ignore
        self.result.title = self.title_field.value  # type: ignore
        self.result.pool_ingore = self.pool_ignore_checkbox.value  # type: ignore
        self.result.created = int(
            datetime.combine(self.date_picker.get(), self.time_picker.get()).timestamp()
        )

        return self.result
