from pathlib import Path

import flet as ft

from data.mc_world import McSave
from data.controls.saves_view import SavesView


class McBackupper(ft.Row):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        self._init_page(page)
        self._fill_page()
        page.add(self)

    def _init_page(self, page: ft.Page):
        page.title = "McBackupper"
        page.window_width = 500
        page.window_height = 600
        page.update()

    def _fill_page(self):
        saves = McSave("saves")
        saves.load_from_path(Path(""))

        versions = McSave("versions")
        versions.load_from_path(Path(""))

        favourites = McSave("favourites")
        favourites.load_from_path(Path(""))
        self.controls = [
            ft.Column(
                [
                    SavesView(saves),
                    ft.Divider(1),
                    SavesView(versions),
                    ft.Divider(1),
                    SavesView(favourites),
                ],
                expand=True,
            ),
            ft.VerticalDivider(1),
        ]
