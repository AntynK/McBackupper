import gettext
from enum import Enum
from pathlib import Path
from typing import Callable

from data.settings import Settings


LOCALE_DIR = Path("assets", "locale")


class Domains(Enum):
    DIALOGS = "dialogs"
    CONTROLS = "controls"


class Localization:
    __INSTANCE = None
    __INITIALIZED = False

    def __new__(cls):
        if Localization.__INSTANCE is None:
            Localization.__INSTANCE = super().__new__(cls)
        return Localization.__INSTANCE

    def __init__(self) -> None:
        if Localization.__INITIALIZED:
            return
        self.current_language = Settings().get_language()
        self.get_available_languages()

    def get_available_languages(self):
        self.available_languages: list[str] = []

        for lang in Path(LOCALE_DIR).iterdir():
            self.available_languages.append(lang.name)
            for domain in Domains:
                if gettext.find(domain.value, LOCALE_DIR, [lang.name]) is None:
                    self.available_languages.remove(lang.name)
                    break

    def get_handler(self, domain: Domains) -> Callable:
        if self.current_language not in self.available_languages:
            return gettext.gettext
        return gettext.translation(
            domain.value, LOCALE_DIR, [self.current_language]
        ).gettext
