# FotoKitaBlur

Real-time hand gesture detection application using MediaPipe. Available as a web application with photobooth and calibration features!

## Features

- **V Sign (Peace)** - Blur effect + typewriter text "Foto kita blur" + Love hearts animation
- **Thumbs Up** - Colored edge detection + "Mantap!" text
- **Fist** - Red overlay + "Hidup Jokowi!!!" text + music
- **Photobooth** - Countdown timer + frame capture + download
- **Calibration** - Custom gesture calibration for better accuracy

## Running the Web Version

```bash
cd web
npx serve -l 3000
```

Then open `http://localhost:3000` in your browser.

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
| Q / ESC | - | Exit application |

## License

This project is open source and available for personal use.
