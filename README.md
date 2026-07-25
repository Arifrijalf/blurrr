# FotoKitaBlur

Real-time hand gesture detection application using MediaPipe. Available as a web application with photobooth and calibration features!

## Features

- **V Sign (Peace)** - Blur effect + typewriter text "blurr" + Love hearts animation
- **Thumbs Up** - Colored edge detection + "Mantap!" text
- **Fist** - Red overlay + "Hidup Jokowi!!!" text + music
- **Photobooth** - Countdown timer + frame capture + download + multi-frame switching
- **Gesture Toggles** - Enable/disable each gesture independently via UI switches
- **Calibration** - Custom gesture calibration for better accuracy (mirror-invariant)

## Running the Web Version

```bash
cd web
npx serve -l 3000
```

Then open `http://localhost:3000` in your browser.

## Web Controls

| Key / Button | Action |
|--------------|--------|
| Click "Start Photobooth" | 3s countdown then capture photo |
| `[` / `]` or ◀ Frame / Frame ▶ buttons | Switch photo frame overlay |
| Click "Download Photo" | Save photo with current frame |
| Gesture toggles (Peace/Mantab/Jokowi) | Enable/disable each gesture |
| Make FIST gesture | Reset photobooth after capture |
| Click "Kalibrasi" | Gesture calibration (mirror-invariant, works for both hands) |
| `Q` / `ESC` | Stop camera & exit |

## Requirements

- Browser: Chrome or Edge (recommended for best performance)
- Webcam access

## Installation (Python Desktop Version)

1. Clone this repository:
```bash
git clone https://github.com/Arifrijalf/blurrr.git
cd blurrr
```

2. Create virtual environment:
```bash
py -3.11 -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download hand landmark model (auto-downloaded on first run, or manually):
```bash
python -c "import urllib.request; urllib.request.urlretrieve('https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task', 'hand_landmarker.task')"
```

## Usage (Desktop Version)

```bash
python hand_gesture_app.py
```

### Controls

| Gesture | Label | Effect |
|---------|-------|--------|
| V Sign | peace | Blur + Love animation + Music |
| Thumbs Up | mantabbb | Edge detection + Text |
| Fist | jokowii | Red overlay + Music |
| `C` | - | Start calibration |
| `Q` / ESC | - | Exit application |

## Technical Notes

- **Service Worker**: Network-first with dynamic cache — always fetches latest files, falls back to cache when offline
- **Frame overlays**: Render with aspect-ratio-preserved scaling (`cover` mode)
- **Calibration**: Uses mirror-invariant similarity matching (X-mirror comparison) so left-hand calibration also works for right hand
- **Gestures**: All three gestures can be independently toggled on/off from the web UI

## License

This project is open source and available for personal use.
