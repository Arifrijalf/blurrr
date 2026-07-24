import json
import os
import time
from collections import deque
from pathlib import Path

class CalibrationManager:
    def __init__(self, calibration_file="data/calibration.json"):
        self.calibration_file = calibration_file
        self.templates = {}
        self.recording = False
        self.current_gesture = None
        self.start_time = 0
        self.recorded_landmarks = deque(maxlen=90)
        self.calibration_steps = ["V_SIGN", "THUMBS_UP", "FIST"]
        self.current_step = 0
        self.step_start_time = 0

    def has_existing_calibration(self):
        return len(self.templates) > 0

    def start_calibration(self):
        self.current_step = 0
        if not self.templates:
            self.load()
        return self.calibration_steps[self.current_step]

    def current_step_name(self):
        return self.calibration_steps[self.current_step]

    def start_recording_step(self):
        gesture = self.calibration_steps[self.current_step]
        self.recording = True
        self.current_gesture = gesture
        self.recorded_landmarks.clear()
        self.start_time = time.time()

    def record_frame(self, landmarks):
        if self.recording and len(self.recorded_landmarks) < 90:
            lm_dict = [{"x": lm.x, "y": lm.y, "z": lm.z} for lm in landmarks]
            self.recorded_landmarks.append(lm_dict)

    def stop_recording(self):
        if not self.recording:
            return
        self.recording = False
        if len(self.recorded_landmarks) < 10:
            return

        new_count = len(self.recorded_landmarks)
        avg_landmarks = []
        for i in range(21):
            x = sum(lm[i]["x"] for lm in self.recorded_landmarks) / new_count
            y = sum(lm[i]["y"] for lm in self.recorded_landmarks) / new_count
            z = sum(lm[i]["z"] for lm in self.recorded_landmarks) / new_count
            avg_landmarks.append({"x": x, "y": y, "z": z})

        gesture = self.current_gesture
        if gesture in self.templates:
            old = self.templates[gesture]
            old_count = old.get("sample_count", 1)
            old_landmarks = old["landmarks"]
            total = old_count + new_count
            merged = []
            for i in range(21):
                mx = (old_landmarks[i]["x"] * old_count + avg_landmarks[i]["x"] * new_count) / total
                my = (old_landmarks[i]["y"] * old_count + avg_landmarks[i]["y"] * new_count) / total
                mz = (old_landmarks[i]["z"] * old_count + avg_landmarks[i]["z"] * new_count) / total
                merged.append({"x": mx, "y": my, "z": mz})
            self.templates[gesture] = {
                "landmarks": merged,
                "recorded_at": time.time(),
                "sample_count": total
            }
        else:
            self.templates[gesture] = {
                "landmarks": avg_landmarks,
                "recorded_at": time.time(),
                "sample_count": new_count
            }

    def next_step(self):
        self.current_step += 1
        if self.current_step >= len(self.calibration_steps):
            return None
        return self.calibration_steps[self.current_step]

    def save(self):
        path = Path(self.calibration_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.templates, f, indent=2)

    def load(self):
        path = Path(self.calibration_file)
        if path.exists():
            with open(path) as f:
                self.templates = json.load(f)
            return True
        return False

    def match_gesture(self, landmarks):
        if not self.templates:
            return None
        lm_dict = [{"x": lm["x"], "y": lm["y"], "z": lm["z"]} if isinstance(lm, dict)
                   else {"x": lm.x, "y": lm.y, "z": lm.z} for lm in landmarks]
        best_gesture = None
        best_score = 0
        for gesture_name, template in self.templates.items():
            score = self._calculate_similarity(lm_dict, template["landmarks"])
            if score > best_score:
                best_score = score
                best_gesture = gesture_name
        return best_gesture if best_score > 0.7 else None

    def _calculate_similarity(self, current, template):
        total_distance = 0
        for i in range(21):
            dx = current[i]["x"] - template[i]["x"]
            dy = current[i]["y"] - template[i]["y"]
            dz = current[i]["z"] - template[i]["z"]
            total_distance += (dx * dx + dy * dy + dz * dz) ** 0.5
        avg_distance = total_distance / 21
        return max(0.0, 1.0 - avg_distance * 8)
