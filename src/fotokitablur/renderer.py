
import cv2
import numpy as np
import time
from enum import Enum, auto

from src.fotokitablur.enums import GestureMode
from src.fotokitablur.constants import (
    BLUR_KERNEL_SIZE,
    EDGE_CANNY_LOW,
    EDGE_CANNY_HIGH,
    FADE_DURATION,
    FONT_SCALE_MAIN,
    FONT_SCALE_STATUS
)


class EffectRenderer:
    TYPEWRITER_TEXT = "blurr"
    TYPEWRITER_CHAR_DELAY = 0.12
    TYPEWRITER_FADE_DURATION = 0.08

    def __init__(self):
        self._thumbs_anim_start = 0.0
        self._fist_anim_start = 0.0
        self._vsign_start_time = 0.0

    def reset_vsign_anim(self):
        self._vsign_start_time = time.time()

    def _put_text_centered(self, frame, text, font_scale, color,
                           thickness=3, outline_color=(0, 0, 0), outline_thickness=6):
        font = cv2.FONT_HERSHEY_DUPLEX
        h, w = frame.shape[:2]
        (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
        x = (w - text_w) // 2
        y = (h + text_h) // 2

        cv2.putText(frame, text, (x, y), font, font_scale,
                    outline_color, outline_thickness, cv2.LINE_AA)
        cv2.putText(frame, text, (x, y), font, font_scale,
                    color, thickness, cv2.LINE_AA)

    def _put_text_typewriter(self, frame, full_text, elapsed, font_scale, color,
                             thickness=3, outline_color=(0, 0, 0), outline_thickness=7):
        font = cv2.FONT_HERSHEY_DUPLEX
        h, w = frame.shape[:2]

        (full_tw, text_h), _ = cv2.getTextSize(full_text, font, font_scale, thickness)
        base_x = (w - full_tw) // 2
        base_y = (h + text_h) // 2

        total_chars = len(full_text)
        char_progress = elapsed / self.TYPEWRITER_CHAR_DELAY
        visible_count = min(int(char_progress) + 1, total_chars)

        solid_text = full_text[:max(0, visible_count - 1)]
        if solid_text:
            cv2.putText(frame, solid_text, (base_x, base_y), font, font_scale,
                        outline_color, outline_thickness, cv2.LINE_AA)
            cv2.putText(frame, solid_text, (base_x, base_y), font, font_scale,
                        color, thickness, cv2.LINE_AA)

        if visible_count <= total_chars:
            fade_char = full_text[visible_count - 1]
            prefix = full_text[:visible_count - 1]
            (prefix_w, _), _ = cv2.getTextSize(prefix, font, font_scale, thickness)
            char_x = base_x + prefix_w

            frac = char_progress - int(char_progress)
            alpha = min(frac / (self.TYPEWRITER_FADE_DURATION / self.TYPEWRITER_CHAR_DELAY), 1.0)
            if visible_count > int(char_progress) + 1:
                alpha = 1.0

            fade_color = tuple(
                int(outline_color[i] + (color[i] - outline_color[i]) * alpha) for i in range(3)
            )
            fade_outline = tuple(int(outline_color[i] * alpha) for i in range(3))

            cv2.putText(frame, fade_char, (char_x, base_y), font, font_scale,
                        fade_outline, outline_thickness, cv2.LINE_AA)
            cv2.putText(frame, fade_char, (char_x, base_y), font, font_scale,
                        fade_color, thickness, cv2.LINE_AA)

    def apply_v_sign(self, frame: np.ndarray) -> np.ndarray:
        k = BLUR_KERNEL_SIZE if BLUR_KERNEL_SIZE % 2 == 1 else BLUR_KERNEL_SIZE + 1
        blurred = cv2.GaussianBlur(frame, (k, k), 0)
        elapsed = time.time() - self._vsign_start_time

        self._put_text_typewriter(
            blurred, self.TYPEWRITER_TEXT, elapsed,
            font_scale=FONT_SCALE_MAIN, color=(255, 255, 255),
            thickness=3, outline_color=(0, 0, 0), outline_thickness=7,
        )
        return blurred

    def apply_thumbs_up(self, frame: np.ndarray, first_frame: bool) -> np.ndarray:
        if first_frame:
            self._thumbs_anim_start = time.time()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, EDGE_CANNY_LOW, EDGE_CANNY_HIGH)

        edge_colored = np.zeros_like(frame)
        edge_colored[:, :, 0] = edges
        edge_colored[:, :, 1] = edges // 2
        edge_colored[:, :, 2] = edges

        output = cv2.addWeighted(frame, 0.7, edge_colored, 0.8, 0)

        elapsed = time.time() - self._thumbs_anim_start
        if elapsed < FADE_DURATION:
            scale = 0.5 + (FONT_SCALE_MAIN - 0.5) * (elapsed / FADE_DURATION)
        else:
            scale = FONT_SCALE_MAIN

        self._put_text_centered(
            output, "Mantab!", font_scale=scale,
            color=(0, 255, 200), thickness=3,
            outline_color=(0, 0, 0), outline_thickness=7,
        )
        return output

    def apply_fist(self, frame: np.ndarray, first_frame: bool) -> np.ndarray:
        if first_frame:
            self._fist_anim_start = time.time()

        red_overlay = frame.copy()
        cv2.rectangle(red_overlay, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 180), -1)
        output = cv2.addWeighted(frame, 0.7, red_overlay, 0.3, 0)

        elapsed = time.time() - self._fist_anim_start
        if elapsed < 0.15:
            progress = elapsed / 0.15
            scale = 0.3 + (FONT_SCALE_MAIN + 0.5 - 0.3) * progress
        elif elapsed < 0.3:
            progress = (elapsed - 0.15) / 0.15
            scale = (FONT_SCALE_MAIN + 0.5) - 0.5 * progress
        else:
            scale = FONT_SCALE_MAIN

        self._put_text_centered(
            output, "Hidup Jokowi!!!", font_scale=scale,
            color=(0, 0, 255), thickness=4,
            outline_color=(255, 255, 255), outline_thickness=8,
        )
        return output

    def draw_status(self, frame: np.ndarray, mode: GestureMode):
        status_map = {
            GestureMode.NORMAL:    ("b aja",       (180, 180, 180)),
            GestureMode.V_SIGN:    ("peace",   (0, 220, 255)),
            GestureMode.THUMBS_UP: ("mantab", (0, 255, 100)),
            GestureMode.FIST:      ("jokowii",     (0, 0, 255)),
        }
        label, color = status_map[mode]

        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (340, 36), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        cv2.putText(frame, label, (10, 24),
                    cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE_STATUS,
                    color, 2, cv2.LINE_AA)

    def draw_hint(self, frame: np.ndarray):
        h, w = frame.shape[:2]
        hint = "Q / ESC: Keluar | C: Kalibrasi"
        (tw, _), _ = cv2.getTextSize(hint, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
        cv2.putText(frame, hint, (w - tw - 10, h - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (160, 160, 160), 1, cv2.LINE_AA)

    def draw_calibration_overlay(self, frame: np.ndarray, text: str, progress: int):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        
        cv2.putText(frame, "KALIBRASI", (w//2 - 100, h//2 - 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3, cv2.LINE_AA)
        
        cv2.putText(frame, text, (w//2 - 150, h//2),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA)
        
        bar_width = 300
        bar_height = 30
        bar_x = (w - bar_width) // 2
        bar_y = h//2 + 40
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (50, 50, 50), -1)
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + int(bar_width * progress / 100), bar_y + bar_height), (0, 255, 0), -1)


class HandLandmarkerDrawer:
    HAND_CONNECTIONS = [
        (0, 1), (1, 2), (2, 3), (3, 4),
        (0, 5), (5, 6), (6, 7), (7, 8),
        (5, 9), (9, 10), (10, 11), (11, 12),
        (9, 13), (13, 14), (14, 15), (15, 16),
        (13, 17), (17, 18), (18, 19), (19, 20),
        (0, 17),
    ]

    @staticmethod
    def draw_landmarks(frame, landmarks, w, h):
        lm_points = []
        for lm in landmarks:
            x = int(lm.x * w)
            y = int(lm.y * h)
            lm_points.append((x, y))

        for start, end in HandLandmarkerDrawer.HAND_CONNECTIONS:
            cv2.line(frame, lm_points[start], lm_points[end], (255, 255, 0), 2)

        for x, y in lm_points:
            cv2.circle(frame, (x, y), 3, (0, 200, 255), -1)