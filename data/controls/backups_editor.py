from pathlib import Path

import flet as ft

from data.mc_world import McWorld
from data.backups import BackupManager
from data.controls.backups_view import BackupsView
from data.dialogs.create_backup import CreateBackupDialog


class BackupsEditor(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page: ft.Page = page

        self.backup_view = BackupsView(self._handle_selection_change)
        self.backup_manager = BackupManager()

        self.restore_button = ft.TextButton(
            "Restore", icon=ft.icons.RESTORE, on_click=self.backup_manager.restore
        )
        self.create_button = ft.TextButton(
            "Create",
            icon=ft.icons.ADD,
            on_click=self._show_create_popup,
        )
        self.delete_button = ft.TextButton(
            "Delete", icon=ft.icons.DELETE, on_click=self._delete_handler
        )
        self.disable_all_buttons(True)
        self.controls = [
            ft.Row([self.restore_button, self.create_button, self.delete_button]),
            self.backup_view,
        ]
        self.current_world: McWorld = McWorld(Path())

    def update_backup_view(self):
        self.backup_view.set_backups(self.backup_manager.backups)
        self.disable_control_buttons(True)
        self.update()

    def disable_all_buttons(self, state: bool):
        self.create_button.disabled = state
        self.disable_control_buttons(state)

    def disable_control_buttons(self, state: bool):
        self.restore_button.disabled = state
        self.delete_button.disabled = state

    def change_world(self, new_world: McWorld):
        self.current_world = new_world
        self.backup_manager.load(new_world.path)
        self.backup_manager.set_selected(None)
        self.update_backup_view()
        self.create_button.disabled = False

    def _handle_selection_change(self, selected):
        self.disable_control_buttons(False)
        self.update()
        self.backup_manager.set_selected(selected)

    def _delete_handler(self, e):
        self.backup_manager.delete()
        self.update_backup_view()

    def _show_create_popup(self, e):
        CreateBackupDialog(
            self.page, self.current_world.name, self._create_handler
        ).show()

    def _create_handler(self, new_backup):
        self.backup_manager.create(new_backup)
        self.update_backup_view()
