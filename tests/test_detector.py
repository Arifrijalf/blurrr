
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.fotokitablur.detector import GestureDetector, GestureMode

class MockLandmark:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def create_landmarks(lm_list):
    return [MockLandmark(x, y) for x, y in lm_list]

def test_vsign_detection():
    detector = GestureDetector()
    landmarks = [
        MockLandmark(0.5, 0.5), # 0 WRIST
        MockLandmark(0.5, 0.4), # 1 THUMB_CMC
        MockLandmark(0.5, 0.3), # 2 THUMB_MCP
        MockLandmark(0.5, 0.2), # 3 THUMB_IP
        MockLandmark(0.5, 0.1), # 4 THUMB_TIP
        MockLandmark(0.4, 0.3), # 5 INDEX_MCP
        MockLandmark(0.4, 0.2), # 6 INDEX_PIP
        MockLandmark(0.4, 0.15), # 7 INDEX_DIP
        MockLandmark(0.4, 0.1), # 8 INDEX_TIP
        MockLandmark(0.5, 0.3), # 9 MIDDLE_MCP
        MockLandmark(0.5, 0.2), # 10 MIDDLE_PIP
        MockLandmark(0.5, 0.15), # 11 MIDDLE_DIP
        MockLandmark(0.5, 0.1), # 12 MIDDLE_TIP
        MockLandmark(0.6, 0.3), # 13 RING_MCP
        MockLandmark(0.6, 0.4), # 14 RING_PIP
        MockLandmark(0.6, 0.45), # 15 RING_DIP
        MockLandmark(0.6, 0.5), # 16 RING_TIP
        MockLandmark(0.7, 0.3), # 17 PINKY_MCP
        MockLandmark(0.7, 0.4), # 18 PINKY_PIP
        MockLandmark(0.7, 0.45), # 19 PINKY_DIP
        MockLandmark(0.7, 0.5), # 20 PINKY_TIP
    ]
    mode = detector.detect(landmarks)
    assert mode == GestureMode.V_SIGN

def test_vsign_with_ring_noise():
    detector = GestureDetector()
    landmarks = [
        MockLandmark(0.5, 0.5), # 0 WRIST
        MockLandmark(0.5, 0.4), # 1 THUMB_CMC
        MockLandmark(0.5, 0.3), # 2 THUMB_MCP
        MockLandmark(0.5, 0.2), # 3 THUMB_IP
        MockLandmark(0.5, 0.1), # 4 THUMB_TIP
        MockLandmark(0.4, 0.3), # 5 INDEX_MCP
        MockLandmark(0.4, 0.2), # 6 INDEX_PIP
        MockLandmark(0.4, 0.15), # 7 INDEX_DIP
        MockLandmark(0.4, 0.1), # 8 INDEX_TIP
        MockLandmark(0.5, 0.3), # 9 MIDDLE_MCP
        MockLandmark(0.5, 0.2), # 10 MIDDLE_PIP
        MockLandmark(0.5, 0.15), # 11 MIDDLE_DIP
        MockLandmark(0.5, 0.1), # 12 MIDDLE_TIP
        MockLandmark(0.6, 0.3), # 13 RING_MCP
        MockLandmark(0.6, 0.35), # 14 RING_PIP
        MockLandmark(0.6, 0.33), # 15 RING_DIP (slightly up - noise)
        MockLandmark(0.6, 0.30), # 16 RING_TIP (slightly up - noise)
        MockLandmark(0.7, 0.3), # 17 PINKY_MCP
        MockLandmark(0.7, 0.4), # 18 PINKY_PIP
        MockLandmark(0.7, 0.45), # 19 PINKY_DIP
        MockLandmark(0.7, 0.5), # 20 PINKY_TIP
    ]
    mode = detector.detect(landmarks)
    assert mode == GestureMode.V_SIGN

def test_vsign_with_pinky_noise():
    detector = GestureDetector()
    landmarks = [
        MockLandmark(0.5, 0.5), # 0 WRIST
        MockLandmark(0.5, 0.4), # 1 THUMB_CMC
        MockLandmark(0.5, 0.3), # 2 THUMB_MCP
        MockLandmark(0.5, 0.2), # 3 THUMB_IP
        MockLandmark(0.5, 0.1), # 4 THUMB_TIP
        MockLandmark(0.4, 0.3), # 5 INDEX_MCP
        MockLandmark(0.4, 0.2), # 6 INDEX_PIP
        MockLandmark(0.4, 0.15), # 7 INDEX_DIP
        MockLandmark(0.4, 0.1), # 8 INDEX_TIP
        MockLandmark(0.5, 0.3), # 9 MIDDLE_MCP
        MockLandmark(0.5, 0.2), # 10 MIDDLE_PIP
        MockLandmark(0.5, 0.15), # 11 MIDDLE_DIP
        MockLandmark(0.5, 0.1), # 12 MIDDLE_TIP
        MockLandmark(0.6, 0.3), # 13 RING_MCP
        MockLandmark(0.6, 0.4), # 14 RING_PIP
        MockLandmark(0.6, 0.45), # 15 RING_DIP
        MockLandmark(0.6, 0.5), # 16 RING_TIP
        MockLandmark(0.7, 0.3), # 17 PINKY_MCP
        MockLandmark(0.7, 0.35), # 18 PINKY_PIP
        MockLandmark(0.7, 0.33), # 19 PINKY_DIP (slightly up - noise)
        MockLandmark(0.7, 0.30), # 20 PINKY_TIP (slightly up - noise)
    ]
    mode = detector.detect(landmarks)
    assert mode == GestureMode.V_SIGN

def test_thumbs_up_detection():
    detector = GestureDetector()
    landmarks = [
        MockLandmark(0.5, 0.5), # WRIST
        MockLandmark(0.5, 0.4), # THUMB_CMC
        MockLandmark(0.5, 0.3), # THUMB_MCP
        MockLandmark(0.5, 0.2), # THUMB_IP
        MockLandmark(0.5, 0.1), # THUMB_TIP
        MockLandmark(0.4, 0.3), # INDEX_MCP
        MockLandmark(0.4, 0.4), # INDEX_PIP
        MockLandmark(0.4, 0.45), # INDEX_DIP
        MockLandmark(0.4, 0.5), # INDEX_TIP
        MockLandmark(0.5, 0.3), # MIDDLE_MCP
        MockLandmark(0.5, 0.4), # MIDDLE_PIP
        MockLandmark(0.5, 0.45), # MIDDLE_DIP
        MockLandmark(0.5, 0.5), # MIDDLE_TIP
        MockLandmark(0.6, 0.3), # RING_MCP
        MockLandmark(0.6, 0.4), # RING_PIP
        MockLandmark(0.6, 0.45), # RING_DIP
        MockLandmark(0.6, 0.5), # RING_TIP
        MockLandmark(0.7, 0.3), # PINKY_MCP
        MockLandmark(0.7, 0.4), # PINKY_PIP
        MockLandmark(0.7, 0.45), # PINKY_DIP
        MockLandmark(0.7, 0.5), # PINKY_TIP
    ]
    mode = detector.detect(landmarks)
    assert mode == GestureMode.THUMBS_UP

def test_thumbs_up_with_pinky_noise():
    detector = GestureDetector()
    landmarks = [
        MockLandmark(0.5, 0.5), # WRIST
        MockLandmark(0.5, 0.4), # THUMB_CMC
        MockLandmark(0.5, 0.3), # THUMB_MCP
        MockLandmark(0.5, 0.2), # THUMB_IP
        MockLandmark(0.5, 0.1), # THUMB_TIP
        MockLandmark(0.4, 0.3), # INDEX_MCP
        MockLandmark(0.4, 0.4), # INDEX_PIP
        MockLandmark(0.4, 0.45), # INDEX_DIP
        MockLandmark(0.4, 0.5), # INDEX_TIP
        MockLandmark(0.5, 0.3), # MIDDLE_MCP
        MockLandmark(0.5, 0.4), # MIDDLE_PIP
        MockLandmark(0.5, 0.45), # MIDDLE_DIP
        MockLandmark(0.5, 0.5), # MIDDLE_TIP
        MockLandmark(0.6, 0.3), # RING_MCP
        MockLandmark(0.6, 0.4), # RING_PIP
        MockLandmark(0.6, 0.45), # RING_DIP
        MockLandmark(0.6, 0.5), # RING_TIP
        MockLandmark(0.7, 0.3), # PINKY_MCP
        MockLandmark(0.7, 0.35), # PINKY_PIP
        MockLandmark(0.7, 0.33), # PINKY_DIP (slightly up - noise)
        MockLandmark(0.7, 0.30), # PINKY_TIP (slightly up - noise)
    ]
    mode = detector.detect(landmarks)
    assert mode == GestureMode.THUMBS_UP

def test_fist_detection():
    detector = GestureDetector()
    landmarks = [
        MockLandmark(0.5, 0.5), # WRIST
        MockLandmark(0.5, 0.4), # THUMB_CMC
        MockLandmark(0.5, 0.35), # THUMB_MCP
        MockLandmark(0.5, 0.33), # THUMB_IP
        MockLandmark(0.5, 0.32), # THUMB_TIP (same level as index_mcp = not thumbs up)
        MockLandmark(0.4, 0.3), # INDEX_MCP
        MockLandmark(0.4, 0.4), # INDEX_PIP
        MockLandmark(0.4, 0.45), # INDEX_DIP
        MockLandmark(0.4, 0.5), # INDEX_TIP
        MockLandmark(0.5, 0.3), # MIDDLE_MCP
        MockLandmark(0.5, 0.4), # MIDDLE_PIP
        MockLandmark(0.5, 0.45), # MIDDLE_DIP
        MockLandmark(0.5, 0.5), # MIDDLE_TIP
        MockLandmark(0.6, 0.3), # RING_MCP
        MockLandmark(0.6, 0.4), # RING_PIP
        MockLandmark(0.6, 0.45), # RING_DIP
        MockLandmark(0.6, 0.5), # RING_TIP
        MockLandmark(0.7, 0.3), # PINKY_MCP
        MockLandmark(0.7, 0.4), # PINKY_PIP
        MockLandmark(0.7, 0.45), # PINKY_DIP
        MockLandmark(0.7, 0.5), # PINKY_TIP
    ]
    mode = detector.detect(landmarks)
    assert mode == GestureMode.FIST

def test_fist_with_ring_noise():
    detector = GestureDetector()
    landmarks = [
        MockLandmark(0.5, 0.5), # WRIST
        MockLandmark(0.5, 0.4), # THUMB_CMC
        MockLandmark(0.5, 0.35), # THUMB_MCP
        MockLandmark(0.5, 0.33), # THUMB_IP
        MockLandmark(0.5, 0.32), # THUMB_TIP (same level as index_mcp)
        MockLandmark(0.4, 0.3), # INDEX_MCP
        MockLandmark(0.4, 0.4), # INDEX_PIP
        MockLandmark(0.4, 0.45), # INDEX_DIP
        MockLandmark(0.4, 0.5), # INDEX_TIP
        MockLandmark(0.5, 0.3), # MIDDLE_MCP
        MockLandmark(0.5, 0.4), # MIDDLE_PIP
        MockLandmark(0.5, 0.45), # MIDDLE_DIP
        MockLandmark(0.5, 0.5), # MIDDLE_TIP
        MockLandmark(0.6, 0.3), # RING_MCP
        MockLandmark(0.6, 0.35), # RING_PIP
        MockLandmark(0.6, 0.33), # RING_DIP (slightly up - noise)
        MockLandmark(0.6, 0.30), # RING_TIP (slightly up - noise)
        MockLandmark(0.7, 0.3), # PINKY_MCP
        MockLandmark(0.7, 0.4), # PINKY_PIP
        MockLandmark(0.7, 0.45), # PINKY_DIP
        MockLandmark(0.7, 0.5), # PINKY_TIP
    ]
    mode = detector.detect(landmarks)
    assert mode == GestureMode.FIST

def test_normal_detection():
    detector = GestureDetector()
    landmarks = [
        MockLandmark(0.5, 0.5), # 0 WRIST
        MockLandmark(0.5, 0.4), # 1 THUMB_CMC
        MockLandmark(0.5, 0.35), # 2 THUMB_MCP
        MockLandmark(0.5, 0.32), # 3 THUMB_IP
        MockLandmark(0.5, 0.30), # 4 THUMB_TIP (not high above index mcp)
        MockLandmark(0.4, 0.3), # 5 INDEX_MCP
        MockLandmark(0.4, 0.25), # 6 INDEX_PIP (tip above dip = finger up)
        MockLandmark(0.4, 0.22), # 7 INDEX_DIP
        MockLandmark(0.4, 0.2), # 8 INDEX_TIP
        MockLandmark(0.5, 0.3), # 9 MIDDLE_MCP
        MockLandmark(0.5, 0.35), # 10 MIDDLE_PIP (tip below dip = finger down)
        MockLandmark(0.5, 0.38), # 11 MIDDLE_DIP
        MockLandmark(0.5, 0.4), # 12 MIDDLE_TIP
        MockLandmark(0.6, 0.3), # 13 RING_MCP
        MockLandmark(0.6, 0.35), # 14 RING_PIP (tip below dip = finger down)
        MockLandmark(0.6, 0.38), # 15 RING_DIP
        MockLandmark(0.6, 0.4), # 16 RING_TIP
        MockLandmark(0.7, 0.3), # 17 PINKY_MCP
        MockLandmark(0.7, 0.35), # 18 PINKY_PIP (tip below dip = finger down)
        MockLandmark(0.7, 0.38), # 19 PINKY_DIP
        MockLandmark(0.7, 0.4), # 20 PINKY_TIP
    ]
    mode = detector.detect(landmarks)
    assert mode == GestureMode.NORMAL


# === FLIPPED HAND TESTS (back of hand visible, fingers point down) ===

def test_vsign_flipped():
    detector = GestureDetector()
    landmarks = [
        MockLandmark(0.5, 0.1), # 0 WRIST (top)
        MockLandmark(0.5, 0.2), # 1 THUMB_CMC
        MockLandmark(0.5, 0.3), # 2 THUMB_MCP
        MockLandmark(0.5, 0.4), # 3 THUMB_IP
        MockLandmark(0.5, 0.5), # 4 THUMB_TIP
        MockLandmark(0.4, 0.3), # 5 INDEX_MCP
        MockLandmark(0.4, 0.4), # 6 INDEX_PIP
        MockLandmark(0.4, 0.45), # 7 INDEX_DIP
        MockLandmark(0.4, 0.5), # 8 INDEX_TIP (tip below pip = extended when flipped)
        MockLandmark(0.5, 0.3), # 9 MIDDLE_MCP
        MockLandmark(0.5, 0.4), # 10 MIDDLE_PIP
        MockLandmark(0.5, 0.45), # 11 MIDDLE_DIP
        MockLandmark(0.5, 0.5), # 12 MIDDLE_TIP (tip below pip = extended when flipped)
        MockLandmark(0.6, 0.3), # 13 RING_MCP
        MockLandmark(0.6, 0.3), # 14 RING_PIP
        MockLandmark(0.6, 0.3), # 15 RING_DIP
        MockLandmark(0.6, 0.3), # 16 RING_TIP (tip above pip = folded)
        MockLandmark(0.7, 0.3), # 17 PINKY_MCP
        MockLandmark(0.7, 0.3), # 18 PINKY_PIP
        MockLandmark(0.7, 0.3), # 19 PINKY_DIP
        MockLandmark(0.7, 0.3), # 20 PINKY_TIP (tip above pip = folded)
    ]
    mode = detector.detect(landmarks)
    assert mode == GestureMode.V_SIGN


def test_thumbs_up_flipped():
    detector = GestureDetector()
    landmarks = [
        MockLandmark(0.5, 0.1), # 0 WRIST (top)
        MockLandmark(0.5, 0.2), # 1 THUMB_CMC
        MockLandmark(0.5, 0.3), # 2 THUMB_MCP
        MockLandmark(0.5, 0.4), # 3 THUMB_IP
        MockLandmark(0.5, 0.5), # 4 THUMB_TIP (pointing down = extended when flipped)
        MockLandmark(0.4, 0.3), # 5 INDEX_MCP
        MockLandmark(0.4, 0.3), # 6 INDEX_PIP
        MockLandmark(0.4, 0.3), # 7 INDEX_DIP
        MockLandmark(0.4, 0.3), # 8 INDEX_TIP (tip at pip level = folded)
        MockLandmark(0.5, 0.3), # 9 MIDDLE_MCP
        MockLandmark(0.5, 0.3), # 10 MIDDLE_PIP
        MockLandmark(0.5, 0.3), # 11 MIDDLE_DIP
        MockLandmark(0.5, 0.3), # 12 MIDDLE_TIP (tip at pip level = folded)
        MockLandmark(0.6, 0.3), # 13 RING_MCP
        MockLandmark(0.6, 0.3), # 14 RING_PIP
        MockLandmark(0.6, 0.3), # 15 RING_DIP
        MockLandmark(0.6, 0.3), # 16 RING_TIP
        MockLandmark(0.7, 0.3), # 17 PINKY_MCP
        MockLandmark(0.7, 0.3), # 18 PINKY_PIP
        MockLandmark(0.7, 0.3), # 19 PINKY_DIP
        MockLandmark(0.7, 0.3), # 20 PINKY_TIP
    ]
    mode = detector.detect(landmarks)
    assert mode == GestureMode.THUMBS_UP


def test_fist_flipped():
    detector = GestureDetector()
    landmarks = [
        MockLandmark(0.5, 0.1), # 0 WRIST (top)
        MockLandmark(0.5, 0.2), # 1 THUMB_CMC
        MockLandmark(0.5, 0.3), # 2 THUMB_MCP
        MockLandmark(0.5, 0.31), # 3 THUMB_IP
        MockLandmark(0.5, 0.31), # 4 THUMB_TIP (same level as mcp = folded)
        MockLandmark(0.4, 0.3), # 5 INDEX_MCP
        MockLandmark(0.4, 0.3), # 6 INDEX_PIP
        MockLandmark(0.4, 0.3), # 7 INDEX_DIP
        MockLandmark(0.4, 0.3), # 8 INDEX_TIP
        MockLandmark(0.5, 0.3), # 9 MIDDLE_MCP
        MockLandmark(0.5, 0.3), # 10 MIDDLE_PIP
        MockLandmark(0.5, 0.3), # 11 MIDDLE_DIP
        MockLandmark(0.5, 0.3), # 12 MIDDLE_TIP
        MockLandmark(0.6, 0.3), # 13 RING_MCP
        MockLandmark(0.6, 0.3), # 14 RING_PIP
        MockLandmark(0.6, 0.3), # 15 RING_DIP
        MockLandmark(0.6, 0.3), # 16 RING_TIP
        MockLandmark(0.7, 0.3), # 17 PINKY_MCP
        MockLandmark(0.7, 0.3), # 18 PINKY_PIP
        MockLandmark(0.7, 0.3), # 19 PINKY_DIP
        MockLandmark(0.7, 0.3), # 20 PINKY_TIP
    ]
    mode = detector.detect(landmarks)
    assert mode == GestureMode.FIST


def test_open_palm_is_normal():
    detector = GestureDetector()
    landmarks = [
        MockLandmark(0.5, 0.5), # 0 WRIST
        MockLandmark(0.5, 0.4), # 1 THUMB_CMC
        MockLandmark(0.5, 0.3), # 2 THUMB_MCP
        MockLandmark(0.5, 0.2), # 3 THUMB_IP
        MockLandmark(0.5, 0.1), # 4 THUMB_TIP
        MockLandmark(0.4, 0.3), # 5 INDEX_MCP
        MockLandmark(0.4, 0.2), # 6 INDEX_PIP
        MockLandmark(0.4, 0.15), # 7 INDEX_DIP
        MockLandmark(0.4, 0.1), # 8 INDEX_TIP (up)
        MockLandmark(0.5, 0.3), # 9 MIDDLE_MCP
        MockLandmark(0.5, 0.2), # 10 MIDDLE_PIP
        MockLandmark(0.5, 0.15), # 11 MIDDLE_DIP
        MockLandmark(0.5, 0.1), # 12 MIDDLE_TIP (up)
        MockLandmark(0.6, 0.3), # 13 RING_MCP
        MockLandmark(0.6, 0.2), # 14 RING_PIP
        MockLandmark(0.6, 0.15), # 15 RING_DIP
        MockLandmark(0.6, 0.1), # 16 RING_TIP (up)
        MockLandmark(0.7, 0.3), # 17 PINKY_MCP
        MockLandmark(0.7, 0.2), # 18 PINKY_PIP
        MockLandmark(0.7, 0.15), # 19 PINKY_DIP
        MockLandmark(0.7, 0.1), # 20 PINKY_TIP (up)
    ]
    mode = detector.detect(landmarks)
    assert mode == GestureMode.NORMAL
