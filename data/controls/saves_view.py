from typing import Union

import flet as ft

from data.mc_world import McSave, McWorld, McVersion
from data.controls.world_tile import WorldTile
from data.controls.version_tile import VersionTile


class SavesView(ft.Column):
    def __init__(self, save: McSave) -> None:
        super().__init__(expand=True)
        self.controls = [
            ft.Text(
                spans=[
                    ft.TextSpan(
                        save.name,
                        on_click=self.hide,
                        style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=20),
                    )
                ]
            ),
            ft.Column(
                [
                    *self.render_items(save),
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            ),
        ]

    def hide(self, e):
        for control in self.controls[1].controls:
            if isinstance(control, ft.Text):
                continue
            control.visible = not control.visible
        self.update()

    def render_items(self, save: McSave) -> list[Union[WorldTile, VersionTile]]:
        result: list[Union[WorldTile, VersionTile]] = []
        for item in save.items:
            if converted := self.convertItem(item):
                result.append(converted)
        return result

    def convertItem(
        self, item: Union[McVersion, McWorld]
    ) -> Union[WorldTile, VersionTile, None]:
        if isinstance(item, McWorld):
            return WorldTile(item)
        if isinstance(item, McVersion):
            return VersionTile(item)
