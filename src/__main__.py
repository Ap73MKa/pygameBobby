import pygame as pg

from misc.config import Config
from src.scenes.scene import Scene


class Game:
    def __init__(self):
        self._running = True
        self.size = self.width, self.height = Config.WIDTH, Config.HEIGHT
        self.screen = self.on_init()
        self.clock = pg.time.Clock()
        self.scene = Scene()

    def on_init(self):
        pg.init()
        pg.display.set_caption('Bobby Carrot')
        return pg.display.set_mode(self.size, pg.DOUBLEBUF)

    def on_event(self):
        for event in pg.event.get():
            self._running = not event.type == pg.QUIT

    def on_update(self, delta):
        self.scene.update(delta)

    def on_render(self):
        self.scene.render()
        pg.display.update()

    def on_execute(self) -> None:
        delta = 0
        while self._running:
            self.on_event()
            self.on_update(delta)
            self.on_render()
            delta = self.clock.tick(Config.FPS) / 1000
        pg.quit()


if __name__ == '__main__':
    game = Game()
    game.on_execute()
