
import cv2
import numpy as np
import mediapipe as mp
import time
import subprocess
from enum import Enum, auto

mp_tasks = mp.tasks
mp_vision = mp_tasks.vision

from src.fotokitablur.enums import GestureMode
from src.fotokitablur.constants import (
    BLUR_KERNEL_SIZE,
    EDGE_CANNY_LOW,
    EDGE_CANNY_HIGH,
    FADE_DURATION,
    MIN_DETECTION_CONFIDENCE,
    MIN_TRACKING_CONFIDENCE,
    FONT_SCALE_MAIN,
    FONT_SCALE_STATUS,
    TYPEWRITER_TEXT,
    TYPEWRITER_CHAR_DELAY,
    TYPEWRITER_FADE_DURATION,
    MUSIC_PATH,
    MUSIC_PATH_2,
    CALIBRATION_DURATION
)

from src.fotokitablur.audio import AudioManager
from src.fotokitablur.detector import GestureDetector
from src.fotokitablur.calibration import CalibrationManager
from src.fotokitablur.renderer import EffectRenderer, HandLandmarkerDrawer


class HandGestureApp:
    SKIP_CAMERAS = ["droidcam"]
    MODEL_PATH = "hand_landmarker.task"

    def __init__(self):
        base_options = mp_tasks.BaseOptions(model_asset_path=self.MODEL_PATH)
        options = mp_vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=mp_vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_hand_presence_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
        )
        self.hand_landmarker = mp_vision.HandLandmarker.create_from_options(options)
        self.drawer = HandLandmarkerDrawer()

        self.gesture_detector = GestureDetector()
        self.calibration_manager = CalibrationManager()
        self.calibration_manager.load()
        self.renderer = EffectRenderer()
        self.audio = AudioManager()
        self.audio.load("vsign", MUSIC_PATH)
        self.audio.load("fist", MUSIC_PATH_2)

        self.current_mode: GestureMode = GestureMode.NORMAL
        self._thumbs_first_frame = False
        self._fist_first_frame = False

        self.calibrating = False
        self.calibration_countdown = 0
        self.calibration_next_gesture = None
        self._show_merge_info = False

    def _handle_mode_transition(self, new_mode: GestureMode):
        if new_mode == self.current_mode:
            return

        leaving = self.current_mode
        entering = new_mode

        if leaving == GestureMode.V_SIGN:
            self.audio.stop("vsign")
        if leaving == GestureMode.FIST:
            self.audio.stop("fist")

        if entering == GestureMode.V_SIGN:
            self.audio.play("vsign")
            self.renderer.reset_vsign_anim()
        if entering == GestureMode.THUMBS_UP:
            self._thumbs_first_frame = True
        if entering == GestureMode.FIST:
            self.audio.play("fist", loop=True)
            self._fist_first_frame = True

        self.current_mode = entering

    @staticmethod
    def _get_camera_names() -> list[str]:
        try:
            cmd = (
                'powershell -Command "Get-PnpDevice -Class Camera -Status OK '
                '| Select-Object -ExpandProperty FriendlyName"'
            )
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5, shell=True)
            return [n.strip() for n in result.stdout.strip().splitlines() if n.strip()]
        except Exception:
            return []

    def _find_camera_index(self) -> int:
        names = self._get_camera_names()
        if names:
            print(f"[INFO] Cameras detected: {names}")
            for idx, name in enumerate(names):
                if not any(skip in name.lower() for skip in self.SKIP_CAMERAS):
                    print(f"[INFO] Using: {name} (index {idx})")
                    return idx
            print("[WARNING] All cameras skipped, falling back to index 0")
        return 0

    def run(self):
        cam_index = self._find_camera_index()

        cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap = cv2.VideoCapture(cam_index)
        if not cap.isOpened():
            cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("[ERROR] Cannot open webcam. Ensure camera is not in use by another app.")
            return

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)

        print("[INFO] App running. Press Q or ESC to exit.")

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[ERROR] Failed to read frame from webcam.")
                break

            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

            frame_count += 1
            timestamp_ms = int(time.time() * 1000)

            results = self.hand_landmarker.detect_for_video(mp_image, timestamp_ms)

            detected_mode = GestureMode.NORMAL

            if results.hand_landmarks:
                hand_landmarks = results.hand_landmarks[0]
                
                if self.calibrating:
                    self.calibration_manager.record_frame(hand_landmarks)
                
                detected_mode = self.gesture_detector.detect(hand_landmarks, self.calibration_manager)

                if detected_mode == GestureMode.NORMAL:
                    self.drawer.draw_landmarks(frame, hand_landmarks, w, h)

            self._handle_mode_transition(detected_mode)

            if self.current_mode == GestureMode.V_SIGN:
                frame = self.renderer.apply_v_sign(frame)
            elif self.current_mode == GestureMode.THUMBS_UP:
                frame = self.renderer.apply_thumbs_up(frame, self._thumbs_first_frame)
                self._thumbs_first_frame = False
            elif self.current_mode == GestureMode.FIST:
                frame = self.renderer.apply_fist(frame, self._fist_first_frame)
                self._fist_first_frame = False

            self.renderer.draw_status(frame, self.current_mode)
            self.renderer.draw_hint(frame)
            
            if self.calibrating:
                self.calibration_countdown -= 1/30
                if self.calibration_countdown <= 0:
                    if not self.calibration_manager.recording:
                        self.calibration_manager.start_recording_step()
                        self.calibration_countdown = CALIBRATION_DURATION
                    else:
                        self.calibration_manager.stop_recording()
                        self.calibration_manager.save()
                        next_gesture = self.calibration_manager.next_step()
                        if next_gesture:
                            self.calibration_next_gesture = next_gesture
                            self.calibration_countdown = CALIBRATION_DURATION
                            print(f"[INFO] Next calibration: {next_gesture}")
                        else:
                            self.calibrating = False
                            print("[INFO] Calibration completed!")
                else:
                    progress = int((CALIBRATION_DURATION - self.calibration_countdown) / CALIBRATION_DURATION * 100)
                    self.renderer.draw_calibration_overlay(frame, f"Pose: {self.calibration_next_gesture}", progress, self._show_merge_info)

            cv2.imshow("Hand Gesture Detection", frame)

            key = cv2.waitKey(1) & 0xFF
            if key in (ord('q'), ord('Q'), 27):
                break
            
            if key == ord('c') and not self.calibrating:
                self.calibrating = True
                self._show_merge_info = self.calibration_manager.has_existing_calibration()
                self.calibration_manager.start_calibration()
                self.calibration_countdown = CALIBRATION_DURATION
                self.calibration_next_gesture = self.calibration_manager.current_step_name()
                print(f"[INFO] Calibration started. Pose: {self.calibration_next_gesture}")

        self.audio.stop_all()
        cap.release()
        cv2.destroyAllWindows()
        self.hand_landmarker.close()
        print("[INFO] App closed.")


if __name__ == "__main__":
    app = HandGestureApp()
    app.run()
