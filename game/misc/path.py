import sys
from abc import ABC
from typing import Final
from pathlib import Path


def get_root():
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent


class PathManager(ABC):
    ROOT: Final = get_root()

    @classmethod
    def get(cls, path: str) -> str:
        return str(cls.ROOT.joinpath(path))

    @classmethod
    def get_folder(cls, path: str) -> list[Path]:
        return [f for f in Path(cls.get(path)).iterdir() if f.is_file()]
