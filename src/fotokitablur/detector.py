from src.fotokitablur.enums import GestureMode
from src.fotokitablur.constants import DEBOUNCE_FRAMES, THUMB_THRESHOLD


class GestureDetector:
    FINGER_TIPS = [8, 12, 16, 20]
    FINGER_PIPS = [6, 10, 14, 18]
    FINGER_DIPS = [7, 11, 15, 19]
    THUMB_TIP = 4
    THUMB_IP = 3
    THUMB_MCP = 2
    WRIST = 0
    INDEX_MCP = 5
    MIDDLE_MCP = 9

    def __init__(self):
        self._debounce_buffer: list[GestureMode] = []
        self._stable_mode: GestureMode = GestureMode.NORMAL

    @staticmethod
    def _is_hand_upright(lm) -> bool:
        wrist = lm[0]
        middle_mcp = lm[9]
        return wrist.y > middle_mcp.y

    def _finger_up(self, lm, tip_idx: int, pip_idx: int) -> bool:
        dip_idx = tip_idx - 1
        upright = self._is_hand_upright(lm)
        if upright:
            return lm[tip_idx].y < lm[dip_idx].y
        else:
            return lm[tip_idx].y > lm[dip_idx].y

    def _finger_down(self, lm, tip_idx: int, pip_idx: int) -> bool:
        upright = self._is_hand_upright(lm)
        if upright:
            return lm[tip_idx].y >= lm[pip_idx].y
        else:
            return lm[tip_idx].y <= lm[pip_idx].y

    def _count_fingers_up(self, lm) -> int:
        return sum(
            self._finger_up(lm, tip, pip)
            for tip, pip in zip(self.FINGER_TIPS, self.FINGER_PIPS)
        )

    def _is_thumbs_up(self, lm, fingers_up: list[bool]) -> bool:
        index_up, middle_up, ring_up, pinky_up = fingers_up
        if index_up or middle_up:
            return False

        upright = self._is_hand_upright(lm)
        thumb_tip = lm[self.THUMB_TIP]
        thumb_ip = lm[self.THUMB_IP]
        index_mcp = lm[self.INDEX_MCP]
        wrist = lm[self.WRIST]

        hand_height = abs(wrist.y - index_mcp.y)
        if hand_height < 0.01:
            return False

        if upright:
            thumb_ext_tip = index_mcp.y - thumb_tip.y
            thumb_ext_ip = index_mcp.y - thumb_ip.y
        else:
            thumb_ext_tip = thumb_tip.y - index_mcp.y
            thumb_ext_ip = thumb_ip.y - index_mcp.y

        avg_thumb_ext = (thumb_ext_tip + thumb_ext_ip) / 2
        return avg_thumb_ext > hand_height * THUMB_THRESHOLD

    def _is_fist(self, lm, fingers_up: list[bool]) -> bool:
        index_up, middle_up, ring_up, pinky_up = fingers_up
        if index_up or middle_up:
            return False

        upright = self._is_hand_upright(lm)
        thumb_tip = lm[self.THUMB_TIP]
        index_mcp = lm[self.INDEX_MCP]
        wrist = lm[self.WRIST]

        hand_height = abs(wrist.y - index_mcp.y)
        if hand_height < 0.01:
            return False

        if upright:
            thumb_above = index_mcp.y - thumb_tip.y
        else:
            thumb_above = thumb_tip.y - index_mcp.y

        return thumb_above <= hand_height * THUMB_THRESHOLD

    def _debounce(self, raw_mode: GestureMode) -> GestureMode:
        self._debounce_buffer.append(raw_mode)
        if len(self._debounce_buffer) > DEBOUNCE_FRAMES:
            self._debounce_buffer.pop(0)

        if (len(self._debounce_buffer) == DEBOUNCE_FRAMES
                and all(m == raw_mode for m in self._debounce_buffer)):
            self._stable_mode = raw_mode

        return self._stable_mode

    def detect(self, landmarks) -> GestureMode:
        lm = landmarks
        fingers_up = [
            self._finger_up(lm, tip, pip)
            for tip, pip in zip(self.FINGER_TIPS, self.FINGER_PIPS)
        ]
        index_up, middle_up, ring_up, pinky_up = fingers_up

        if index_up and middle_up and not (ring_up and pinky_up):
            return self._debounce(GestureMode.V_SIGN)

        if self._is_thumbs_up(lm, fingers_up):
            return self._debounce(GestureMode.THUMBS_UP)

        if self._is_fist(lm, fingers_up):
            return self._debounce(GestureMode.FIST)

        return self._debounce(GestureMode.NORMAL)
