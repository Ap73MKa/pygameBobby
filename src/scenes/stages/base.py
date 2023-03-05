from pygame.font import Font
from pygame.display import get_surface
from pygame import event


class BaseState:
    def __init__(self):
        self.surface = get_surface()
        self.done = self.quit = False
        self.next_state = None
        self.screen_rect = get_surface().get_rect()
        self.persist = {}
        self.font = Font(None, 24)

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event: event):
        pass

    def update(self, delta: float):
        pass

    def render(self):
        pass
