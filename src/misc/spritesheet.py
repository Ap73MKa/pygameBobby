from pygame import image
from pygame.surface import Surface


class SpriteSheet:
    def __init__(self, sprite_path: str, sprite_size: tuple | None = None):
        self.__all_frames = self.__get_all_frames(
            image.load(sprite_path).convert_alpha(), sprite_size[0], sprite_size[1]
        )

    def __getitem__(self, item: int) -> tuple:
        return self.__all_frames[item]

    def __len__(self) -> int:
        return len(self.__all_frames)

    @staticmethod
    def __get_all_frames(img: Surface, x, y) -> tuple:
        if not (x and y):
            raise Exception("sprite_size can not be equal 0")

        frames = []
        for _y in range(img.get_height() // y):
            local = [
                img.subsurface((_x * x, y * _y, x, y))
                for _x in range(img.get_width() // x)
            ]
            frames.append(tuple(local))
        return tuple(frames)
