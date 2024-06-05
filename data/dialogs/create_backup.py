from typing import Callable

import flet as ft

from data.backups import Backup


class CreateBackupDialog(ft.AlertDialog):
    def __init__(self, page: ft.Page, world_name: str, after_completion: Callable):
        super().__init__()
        self.result = Backup()
        self.title = ft.Text("Create backup")
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
            ft.TextButton("Cancel", on_click=self.cancel),
        ]
        self.page: ft.Page = page
        self.after_completion = after_completion

    def close(self):
        self.open = False
        self.page.update()

    def cancel(self, e):
        self.close()

    def update_backup(self):
        self.result.name = self.name_field.value  # type: ignore
        self.result.title = self.title_field.value  # type: ignore
        self.result.pull_ignore = self.pull_ignore_checkbox.value  # type: ignore

    def create(self, e):
        self.update_backup()
        self.after_completion(self.result)
        self.close()

    def show(self):
        self.page.dialog = self
        self.open = True
        self.page.update()
