import os
from pico2d import load_wav
from sound_files import SOUND_FILES

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class SoundManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SoundManager, cls).__new__(cls)
            cls._instance.sounds = {}
        return cls._instance

    def load_all(self):
        for name, path in SOUND_FILES.items():
            full_path = os.path.join(BASE_DIR, path)
            if name not in self.sounds:
                self.sounds[name] = load_wav(full_path)

    def play(self, name, volume=64):
        if name in self.sounds:
            self.sounds[name].set_volume(volume) # 볼륨 설정 (0 ~ 128)
            self.sounds[name].play()
        else:
            pass

    def play_loop(self, name, volume=64):
        """배경음악을 무한 반복 재생"""
        if name in self.sounds:
            self.sounds[name].set_volume(volume)
            self.sounds[name].repeat_play()
        else:
            pass

    def stop(self, name):
        """사운드 정지"""
        if name in self.sounds:
            self.sounds[name].set_volume(0)

sound_manager = SoundManager()