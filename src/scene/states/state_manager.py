from pygame import Surface

from src.scene.states.gameplay import Gameplay
from src.scene.states.menu import Menu
from src.scene.states.pause import Pause
from src.scene.states.stage_utils import GameState


class StateManager:
    def __init__(self):
        self.stages = {
            GameState.MENU: Menu(),
            GameState.GAMEPLAY: Gameplay(),
            GameState.PAUSE: Pause(),
        }
        self._running = True
        self.state = self.stages[GameState.MENU]

    def is_running(self):
        return not self.state.quit

    def check_state(self):
        if self.state.done:
            persistent = self.state.persist
            self.state.done = False
            self.state = self.stages[self.state.next_state]
            self.state.startup(persistent)

    def render(self, game_screen: Surface):
        self.state.render(game_screen)

    def get_event(self, event):
        self.state.get_event(event)

    def update(self, delta: float):
        self.check_state()
        self.state.update(delta)
