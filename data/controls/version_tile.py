from typing import Callable

import flet as ft

from data.mc_world import McVersion
from data.controls.world_tile import WorldTile


class VersionTile(ft.ExpansionTile):
    def __init__(self, version: McVersion, on_world_clicked: Callable) -> None:
        super().__init__()
        self.title = ft.Text(version.name)
        self.tile_padding = 20
        self.controls = [*self.render_worlds(version, on_world_clicked)]

    def render_worlds(
        self, version: McVersion, on_world_clicked: Callable
    ) -> list[ft.ListTile]:
        return [WorldTile(world, on_world_clicked) for world in version.worlds]
