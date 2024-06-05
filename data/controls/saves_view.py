from typing import Union, Callable

import flet as ft

from data.mc_world import McSave, McWorld, McVersion
from data.controls.world_tile import WorldTile
from data.controls.version_tile import VersionTile


class SavesView(ft.ExpansionTile):
    def __init__(self, save: McSave, on_world_clicked: Callable) -> None:
        super().__init__()
        self.title = ft.Text(save.name)
        self.controls = [
            *self.render_items(save, on_world_clicked),
        ]

    def render_items(
        self, save: McSave, on_world_clicked: Callable
    ) -> list[Union[WorldTile, VersionTile]]:
        result: list[Union[WorldTile, VersionTile]] = []
        for item in save.items:
            if converted := self.convertItem(item, on_world_clicked):
                result.append(converted)
        return result

    def convertItem(
        self, item: Union[McVersion, McWorld], on_world_clicked: Callable
    ) -> Union[WorldTile, VersionTile, None]:
        if isinstance(item, McWorld):
            return WorldTile(item, on_world_clicked)
        if isinstance(item, McVersion):
            return VersionTile(item, on_world_clicked)
