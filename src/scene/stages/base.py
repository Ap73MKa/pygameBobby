from pygame.font import Font
from pygame.display import get_surface
from pygame.event import Event


class BaseState:
    def __init__(self) -> None:
        self.surface = get_surface()
        self.done = self.quit = False
        self.next_state = None
        self.screen_rect = get_surface().get_rect()
        self.persist = {}
        self.font = Font(None, 24)

    def startup(self, persistent: dict) -> None:
        self.persist = persistent

    def get_event(self, e: Event) -> None:
        pass

    def update(self, delta: float) -> None:
        pass

    def render(self) -> None:
        pass
