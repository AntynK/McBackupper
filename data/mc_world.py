from typing import Union
from pathlib import Path


INPORTANT_WORLD_ITEMS = ("level.dat", "region", "data", "icon.png")


class McWorld:
    def __init__(self, path: Path) -> None:
        self.path: Path = path
        self.name: str = path.name

    @staticmethod
    def check_folder(folder: Path) -> bool:
        for item in INPORTANT_WORLD_ITEMS:
            if not folder.joinpath(item).exists():
                return False
        return True


class McVersion:
    def __init__(self, path: Path) -> None:
        self.worlds: list[McWorld] = []
        self.name = path.name
        self.path = path
        self.load_worlds()

    @staticmethod
    def check_folder(folder: Path) -> bool:
        return folder.joinpath("saves").is_dir()

    def load_worlds(self) -> None:
        for world_path in self.path.joinpath("saves").iterdir():
            world_path = self.path.joinpath(world_path)
            if McWorld.check_folder(world_path):
                self.worlds.append(McWorld(world_path))

    def valid(self) -> bool:
        return len(self.worlds) != 0


class McSave:
    def __init__(self, name: str) -> None:
        self.items: list[Union[McVersion, McWorld]] = []
        self.name = name

    def load_from_path(self, path: Path) -> None:
        if not path.is_dir():
            return
        for item in path.iterdir():
            item = path.joinpath(item)
            if loaded := self.load_item(item):
                self.items.append(loaded)

    def load_item(self, item: Path) -> Union[None, McWorld, McVersion]:
        if McWorld.check_folder(item):
            return McWorld(item)
        if McVersion.check_folder(item):
            version = McVersion(item)
            if version.valid():
                return version
