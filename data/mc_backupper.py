import flet as ft

from data.mc_world import McSave
from data.controls.saves_view import SavesView
from data.controls.world_view import WorldView
from data.settings import Settings
from data.dialogs.change_settings import ChangeSettings
from data.localization import Localization, Domains

_ = Localization().get_handler(Domains.CONTROLS)


class McBackupper(ft.Row):
    def __init__(self, page: ft.Page) -> None:
        super().__init__(expand=True)
        self._init_page(page)
        page.add(self)

    def did_mount(self) -> None:
        self._init_bottom_app_bar()
        self._fill_page()

    def _init_page(self, page: ft.Page) -> None:
        page.title = _("McBackupper")
        page.width = 800
        page.height = 600
        page.update()

    def _init_bottom_app_bar(self) -> None:
        self.page.bottom_appbar = ft.BottomAppBar(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.Icons.SETTINGS,
                        on_click=lambda e: self.page.show_dialog(ChangeSettings()),
                    ),
                ]
            ),
        )

    def _fill_page(self) -> None:
        mc_folder = Settings().get_mc_folder()

        saves = McSave(_("saves"))
        saves.load_from_path(mc_folder.joinpath("saves"))

        versions = McSave(_("versions"))
        versions.load_from_path(mc_folder.joinpath("versions"))

        world_view = WorldView()

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
