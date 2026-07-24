"""
Hand Gesture Detection App - Main Entry Point

Real-time hand gesture detection using OpenCV and MediaPipe.

Supported gestures:
- V Sign (Peace): Blur + typewriter text "Foto kita blur" + music
- Thumbs Up: Colored edge detection + "Mantab!" text
- Fist: Red overlay + "Hidup Jokowi!!!" + music

This file serves as a backward-compatible entry point that delegates to
modularized components in src/fotokitablur/.
"""

from src.fotokitablur.app import HandGestureApp

# Re-export the main class for backward compatibility
__all__ = ["HandGestureApp"]

if __name__ == "__main__":
    app = HandGestureApp()
    app.run()