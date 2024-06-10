from typing import Callable

import flet as ft

from data.backups import Backup
from data.dialogs.dialog import Dialog


class CreateBackupDialog(Dialog):
    def __init__(
        self, page: ft.Page, world_name: str, after_completion: Callable
    ) -> None:
        super().__init__(page=page, title="Create backup")
        self.result = Backup()
        self.name_field = ft.TextField(label="File name", value=world_name)
        self.title_field = ft.TextField(label="Title")

        self.pull_ignore_checkbox = ft.Checkbox(label="Pull ignore")

        self.content = ft.Column(
            [
                self.name_field,
                self.title_field,
                self.pull_ignore_checkbox,
            ]
        )
        self.actions = [
            ft.TextButton("Create", on_click=self.create),
            ft.TextButton("Cancel", on_click=self.close),
        ]
        self.after_completion = after_completion

    def update_backup(self) -> None:
        self.result.name = self.name_field.value  # type: ignore
        self.result.title = self.title_field.value  # type: ignore
        self.result.pull_ignore = self.pull_ignore_checkbox.value  # type: ignore

    def create(self, event=None) -> None:
        self.update_backup()
        self.after_completion(self.result)
        self.close()
