from typing import Callable
import flet as ft

from data.backup_manager import Backup
from data.utils import convert_timestamp, open_with_explorer, UI_DATETIME_FORMAT


class BackupDataRow(ft.DataRow):
    def __init__(
        self,
        backup: Backup,
        on_select_changed: Callable,
        on_long_press: Callable,
        index: int,
    ) -> None:
        super().__init__()
        self.on_select_changed = lambda e: on_select_changed(backup, index)
        self.on_long_press = lambda e: on_long_press(backup)

        self.cells = [
            ft.DataCell(
                ft.Text(backup.name), on_tap=lambda e: open_with_explorer(backup.path)
            ),
            ft.DataCell(ft.Text(backup.title)),
            ft.DataCell(ft.Text(convert_timestamp(backup.created, UI_DATETIME_FORMAT))),
            ft.DataCell(ft.Checkbox(value=backup.pool_ingore, disabled=True)),
        ]
