from typing import Union, Optional
from pathlib import Path

import flet as ft

from data.mc_world import McWorld
from data.backup_manager import BackupManager, Backup
from data.controls.backups_view import BackupsView
from data.dialogs.create_backup import CreateBackupDialog
from data.dialogs.change_backup import ChangeBackup


class BackupsEditor(ft.Column):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.page: ft.Page = page
        self.expand = True
        self.scroll = ft.ScrollMode.AUTO

        self.backup_view = BackupsView(
            self._handle_selection_change, self._show_change_backup_menu
        )
        self.backup_manager = BackupManager()

        self.restore_button = ft.TextButton(
            "Restore", icon=ft.icons.RESTORE, on_click=self._restore_handler
        )
        self.create_button = ft.TextButton(
            "Create",
            icon=ft.icons.ADD,
            on_click=self._show_create_popup,
        )
        self.edit_button = ft.TextButton(
            "Edit",
            icon=ft.icons.EDIT,
            on_click=lambda e: self._show_change_backup_menu(),
        )
        self.delete_button = ft.TextButton(
            "Delete", icon=ft.icons.DELETE, on_click=self._delete_handler
        )
        self.disable_all_buttons(True)
        self.controls = [
            ft.Row(
                [
                    self.restore_button,
                    self.create_button,
                    self.edit_button,
                    self.delete_button,
                ]
            ),
            self.backup_view,
        ]
        self.current_world: McWorld = McWorld(Path())
        self.selected_backup: Union[None, Backup] = None

    def update_backup_view(self) -> None:
        self.backup_view.set_backups(self.backup_manager.get_sorted_backups())
        self.disable_control_buttons(True)
        self.update()

    def disable_all_buttons(self, state: bool) -> None:
        self.create_button.disabled = state
        self.disable_control_buttons(state)

    def disable_control_buttons(self, state: bool) -> None:
        self.restore_button.disabled = state
        self.delete_button.disabled = state
        self.edit_button.disabled = state

    def change_world(self, new_world: McWorld) -> None:
        self.current_world = new_world
        self.backup_manager.load(new_world.path)
        self.update_backup_view()
        self.create_button.disabled = False

    def _handle_selection_change(self, selected: Backup) -> None:
        self.selected_backup = selected
        self.disable_control_buttons(False)
        self.update()

    def _show_change_backup_menu(self, backup: Optional[Backup] = None) -> None:
        if backup is None:
            if self.selected_backup is None:
                return
            backup = self.selected_backup

        ChangeBackup(self.page, backup, self._change_backup_handler).show()

    def _change_backup_handler(self, changed_backup: Backup):
        self.backup_manager.save()
        self.update_backup_view()

    def _delete_handler(self, e) -> None:
        if self.selected_backup is None:
            return
        self.backup_manager.delete(self.selected_backup)
        self.update_backup_view()

    def _show_create_popup(self, e) -> None:
        CreateBackupDialog(
            self.page, self.current_world.name, self._create_handler
        ).show()

    def _create_handler(self, new_backup: Backup) -> None:
        self.backup_manager.create(new_backup)
        self.update_backup_view()

    def _restore_handler(self, e) -> None:
        if self.selected_backup is None:
            return
        self.backup_manager.restore(self.selected_backup)
