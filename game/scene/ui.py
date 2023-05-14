import pygame.display
from pygame import Surface

from game.misc import Config, PathManager


class UI:
    def __init__(self) -> None:
        self.start_time = pygame.time.get_ticks()
        self.font = pygame.font.Font(
            PathManager.get("assets/graphics/hud/font.ttf"), 10
        )
        self.carrot_img = pygame.image.load(
            PathManager.get("assets/graphics/hud/carrot.png")
        )
        self.shadow_offset = 1
        self.carrot_count = 0
        self.elapsed_time = 0
        self.timer_text = ""

    def set_start_time(self, time: int) -> None:
        self.elapsed_time = 0
        self.start_time = time

    def update(self, carrot_count: int) -> None:
        self.carrot_count = carrot_count
        self.elapsed_time += pygame.time.Clock().tick(Config.FPS)
        minutes = int(self.elapsed_time / 60000)
        seconds = int((self.elapsed_time % 60000) / 1000)
        self.timer_text = f"{minutes:02d}:{seconds:02d}"

    def render(self, game_screen: Surface) -> None:
        game_screen.blit(
            self.font.render(self.timer_text, False, (0, 0, 0)),
            (2 + self.shadow_offset, 2 + self.shadow_offset),
        )
        game_screen.blit(
            self.font.render(self.timer_text, False, (255, 255, 255)), (2, 2)
        )
        if self.carrot_count <= 0:
            return

        game_screen.blit(self.carrot_img, (Config.WIDTH - Config.TITLE_SIZE, 2))
        game_screen.blit(
            self.font.render(str(self.carrot_count), False, (0, 0, 0)),
            (
                Config.WIDTH - Config.TITLE_SIZE * 2 + self.shadow_offset,
                2 + self.shadow_offset,
            ),
        )

        game_screen.blit(
            self.font.render(str(self.carrot_count), False, (255, 255, 255)),
            (Config.WIDTH - Config.TITLE_SIZE * 2, 2),
        )
