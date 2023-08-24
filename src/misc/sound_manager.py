from pygame import mixer

from src.misc import PathManager, SingletonMeta


class SoundManager(metaclass=SingletonMeta):
    def __init__(self):
        mixer.init()
        self.sounds: dict[str, mixer.Sound] = self.load_sounds()

    @staticmethod
    def load_sounds() -> dict[str, mixer.Sound]:
        sound_folder = PathManager.get_all_files_by_ext(
            "assets/sounds/", ["mp3", "wav"]
        )
        return {file.stem: mixer.Sound(file) for file in sound_folder}

    def play_sound(self, sound_name: str, loops: int = 0) -> None:
        if sound := self.__get_sound(sound_name):
            sound.play(loops)

    def stop_sound(self, sound_name: str) -> None:
        if sound := self.__get_sound(sound_name):
            sound.stop()

    def set_volume(self, sound_name: str, volume: float) -> None:
        if sound := self.__get_sound(sound_name):
            sound.set_volume(volume)

    def __get_sound(self, sound_name: str) -> mixer.Sound | None:
        return self.sounds.get(sound_name)
