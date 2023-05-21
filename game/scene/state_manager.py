from pygame import Surface
from pygame.event import Event

from game.scene.states import Menu, Pause, GameState, Gameplay, LevelTransition


class StateManager:
    def __init__(self):
        self.stages = {
            GameState.MENU: Menu(),
            GameState.GAMEPLAY: Gameplay(),
            GameState.PAUSE: Pause(),
            GameState.TRANSITION: LevelTransition(),
        }
        self._running = True
        self.state = self.stages[GameState.MENU]

    def __check_state(self):
        if self.state.done:
            persistent = self.state.persist
            self.state.done = False
            self.state = self.stages[self.state.next_state]
            self.state.startup(persistent)

    def is_running(self):
        return not self.state.quit

    def handle_event(self, event: Event) -> None:
        self.state.handle_event(event)

    def update(self, delta: float) -> None:
        self.__check_state()
        self.state.update(delta)

    def render(self, game_screen: Surface) -> None:
        self.state.render(game_screen)
