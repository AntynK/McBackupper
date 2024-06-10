import flet as ft


class Dialog(ft.AlertDialog):
    def __init__(self, page: ft.Page, title: str) -> None:
        super().__init__()
        self.title = ft.Text(title)
        self.page: ft.Page = page

    def close(self, event=None) -> None:
        self.open = False
        self.page.update()

    def show(self, event=None) -> None:
        self.page.dialog = self
        self.open = True
        self.page.update()
