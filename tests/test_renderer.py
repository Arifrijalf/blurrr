
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from src.fotokitablur.renderer import EffectRenderer, HandLandmarkerDrawer
from src.fotokitablur.enums import GestureMode
import time

class MockFrame:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.data = np.zeros((height, width, 3), dtype=np.uint8)

    def shape(self):
        return (self.height, self.width, 3)

def test_effect_renderer_initialization():
    renderer = EffectRenderer()
    assert renderer._thumbs_anim_start == 0.0
    assert renderer._fist_anim_start == 0.0
    assert renderer._vsign_start_time == 0.0

def test_apply_v_sign_effect():
    renderer = EffectRenderer()
    frame = MockFrame()
    frame.data = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    renderer.reset_vsign_anim()
    time.sleep(0.1)  # Simulate some time passing
    
    result = renderer.apply_v_sign(frame.data)
    assert result is not None
    assert result.shape == frame.data.shape

def test_apply_thumbs_up_effect():
    renderer = EffectRenderer()
    frame = MockFrame()
    frame.data = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    result = renderer.apply_thumbs_up(frame.data, True)
    assert result is not None
    assert result.shape == frame.data.shape

def test_apply_fist_effect():
    renderer = EffectRenderer()
    frame = MockFrame()
    frame.data = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    result = renderer.apply_fist(frame.data, True)
    assert result is not None
    assert result.shape == frame.data.shape

def test_draw_status():
    renderer = EffectRenderer()
    frame = MockFrame()
    frame.data = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    renderer.draw_status(frame.data, GestureMode.NORMAL)
    renderer.draw_status(frame.data, GestureMode.V_SIGN)
    renderer.draw_status(frame.data, GestureMode.THUMBS_UP)
    renderer.draw_status(frame.data, GestureMode.FIST)

def test_draw_hint():
    renderer = EffectRenderer()
    frame = MockFrame()
    frame.data = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    renderer.draw_hint(frame.data)

class MockLandmarks:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def test_hand_landmarker_drawer():
    drawer = HandLandmarkerDrawer()
    frame = MockFrame()
    frame.data = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    landmarks = [MockLandmarks(0.5, 0.5) for _ in range(21)]
    drawer.draw_landmarks(frame.data, landmarks, 640, 480)