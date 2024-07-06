from typing import Callable

import flet as ft

from data.backup_manager.backup import Backup
from data.dialogs.dialog import Dialog
from data.controls.backup_entry import BackupEntry
from data.localization import Localization, Domains

_ = Localization().get_handler(Domains.DIALOGS)


class CreateBackupDialog(Dialog):
    def __init__(
        self, page: ft.Page, world_name: str, after_completion: Callable
    ) -> None:
        super().__init__(page=page, title=_("Create backup"))
        self.backup_entry = BackupEntry(Backup(name=world_name))

        self.content = ft.Column([self.backup_entry], expand=True)

        self.actions = [
            ft.TextButton(_("Create"), on_click=self.create),
            ft.TextButton(_("Cancel"), on_click=self.close),
        ]
        self.after_completion = after_completion

    def create(self, event=None) -> None:
        self.after_completion(self.backup_entry.get_backup())
        self.close()
