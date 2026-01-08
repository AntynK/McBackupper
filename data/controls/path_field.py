from typing import Optional
from pathlib import Path

import flet as ft

from data.path_utils import get_top_dir
from data.localization import Localization, Domains

_ = Localization().get_handler(Domains.CONTROLS)


class PathField(ft.Row):
    def __init__(self, label: str) -> None:
        super().__init__(expand=True)
        self.path_field = ft.TextField(label=label, expand=True, autocorrect=False)
        self.file_picker = ft.FilePicker()

        self.controls.append(self.path_field)
        self.controls.append(
            ft.TextButton(content="...", on_click=self._show_file_picker)
        )

    @property
    def path(self) -> str:
        return self.path_field.value  # type: ignore

    @path.setter
    def path(self, new_path: str) -> None:
        self.path_field.value = new_path

    def set_error(self, error_text: Optional[str]) -> None:
        self.path_field.error = error_text

    def remove_error(self) -> None:
        self.set_error(None)

    def _save_new_path(self, new_path: Optional[str]) -> None:
        if new_path:
            self.path_field.value = new_path

    async def _show_file_picker(self, event=None) -> None:
        path = Path(self.path)
        if not path.is_dir():
            path = get_top_dir(path)
        new_path = await self.file_picker.get_directory_path(
            _("Select folder"), str(path)
        )
        self._save_new_path(new_path)
