from pygame import Surface
from pygame.event import Event

from .states import Gameplay, GameState, LevelTransition, Menu, Pause


class StateManager:
    def __init__(self):
        self.states = {
            GameState.MENU: Menu(),
            GameState.GAMEPLAY: Gameplay(),
            GameState.PAUSE: Pause(),
            GameState.TRANSITION: LevelTransition(),
        }
        self._running = True
        self.current_state = self.states[GameState.MENU]

    def _swap_state(self) -> None:
        persistent = self.current_state.persist
        self.current_state.done = False
        self.current_state = self.states[self.current_state.next_state]
        self.current_state.startup(persistent)

    def is_running(self) -> bool:
        return not self.current_state.quit

    def handle_event(self, event: Event) -> None:
        self.current_state.handle_event(event)

    def update(self, delta: float) -> None:
        if self.current_state.done:
            self._swap_state()
        self.current_state.update(delta)

    def render(self, game_screen: Surface) -> None:
        self.current_state.render(game_screen)
