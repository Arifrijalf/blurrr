# FotoKitaBlur

Real-time hand gesture detection application using OpenCV and MediaPipe. Detect hand gestures through your webcam and apply cool visual effects with music.

## Features

- **V Sign (Peace)** - Gaussian blur effect + typewriter text "Foto kita blur" + background music
- **Thumbs Up** - Colored edge detection effect + animated "Mantap!" text
- **Fist** - Red overlay + animated "Hidup Jokowi!!!" text + music

## Requirements

- Python 3.11 (recommended)
- Webcam

## Installation

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

## Usage

```bash
python hand_gesture_app.py
```

### Controls

| Gesture | Effect |
|---------|--------|
| V Sign (Peace) | Blur + "Foto kita blur" text + music |
| Thumbs Up | Edge detection + "Mantap!" text |
| Fist | Red overlay + "Hidup Jokowi!!!" + music |
| Q / ESC | Exit application |

## Project Structure

```
FotoKitaBlur/
├── hand_gesture_app.py          # Main application
├── requirements.txt             # Python dependencies
├── hand_landmarker.task         # MediaPipe hand landmark model
├── FOTO KITA BLUR - *.mp3       # Music files
└── README.md
```

## Dependencies

- `opencv-python` - Computer vision library
- `mediapipe` - Hand landmark detection
- `numpy` - Numerical computing
- `pygame` - Audio playback

## License

This project is open source and available for personal use.
