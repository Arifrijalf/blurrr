from src.fotokitablur.constants import MUSIC_PATH, MUSIC_PATH_2

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


class AudioManager:
    def __init__(self):
        self._initialized = False
        self._tracks: dict[str, "pygame.mixer.Sound"] = {}
        self._channels: dict[str, "pygame.mixer.Channel | None"] = {}

        if not PYGAME_AVAILABLE:
            return

        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self._initialized = True
        except Exception as e:
            print(f"[AudioManager] Init failed: {e}")

    def load(self, name: str, path: str):
        if not self._initialized:
            return
        try:
            self._tracks[name] = pygame.mixer.Sound(path)
            self._channels[name] = None
        except Exception as e:
            print(f"[AudioManager] Failed to load '{path}': {e}")

    def play(self, name: str, loop: bool = True):
        if not self._initialized or name not in self._tracks:
            return
        if self._channels.get(name) and self._channels[name].get_busy():
            return
        try:
            ch = self._tracks[name].play(-1 if loop else 0)
            self._channels[name] = ch
        except Exception as e:
            print(f"[AudioManager] Playback error '{name}': {e}")

    def stop(self, name: str):
        if not self._initialized:
            return
        ch = self._channels.get(name)
        if ch and ch.get_busy():
            ch.stop()
            self._channels[name] = None

    def stop_all(self):
        if not self._initialized:
            return
        for name in list(self._channels.keys()):
            self.stop(name)