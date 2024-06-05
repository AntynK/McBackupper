from typing import Callable
import flet as ft

from data.backups import Backup
from data.utils import convert_timestamp


class BackupDataRow(ft.DataRow):
    def __init__(self, backup: Backup, on_select_changed: Callable):
        super().__init__()
        self.on_select_changed = lambda e: on_select_changed(backup)
        self.cells = [
            ft.DataCell(ft.Text(backup.name)),
            ft.DataCell(ft.Text(backup.title)),
            ft.DataCell(ft.Text(convert_timestamp(backup.created))),
            ft.DataCell(ft.Checkbox(value=backup.pull_ignore)),
        ]
