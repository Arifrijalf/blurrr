# FotoKitaBlur

Real-time hand gesture detection application using OpenCV and MediaPipe. Detect hand gestures through your webcam and apply cool visual effects with music.

## Features

- **V Sign (Peace)** - Gaussian blur effect + typewriter text "Foto kita blur" + background music
- **Thumbs Up** - Colored edge detection effect + animated "Mantap!" text
- **Fist** - Red overlay + animated "Hidup Jokowi!!!" text + music

## Requirements

- Python 3.11 (recommended)
- Webcam
- Windows OS (tested on Windows 10/11)

## Installation

1. Clone this repository:

```bash
git clone https://github.com/Arifrijalf/blurrr.git
cd blurrr
```

2. Create virtual environment (recommended):

```bash
py -3.11 -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Download hand landmark model:

```bash
python -c "import urllib.request; urllib.request.urlretrieve('https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task', 'hand_landmarker.task')"
```

> **Note**: File `hand_landmarker.task` harus ada di root folder agar aplikasi dapat berjalan.

## Usage

```bash
python hand_gesture_app.py
```

### Controls

| Gesture        | Effect                                  |
| -------------- | --------------------------------------- |
| V Sign (Peace) | Blur + "Foto kita blur" text + music    |
| Thumbs Up      | Edge detection + "Mantap!" text         |
| Fist           | Red overlay + "Hidup Jokowi!!!" + music |
| Q / ESC        | Exit application                        |

## Troubleshooting

### Kamera tidak terdeteksi

- Pastikan tidak ada aplikasi lain yang menggunakan webcam (Zoom, Teams, dll).
- Coba cabut dan pasang kembali webcam.
- Aplikasi akan otomatis mencoba mendeteksi kamera pada index 0 atau 1.

### Error `AttributeError: module 'mediapipe' has no attribute 'solutions'`

- Pastikan versi mediapipe yang terinstall >= 0.10.30.
- Jalankan: `pip install --upgrade mediapipe`

### Error `FileNotFoundError: hand_landmarker.task`

- Pastikan file `hand_landmarker.task` ada di root folder project.
- Ikuti langkah instalasi nomor 4 untuk mengunduh model.

## Project Structure

```
FotoKitaBlur/
├── hand_gesture_app.py          # Main application
├── requirements.txt             # Python dependencies
├── hand_landmarker.task         # MediaPipe hand landmark model (auto-downloaded)
├── FOTO KITA BLUR - SAL PRIADI.mp3  # Background music
└── README.md
```

## Dependencies

- `opencv-python` - Computer vision library
- `mediapipe` - Hand landmark detection
- `numpy` - Numerical computing
- `pygame` - Audio playback

## License

This project is open source and available for personal use.
