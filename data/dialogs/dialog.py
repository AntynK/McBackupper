import flet as ft


class Dialog(ft.AlertDialog):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.title = ft.Text(title)
