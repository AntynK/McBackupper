from typing import Callable

import flet as ft

from data.backup_manager import Backup
from data.controls.backup_data_row import BackupDataRow


class BackupsView(ft.DataTable):
    def __init__(self, on_select_changed: Callable, on_long_press: Callable) -> None:
        super().__init__()

        self.border = ft.Border(
            ft.BorderSide(1),
            ft.BorderSide(1),
            ft.BorderSide(1),
            ft.BorderSide(1),
        )
        self.columns = [
            ft.DataColumn(ft.Text("File name")),
            ft.DataColumn(ft.Text("Title")),
            ft.DataColumn(ft.Text("Created(Y.M.D H-M-S)")),
            ft.DataColumn(ft.Text("Pull ignore")),
        ]
        self.rows = []
        self.backups: list[Backup] = []
        self.on_select_changed = on_select_changed
        self.on_long_press = on_long_press

    def set_backups(self, backups: list[Backup]) -> None:
        self.backups = backups
        self.update_table()

    def update_table(self) -> None:
        self.rows.clear()
        for backup in self.backups:
            self.rows.append(
                BackupDataRow(backup, self.on_select_changed, self.on_long_press)
            )
        self.update()
