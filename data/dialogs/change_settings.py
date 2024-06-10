from pathlib import Path

import flet as ft

from data.settings import Settings
from data.dialogs.dialog import Dialog
from data.path_utils import is_mc_folder
from data.controls.path_field import PathField


class ChangeSettings(Dialog):
    def __init__(self, page: ft.Page) -> None:
        super().__init__(page=page, title="Settings")
        self.backups_folder_field = PathField(label="Backups folder", page=page)
        self.mc_folder_field = PathField(label="Minecraft folder", page=page)
        self.pull_size_entry = ft.TextField(label="Pull size")

        self.content = ft.Column(
            [self.backups_folder_field, self.mc_folder_field, self.pull_size_entry]
        )
        self.actions = [
            ft.TextButton("Save", on_click=self.save),
            ft.TextButton("Cancel", on_click=self.close),
        ]

    def save(self, event=None) -> None:
        backup_folder = Path(self.backups_folder_field.path)  # type: ignore
        if not backup_folder.is_dir():
            self.backups_folder_field.set_error("Wrong path")
            return
        Settings().update_backup_folder(backup_folder)
        self.backups_folder_field.remove_error()

        mc_folder = Path(self.mc_folder_field.path)  # type: ignore
        if not is_mc_folder(mc_folder):
            self.mc_folder_field.set_error("Wrong path")
            return
        Settings().update_mc_folder(mc_folder)
        self.mc_folder_field.remove_error()

        try:
            pull_size = int(self.pull_size_entry.value)  # type: ignore
            if pull_size <= 0:
                raise ValueError()
        except ValueError:
            self.pull_size_entry.error_text = "Wrong size"
            self.pull_size_entry.update()
            return
        self.pull_size_entry.error_text = ""
        self.pull_size_entry.update()

        Settings().update_pull_size(pull_size)
        self.close()

    def show(self, event=None) -> None:
        super().show(event)
        self.backups_folder_field.path = str(Settings().get_backup_folder())
        self.backups_folder_field.remove_error()

        self.mc_folder_field.path = str(Settings().get_mc_folder())
        self.backups_folder_field.remove_error()

        self.pull_size_entry.value = str(Settings().get_pull_size())
        self.pull_size_entry.error_text = ""
        self.update()
