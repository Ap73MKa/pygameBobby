from abc import ABC
from typing import Final
from pathlib import Path


class PathManager(ABC):
    ROOT: Final = Path(__file__).resolve().parent.parent.parent

    @classmethod
    def get(cls, path: str) -> str:
        return str(cls.ROOT.joinpath(path))

    @classmethod
    def get_folder(cls, path: str) -> list[Path]:
        return [f for f in Path(cls.get(path)).iterdir() if f.is_file()]
