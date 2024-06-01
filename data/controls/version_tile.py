import flet as ft

from data.mc_world import McVersion
from data.controls.world_tile import WorldTile


class VersionTile(ft.Container):
    def __init__(self, version: McVersion) -> None:
        super().__init__()

        self.content: ft.Control = ft.Column(
            [
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            version.name,
                            on_click=self.hide,
                            style=ft.TextStyle(
                                weight=ft.FontWeight.BOLD, size=15, italic=True
                            ),
                        )
                    ]
                ),
                *self.render_worlds(version),
            ]
        )

    def hide(self, e):
        for control in self.content.controls:
            if isinstance(control, ft.Text):
                continue
            control.visible = not control.visible
        self.update()

    def render_worlds(self, version: McVersion) -> list[ft.ListTile]:
        return [WorldTile(world) for world in version.worlds]
