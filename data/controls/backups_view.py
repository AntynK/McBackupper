from functools import partial
from typing import Callable, Optional

import flet as ft

from data.backup_manager.backup import Backup
from data.backup_manager.sorting import sort_backups, SortKeys
from data.controls.backup_data_row import BackupDataRow
from data.localization import Localization, Domains

_ = Localization().get_handler(Domains.CONTROLS)


class BackupsView(ft.DataTable):
    def __init__(self, on_select_changed: Callable, on_long_press: Callable) -> None:
        super().__init__()
        self.selected_row = None

        self.border = ft.Border(
            ft.BorderSide(1),
            ft.BorderSide(1),
            ft.BorderSide(1),
            ft.BorderSide(1),
        )
        self.columns = [
            ft.DataColumn(
                ft.Text(_("File name")),
                on_sort=partial(self.sort_table, sort_key=SortKeys.NAME),
            ),
            ft.DataColumn(
                ft.Text(_("Title")),
                on_sort=partial(self.sort_table, sort_key=SortKeys.TITLE),
            ),
            ft.DataColumn(
                ft.Text(_("Created")),
                on_sort=partial(self.sort_table, sort_key=SortKeys.CREATED),
            ),
            ft.DataColumn(
                ft.Text(_("Pool ignore")),
                on_sort=partial(self.sort_table, sort_key=SortKeys.POOL_IGNORE),
            ),
        ]
        self.rows = []
        self.backups: list[Backup] = []
        self.on_select_changed = on_select_changed
        self.on_long_press = on_long_press

    def sort_table(self, e, sort_key: SortKeys):
        e.control.data = not e.control.data
        self.backups = sort_backups(self.backups, sort_key, e.control.data)
        self.update_table()

    def set_backups(self, backups: list[Backup]) -> None:
        self.backups = backups
        self.update_table()

    def update_table(self) -> None:
        self.set_selected_row(None)
        self.rows.clear()
        for index, backup in enumerate(self.backups):
            self.rows.append(
                BackupDataRow(
                    backup, self._handle_select_change, self.on_long_press, index
                )
            )
        self.update()

    def set_selected_row(self, row_index: Optional[int]) -> None:
        if self.selected_row is not None:
            self.rows[self.selected_row].selected = False
        self.selected_row = row_index
        if self.selected_row is not None:
            self.rows[self.selected_row].selected = True

    def _handle_select_change(self, backup: Backup, index: int) -> None:
        self.on_select_changed(backup)
        self.set_selected_row(index)
        self.update()
