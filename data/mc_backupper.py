import flet as ft

from data.mc_world import McSave
from data.controls.saves_view import SavesView
from data.controls.world_view import WorldView
from data.settings import Settings
from data.dialogs.change_settings import ChangeSettings


class McBackupper(ft.Row):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.expand = True
        self.page: ft.Page = page
        self._init_page()
        self._fill_page()
        self.page.add(self)

    def _init_page(self) -> None:
        self.page.title = "McBackupper"
        self.page.window_width = 800
        self.page.window_height = 600
        self._init_bottom_app_bar()
        self.page.update()

    def _init_bottom_app_bar(self) -> None:
        self.page.bottom_appbar = ft.BottomAppBar(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.SETTINGS, on_click=ChangeSettings(self.page).show
                    ),
                ]
            ),
        )

    def _fill_page(self) -> None:
        mc_folder = Settings().get_mc_folder()

        saves = McSave("saves")
        saves.load_from_path(mc_folder.joinpath("saves"))

        versions = McSave("versions")
        versions.load_from_path(mc_folder.joinpath("versions"))

        world_view = WorldView(self.page)

        self.controls = [
            ft.Column(
                [
                    SavesView(saves, world_view.change_world),
                    SavesView(versions, world_view.change_world),
                ],
                width=250,
                scroll=ft.ScrollMode.AUTO,
            ),
            ft.VerticalDivider(1),
            world_view,
        ]
