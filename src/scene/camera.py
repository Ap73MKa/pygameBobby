from pygame import Surface
from pygame.sprite import Sprite, Group
from pygame.math import Vector2

from src.objects.player import Player
from src.misc.config import Config


class CameraGroup(Group):
    def __init__(self):
        super().__init__()
        self.size = Vector2((Config.WIDTH, Config.HEIGHT))
        self.camera = Vector2(*(self.size // 2))
        self.offset = Vector2()

    def is_visible(self, sprite: Sprite) -> bool:
        return (
            self.size.y + self.offset.y
            > sprite.rect.y
            > -Config.TITLE_SIZE - self.offset.y
            and self.size.x + self.offset.x
            > sprite.rect.x
            > -Config.TITLE_SIZE - self.offset.x
        )

    def custom_update(self, player: Player, corner: Vector2, delta: float):
        heading = player.rect.center - self.camera
        self.camera += heading * 0.1 * 50 * delta
        self.offset = self.camera - (self.size / 2)

        self.offset.x = max(self.offset.x, 0)
        self.offset.y = max(self.offset.y, 0)
        self.offset.x = min(self.offset.x, corner.x - self.size.x)
        self.offset.y = min(self.offset.y, corner.y - self.size.y)

        self.offset.x = round(self.offset.x)
        self.offset.y = round(self.offset.y)

    def custom_render(self, game_screen: Surface):
        game_screen.fill("black")
        for sprite in self.sprites():
            if not self.is_visible(sprite):
                continue
            offset_pos = sprite.rect.topleft - self.offset
            game_screen.blit(sprite.image, offset_pos)
