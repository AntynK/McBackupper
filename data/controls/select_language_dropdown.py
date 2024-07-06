import flet as ft

from data.localization import Localization


class SelectLanguageDropdown(ft.Dropdown):
    def __init__(self, label: str):
        super().__init__(label=label)
        self.options = [
            ft.dropdown.Option(lang) for lang in Localization().available_languages
        ]
