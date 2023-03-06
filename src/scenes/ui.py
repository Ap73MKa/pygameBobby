import pygame.display
from pygame.transform import scale

from src.misc.config import Config
from src.misc.path import PathManager


class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.start_time = pygame.time.get_ticks()
        self.font = pygame.font.Font(
            PathManager.get("assets/graphics/hud/font.ttf"), 28
        )
        self.carrot_img = pygame.image.load(
            PathManager.get("assets/graphics/hud/carrot.png")
        )
        self.carrot_img = scale(
            self.carrot_img,
            (self.carrot_img.get_size()[0] * 3, self.carrot_img.get_size()[1] * 3),
        )
        self.shadow_offset = 4
        self.carrot_count = 0
        self.elapsed_time = 0
        self.timer_text = ""

    def set_start_time(self, time: int):
        self.elapsed_time = 0
        self.start_time = time

    def update(self, carrot_count: int):
        self.carrot_count = carrot_count
        self.elapsed_time += pygame.time.Clock().tick(60)
        minutes = int(self.elapsed_time / 60000)
        seconds = int((self.elapsed_time % 60000) / 1000)
        self.timer_text = "{:02d}:{:02d}".format(minutes, seconds)

    def render(self):
        self.display_surface.blit(
            self.font.render(self.timer_text, True, (0, 0, 0)),
            (20 + self.shadow_offset, 10 + self.shadow_offset),
        )
        self.display_surface.blit(
            self.font.render(self.timer_text, True, (255, 255, 255)), (20, 10)
        )
        if self.carrot_count <= 0:
            return

        self.display_surface.blit(
            self.carrot_img, (Config.WIDTH - Config.TITLE_SIZE, 5)
        )
        self.display_surface.blit(
            self.font.render(str(self.carrot_count), True, (0, 0, 0)),
            (
                Config.WIDTH - Config.TITLE_SIZE * 2 + self.shadow_offset,
                10 + self.shadow_offset,
            ),
        )

        self.display_surface.blit(
            self.font.render(str(self.carrot_count), True, (255, 255, 255)),
            (Config.WIDTH - Config.TITLE_SIZE * 2, 10),
        )
