from pathlib import Path

from data.settings import Settings


def get_rel_world_path(world_path: Path) -> Path:
    """Return relative path to Minecraft folder. It is used to remove `.minecraft` from world path.

    Example `.minecraft/saves/NewWorld` converts to `saves/NewWorld`
    """

    return world_path.relative_to(Settings().get_mc_folder())


def convert_world_path_to_backup(world_path: Path) -> Path:
    """Convert world path(example `.minecraft/saves/NewWorld`) to path for backup folder(example `backups/saves/NewWrold`)."""

    return Settings().get_backup_folder().joinpath(get_rel_world_path(world_path))


def get_top_dir(path: Path) -> Path:
    return Path(*path.parts[:-1])


def is_mc_folder(folder: Path) -> bool:
    for sub_folder in ("saves", "versions"):
        if not folder.joinpath(sub_folder).is_dir():
            return False
    return True
