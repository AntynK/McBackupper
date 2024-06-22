from typing import Callable

import flet as ft

from data.backup_manager import Backup
from data.dialogs.dialog import Dialog
from data.controls.backup_entry import BackupEntry


class ChangeBackup(Dialog):
    def __init__(
        self, page: ft.Page, backup: Backup, after_completion: Callable
    ) -> None:
        super().__init__(page=page, title="Change backup")
        self.backup_entry = BackupEntry(backup, True)

        self.content = self.backup_entry

        self.actions = [
            ft.TextButton("Save", on_click=self.save),
            ft.TextButton("Cancel", on_click=self.close),
        ]
        self.after_completion = after_completion

    def save(self, event=None) -> None:
        self.after_completion(self.backup_entry.get_backup())
        self.close()
