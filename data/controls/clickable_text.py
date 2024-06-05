from typing import Optional, Callable

import flet as ft


class ClickableText(ft.Text):
    def __init__(
        self,
        on_click: Callable,
        size: Optional[int] = None,
        italic: Optional[bool] = None,
    ):
        super().__init__()
        self.spans: list[ft.TextSpan] = [
            ft.TextSpan(
                style=ft.TextStyle(size=size, italic=italic),
                on_click=lambda e: on_click(e.control.text),
            )
        ]

    @property
    def text(self):
        return self.data

    @text.setter
    def text(self, text: str):
        self.spans[0].text = text
