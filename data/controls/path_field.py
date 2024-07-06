from pathlib import Path

import flet as ft

from data.path_utils import get_top_dir
from data.localization import Localization, Domains

_ = Localization().get_handler(Domains.CONTROLS)


class PathField(ft.Row):
    def __init__(self, label: str, page: ft.Page) -> None:
        super().__init__(expand=True)
        self.path_field = ft.TextField(label=label, expand=True)
        self.file_picker = ft.FilePicker(on_result=self._save_selected_path)
        self.file_picker.allow_multiple = False

        self.controls = [
            self.path_field,
            ft.TextButton(text="...", on_click=self._show_file_picker),
        ]
        page.overlay.append(self.file_picker)

    @property
    def path(self) -> str:
        return self.path_field.value  # type: ignore

    @path.setter
    def path(self, new_path: str) -> None:
        self.path_field.value = new_path
        self.update()

    def set_error(self, error_text: str) -> None:
        self.path_field.error_text = error_text
        self.update()

    def remove_error(self) -> None:
        self.set_error("")

    def _save_selected_path(self, event: ft.FilePickerResultEvent) -> None:
        if new_path := event.path:
            self.path_field.value = new_path
            self.update()

    def _show_file_picker(self, event=None) -> None:
        path = Path(self.path)
        if not path.is_dir():
            path = get_top_dir(path)
        self.file_picker.get_directory_path(_("Select folder"), str(path))
