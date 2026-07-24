import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.fotokitablur.audio import AudioManager

def test_audio_manager_initialization():
    audio = AudioManager()
    # _initialized depends on whether pygame is available
    # When pygame is installed, _initialized will be True
    assert audio._tracks == {}
    assert audio._channels == {}

def test_audio_manager_load_noop():
    # Test load when _initialized is False (no pygame)
    audio = AudioManager()
    audio._initialized = False
    audio.load("test", "nonexistent.mp3")
    assert "test" not in audio._tracks

def test_audio_manager_play_stop():
    audio = AudioManager()
    audio._initialized = False
    # Should be no-ops when not initialized
    audio.play("test")
    audio.stop("test")
    audio.stop_all()
