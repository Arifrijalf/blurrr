import pytest
import time
from unittest.mock import MagicMock
from src.fotokitablur.calibration import CalibrationManager


class MockLandmark:
    def __init__(self, x, y, z=0.0):
        self.x = x
        self.y = y
        self.z = z


class TestCalibrationManager:
    def setup_method(self):
        import os
        self.test_file = "data/test_calibration.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.cal = CalibrationManager(calibration_file=self.test_file)

    def test_initial_state(self):
        assert self.cal.recording is False
        assert self.cal.current_gesture is None
        assert len(self.cal.templates) == 0

    def test_has_no_existing_calibration(self):
        assert self.cal.has_existing_calibration() is False

    def test_has_existing_calibration(self):
        self.cal.templates = {"V_SIGN": {"landmarks": [{"x": 0.5, "y": 0.5, "z": 0.0}] * 21, "sample_count": 10}}
        assert self.cal.has_existing_calibration() is True

    def test_start_calibration(self):
        step = self.cal.start_calibration()
        assert step == "V_SIGN"
        assert self.cal.current_step == 0

    def test_start_calibration_loads_existing(self):
        self.cal.templates = {"V_SIGN": {"landmarks": [{"x": 0.5, "y": 0.5, "z": 0.0}] * 21, "sample_count": 10}}
        step = self.cal.start_calibration()
        assert step == "V_SIGN"
        assert self.cal.has_existing_calibration() is True

    def test_current_step_name(self):
        self.cal.start_calibration()
        assert self.cal.current_step_name() == "V_SIGN"

    def test_start_recording_step(self):
        self.cal.start_calibration()
        self.cal.start_recording_step()
        assert self.cal.recording is True
        assert self.cal.current_gesture == "V_SIGN"

    def test_record_frame(self):
        self.cal.start_calibration()
        self.cal.start_recording_step()
        landmarks = [MockLandmark(i * 0.05, i * 0.02, i * 0.01) for i in range(21)]
        self.cal.record_frame(landmarks)
        assert len(self.cal.recorded_landmarks) == 1

    def test_record_frame_limit(self):
        self.cal.start_calibration()
        self.cal.start_recording_step()
        landmarks = [MockLandmark(i * 0.05, i * 0.02) for i in range(21)]
        for _ in range(100):
            self.cal.record_frame(landmarks)
        assert len(self.cal.recorded_landmarks) == 90

    def test_stop_recording_creates_template(self):
        self.cal.start_calibration()
        self.cal.start_recording_step()
        landmarks = [MockLandmark(0.5, 0.5, 0.0) for i in range(21)]
        for _ in range(20):
            self.cal.record_frame(landmarks)
        self.cal.stop_recording()
        assert "V_SIGN" in self.cal.templates
        assert self.cal.templates["V_SIGN"]["sample_count"] == 20

    def test_stop_recording_insufficient_samples(self):
        self.cal.start_calibration()
        self.cal.start_recording_step()
        landmarks = [MockLandmark(0.5, 0.5, 0.0) for i in range(21)]
        for _ in range(5):
            self.cal.record_frame(landmarks)
        self.cal.stop_recording()
        assert "V_SIGN" not in self.cal.templates

    def test_stop_recording_merges_with_existing(self):
        self.cal.start_calibration()
        self.cal.start_recording_step()
        old_landmarks = [{"x": 0.5, "y": 0.5, "z": 0.0}] * 21
        self.cal.templates["V_SIGN"] = {
            "landmarks": old_landmarks,
            "recorded_at": time.time(),
            "sample_count": 10
        }
        new_landmarks = [MockLandmark(0.6, 0.6, 0.0) for i in range(21)]
        for _ in range(10):
            self.cal.record_frame(new_landmarks)
        self.cal.stop_recording()
        assert self.cal.templates["V_SIGN"]["sample_count"] == 20
        assert self.cal.templates["V_SIGN"]["landmarks"][0]["x"] == pytest.approx(0.55, abs=0.001)

    def test_next_step(self):
        self.cal.start_calibration()
        next_step = self.cal.next_step()
        assert next_step == "THUMBS_UP"
        assert self.cal.current_step == 1

    def test_next_step_last(self):
        self.cal.start_calibration()
        self.cal.current_step = 2
        next_step = self.cal.next_step()
        assert next_step is None

    def test_save_and_load(self):
        self.cal.start_calibration()
        self.cal.start_recording_step()
        landmarks = [MockLandmark(0.5, 0.5, 0.0) for i in range(21)]
        for _ in range(20):
            self.cal.record_frame(landmarks)
        self.cal.stop_recording()
        self.cal.save()
        new_cal = CalibrationManager(calibration_file="data/test_calibration.json")
        assert new_cal.load() is True
        assert "V_SIGN" in new_cal.templates

    def test_match_gesture(self):
        self.cal.templates["V_SIGN"] = {
            "landmarks": [{"x": 0.5, "y": 0.5, "z": 0.0}] * 21,
            "recorded_at": time.time(),
            "sample_count": 10
        }
        result = self.cal.match_gesture([{"x": 0.5, "y": 0.5, "z": 0.0}] * 21)
        assert result == "V_SIGN"

    def test_match_gesture_no_match(self):
        self.cal.templates["V_SIGN"] = {
            "landmarks": [{"x": 0.1, "y": 0.1, "z": 0.0}] * 21,
            "recorded_at": time.time(),
            "sample_count": 10
        }
        result = self.cal.match_gesture([{"x": 0.9, "y": 0.9, "z": 0.0}] * 21)
        assert result is None

    def test_match_gesture_empty_templates(self):
        result = self.cal.match_gesture([{"x": 0.5, "y": 0.5, "z": 0.0}] * 21)
        assert result is None

    def test_calculate_similarity_identical(self):
        landmarks = [{"x": 0.5, "y": 0.5, "z": 0.0}] * 21
        score = self.cal._calculate_similarity(landmarks, landmarks)
        assert score == pytest.approx(1.0, abs=0.01)

    def test_calculate_similarity_different(self):
        a = [{"x": 0.1, "y": 0.1, "z": 0.0}] * 21
        b = [{"x": 0.9, "y": 0.9, "z": 0.0}] * 21
        score = self.cal._calculate_similarity(a, b)
        assert score == pytest.approx(0.0, abs=0.01)
