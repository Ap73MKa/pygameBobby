import pygame as pg
from pygame import Surface, SurfaceType
from pygame.display import set_caption, set_mode, set_icon
from pygame.event import get as events
from pygame.image import load
from pygame.time import Clock
from pygame.transform import scale
from pygame import mixer

from game.misc import Config, PathManager
from game.scene import StateManager


class Game:
    def __init__(self) -> None:
        self._running = True
        self.size = self.width, self.height = Config.W_WIDTH, Config.W_HEIGHT
        self.game_canvas = Surface((Config.WIDTH, Config.HEIGHT))
        self.screen = self.on_init()
        self.manager = StateManager()
        self.clock = Clock()
        mixer.music.load(PathManager.get('assets/sounds/background_music.mp3'))
        mixer.music.play(-1)

    def on_init(self) -> Surface | SurfaceType:
        pg.init()
        set_caption("Bobby Carrot")
        set_icon(load(PathManager.get("assets/graphics/icon.png")))
        return set_mode(self.size, pg.DOUBLEBUF)

    def on_event(self) -> None:
        for event in events():
            self._running = event.type == pg.QUIT
            self.manager.get_event(event)

    def on_update(self, delta) -> None:
        self._running = self.manager.is_running()
        self.manager.update(delta)

    def on_render(self) -> None:
        self.manager.render(self.game_canvas)
        self.screen.blit(
            scale(self.game_canvas, (Config.W_WIDTH, Config.W_HEIGHT)), (0, 0)
        )
        pg.display.update()

    def on_execute(self) -> None:
        delta = 0.0
        while self._running:
            self.on_event()
            self.on_update(delta)
            self.on_render()
            delta = self.clock.tick(Config.FPS) / 1000
        pg.quit()


if __name__ == "__main__":
    game = Game()
    game.on_execute()
