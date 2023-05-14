from pygame import mixer

from game.misc import SingletonMeta, PathManager


class SoundManager(metaclass=SingletonMeta):
    sounds: dict[str, mixer.Sound] = {}

    def __init__(self):
        mixer.init()
        self.load_sounds()

    def load_sounds(self) -> None:
        sound_folder = PathManager.get_all_files_by_ext("assets/sounds/", ['mp3', 'wav'])
        self.sounds = {file.stem: mixer.Sound(file) for file in sound_folder}

    def play_sound(self, sound_name: str, loops: int = 0) -> None:
        sound = self.__get_sound(sound_name)
        if sound:
            sound.play(loops)

    def stop_sound(self, sound_name: str, volume: float) -> None:
        sound = self.__get_sound(sound_name)
        if sound:
            sound.set_volume(volume)

    def set_volume(self, sound_name: str, volume: float) -> None:
        sound = self.__get_sound(sound_name)
        if sound:
            sound.set_volume(volume)

    def __get_sound(self, sound_name: str) -> mixer.Sound | None:
        return self.sounds.get(sound_name)
