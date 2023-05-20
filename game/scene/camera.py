from pygame.surface import Surface
from pygame.sprite import Group
from pygame.math import Vector2

from game.objects import Player
from game.misc import Config


class CameraGroup(Group):
    def __init__(self):
        super().__init__()
        self.size = Vector2((Config.WIDTH, Config.HEIGHT))
        self.camera = self.size / 2
        self.camera_speed = 5
        self.offset = Vector2()
        self.render_texture = Surface(self.size)

    def __is_visible(self, sprite) -> bool:
        return (
            self.size.y + self.offset.y
            > sprite.rect.y
            > -Config.TITLE_SIZE - self.offset.y
            and self.size.x + self.offset.x
            > sprite.rect.x
            > -Config.TITLE_SIZE - self.offset.x
        )

    def __get_offset_sprites(self):
        return (
            (sprite, sprite.rect.topleft - self.offset)
            for sprite in self.sprites()
            if self.__is_visible(sprite)
        )

    def update_camera_pos(self, player: Player, corner: Vector2, delta: float):
        heading = player.rect.center - self.camera
        self.camera += heading * self.camera_speed * delta
        self.offset = self.camera - (self.size / 2)
        self.offset.x = max(0, min(int(self.offset.x), corner.x - self.size.x))
        self.offset.y = max(0, min(int(self.offset.y), corner.y - self.size.y))
        self.offset = round(self.offset)

    def custom_render(self, surface: Surface):
        self.render_texture.fill((0, 0, 0))
        for sprite, offset_pos in self.__get_offset_sprites():
            self.render_texture.blit(sprite.image, offset_pos)
        surface.blit(self.render_texture, (0, 0))
