import flet as ft

from data.mc_world import McWorld


class WorldTile(ft.ListTile):
    def __init__(self, world: McWorld) -> None:
        super().__init__()
        self.content_padding = ft.Padding(20, 0, 0, 0)
        self.title = ft.Text(world.name)
        self.data = world
