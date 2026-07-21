# FotoKitaBlur

Real-time hand gesture detection application using OpenCV and MediaPipe. Now available as a web application!

## Features

- **V Sign (Peace)** - Blur effect + typewriter text "Foto kita blur" + Love hearts animation
- **Thumbs Up** - Colored edge detection + "mantabbb" text
- **Fist** - Red overlay + "jokowii" text + music

## Web Version

The web version runs directly in your browser using MediaPipe Web SDK.

### Running the Web Version locally:

1. Install Python (for local server):
2. Navigate to `web/` folder:
```bash
cd web
python -m http.server 8000
```
3. Open `http://localhost:8000` in your browser.

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
