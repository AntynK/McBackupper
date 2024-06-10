import flet as ft

from data.mc_world import McWorld
from data.utils import open_with_explorer
from data.controls.backups_editor import BackupsEditor
from data.controls.clickable_text import ClickableText


class WorldView(ft.Column):
    def __init__(self, page: ft.Page) -> None:
        super().__init__()
        self.page = page
        self.world_name_text = ft.Text(weight=ft.FontWeight.BOLD, size=20)
        self.world_path_text = ClickableText(
            on_click=open_with_explorer, size=15, italic=True
        )

        self.backups_view = BackupsEditor(page)
        self.controls = [self.world_name_text, self.world_path_text, self.backups_view]

    def change_world(self, world: McWorld) -> None:
        self.world_name_text.value = world.name
        self.world_path_text.text = str(world.path)
        self.backups_view.change_world(world)
        self.update()
