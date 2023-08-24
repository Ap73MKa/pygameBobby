import sys

from pygame import QUIT, Surface, SurfaceType, display, init
from pygame.display import set_caption, set_icon, set_mode
from pygame.event import get as events
from pygame.image import load
from pygame.time import Clock
from pygame.transform import scale

from src.config import configure
from src.misc import PathManager
from src.misc.sound_manager import SoundManager
from src.scene import StateManager


class Game:
    def __init__(self):
        self._running = True
        self.size = configure.W_WIDTH, configure.W_HEIGHT
        self.game_canvas = Surface((configure.WIDTH, configure.HEIGHT))
        self.screen = self.get_screen()
        self.clock = Clock()
        self.manager = StateManager()

    def get_screen(self) -> Surface | SurfaceType:
        init()
        set_caption("Bobby Carrot")
        set_icon(load(PathManager.get("assets/graphics/icon.png")))
        SoundManager().play_sound("background_music", -1)
        return set_mode(self.size)

    def handle_events(self) -> None:
        for event in events():
            self._running = event.type == QUIT
            self.manager.handle_event(event)

    def update(self, delta: float) -> None:
        self._running = self.manager.is_running()
        self.manager.update(delta)

    def render(self) -> None:
        self.manager.render(self.game_canvas)
        self.screen.blit(scale(self.game_canvas, self.size), (0, 0))
        display.update()

    def run(self) -> None:
        while self._running:
            delta = self.clock.tick(configure.FPS) / 1000.0
            self.handle_events()
            self.update(delta)
            self.render()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
