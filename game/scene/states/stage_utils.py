from enum import IntEnum, auto


class GameState(IntEnum):
    MENU = auto()
    GAMEPLAY = auto()
    PAUSE = auto()
    TRANSITION = auto()
