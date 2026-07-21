import { HandLandmarker, FilesetResolver } from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.18/vision_bundle.mjs";

const MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task";
const MUSIC_URL = "FOTO%20KITA%20BLUR%20-%20SAL%20PRIADI.mp3";
const MUSIC_URL_2 = "Hidup%20jokowi%20%20sound%20meme.mp3";

const FADE_DURATION = 0.4;
const DEBOUNCE_FRAMES = 3;
const TYPEWRITER_CHAR_DELAY = 0.12;
const TYPEWRITER_TEXT = "Foto kita blur";

const W = 640;
const H = 480;
const PROCESS_W = 320;
const PROCESS_H = 240;

let handLandmarker = null;
let video = null;
let canvas = null;
let ctx = null;
let offscreen = null;
let offCtx = null;
let audioCtx = null;
let modelReady = false;

let currentMode = "NORMAL";
let stableMode = "NORMAL";
let debounceBuffer = [];
let vsignStartTime = 0;
let thumbsAnimStart = 0;
let fistAnimStart = 0;
let animFrame = 0;

let audioVsignSource = null;
let audioFistSource = null;
let audioVsignBuf = null;
let audioFistBuf = null;

const FINGER_TIPS = [8, 12, 16, 20];
const FINGER_PIPS = [6, 10, 14, 18];

function unmirror(fn) {
    ctx.save();
    ctx.translate(W, 0);
    ctx.scale(-1, 1);
    fn();
    ctx.restore();
}

let blurIntensity = 14;

function initPreview() {
    const previewCanvas = document.getElementById("preview");
    const pCtx = previewCanvas.getContext("2d");

    const grad = pCtx.createLinearGradient(0, 0, 200, 150);
    grad.addColorStop(0, "#667eea");
    grad.addColorStop(1, "#764ba2");
    pCtx.fillStyle = grad;
    pCtx.fillRect(0, 0, 200, 150);
    pCtx.fillStyle = "#fff";
    pCtx.font = "bold 24px sans-serif";
    pCtx.fillText("PREVIEW", 45, 80);
    previewCanvas.style.filter = `blur(${blurIntensity}px)`;

    const slider = document.getElementById("blurRange");
    const val = document.getElementById("blurVal");
    slider.oninput = (e) => {
        blurIntensity = parseInt(e.target.value);
        val.textContent = blurIntensity + "px";
        previewCanvas.style.filter = `blur(${blurIntensity}px)`;
    };
}
initPreview();

export async function startApp() {
    const btn = document.getElementById("startBtn");
    const loading = document.getElementById("loading");

    btn.style.display = "none";
    loading.style.display = "block";
    document.getElementById("preview").style.display = "none";
    loading.textContent = "Requesting camera access...";

    video = document.getElementById("webcam");
    canvas = document.getElementById("output");
    ctx = canvas.getContext("2d", { willReadFrequently: false });
    canvas.width = W;
    canvas.height = H;

    offscreen = document.createElement("canvas");
    offscreen.width = PROCESS_W;
    offscreen.height = PROCESS_H;
    offCtx = offscreen.getContext("2d", { willReadFrequently: false });

    let stream;
    try {
        stream = await navigator.mediaDevices.getUserMedia({
            video: { width: W, height: H, facingMode: "user" }
        });
    } catch (e) {
        loading.textContent = "Camera access denied. Please allow camera and reload.";
        btn.style.display = "block";
        return;
    }

    video.srcObject = stream;
    video.style.display = "none";
    loading.textContent = "Loading hand detection model...";

    audioCtx = new (window.AudioContext || window.webkitAudioContext)();

    const [vision] = await Promise.all([
        FilesetResolver.forVisionTasks(
            "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.18/wasm"
        ),
        loadAudio(MUSIC_URL).then(buf => { audioVsignBuf = buf; }),
        loadAudio(MUSIC_URL_2).then(buf => { audioFistBuf = buf; })
    ]);

    handLandmarker = await HandLandmarker.createFromOptions(vision, {
        baseOptions: { modelAssetPath: MODEL_URL, delegate: "GPU" },
        runningMode: "VIDEO",
        numHands: 1,
        minHandDetectionConfidence: 0.7,
        minHandPresenceConfidence: 0.7,
        minTrackingConfidence: 0.7
    });

    modelReady = true;
    loading.style.display = "none";

    detectLoop();
}

async function loadAudio(url) {
    try {
        const resp = await fetch(url);
        const buf = await resp.arrayBuffer();
        return await audioCtx.decodeAudioData(buf);
    } catch (e) {
        console.warn("Audio load failed:", e);
        return null;
    }
}

function playAudio(buffer, loop) {
    if (!buffer || !audioCtx) return null;
    if (audioCtx.state === "suspended") audioCtx.resume();
    const source = audioCtx.createBufferSource();
    source.buffer = buffer;
    source.loop = loop;
    source.connect(audioCtx.destination);
    source.start();
    return source;
}

function stopAudio(source) {
    if (source) { try { source.stop(); } catch (e) {} }
    return null;
}

function fingerUp(landmarks, tipIdx, pipIdx) {
    return landmarks[tipIdx].y < landmarks[pipIdx].y;
}

function detectGesture(landmarks) {
    const fingersUp = FINGER_TIPS.map((tip, i) => fingerUp(landmarks, tip, FINGER_PIPS[i]));
    const [indexUp, middleUp, ringUp, pinkyUp] = fingersUp;

    if (indexUp && middleUp && !ringUp && !pinkyUp) return "V_SIGN";

    const thumbTip = landmarks[4];
    const indexMcp = landmarks[5];
    const wrist = landmarks[0];
    const handHeight = Math.abs(wrist.y - indexMcp.y);
    if (handHeight > 0.01) {
        const thumbAbove = indexMcp.y - thumbTip.y;
        if (!fingersUp.some(f => f) && thumbAbove > handHeight * 0.3) return "THUMBS_UP";
        if (!fingersUp.some(f => f) && thumbAbove <= handHeight * 0.3) return "FIST";
    }
    return "NORMAL";
}

function debounce(rawMode) {
    debounceBuffer.push(rawMode);
    if (debounceBuffer.length > DEBOUNCE_FRAMES) debounceBuffer.shift();
    if (debounceBuffer.length === DEBOUNCE_FRAMES && debounceBuffer.every(m => m === rawMode)) {
        stableMode = rawMode;
    }
    return stableMode;
}

function handleTransition(newMode) {
    if (newMode === currentMode) return;

    if (currentMode === "V_SIGN") audioVsignSource = stopAudio(audioVsignSource);
    if (currentMode === "FIST") audioFistSource = stopAudio(audioFistSource);

    if (newMode === "V_SIGN") {
        audioVsignSource = playAudio(audioVsignBuf, true);
        vsignStartTime = performance.now();
    }
    if (newMode === "THUMBS_UP") {
        thumbsAnimStart = performance.now();
    }
    if (newMode === "FIST") {
        audioFistSource = playAudio(audioFistBuf, true);
        fistAnimStart = performance.now();
    }
    currentMode = newMode;
}

function detectLoop() {
    if (!video || video.readyState < 2) {
        requestAnimationFrame(detectLoop);
        return;
    }

    if (!modelReady || !handLandmarker) {
        ctx.drawImage(video, 0, 0, W, H);
        ctx.fillStyle = "rgba(0,0,0,0.5)";
        ctx.fillRect(0, 0, W, H);
        ctx.font = "bold 20px 'Segoe UI', sans-serif";
        ctx.fillStyle = "#fff";
        ctx.textAlign = "center";
        ctx.fillText("Loading model...", W / 2, H / 2);
        requestAnimationFrame(detectLoop);
        return;
    }

    const results = handLandmarker.detectForVideo(video, performance.now());
    let detectedMode = "NORMAL";

    if (results.landmarks && results.landmarks.length > 0) {
        const landmarks = results.landmarks[0];
        detectedMode = detectGesture(landmarks);

        if (stableMode === "NORMAL" || currentMode === "NORMAL") {
            drawLandmarks(landmarks);
        }
    }

    const debounced = debounce(detectedMode);
    handleTransition(debounced);
    renderEffect();
    animFrame++;
    requestAnimationFrame(detectLoop);
}

function drawLandmarks(landmarks) {
    const connections = [
        [0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],
        [5,9],[9,10],[10,11],[11,12],[9,13],[13,14],[14,15],[15,16],
        [13,17],[17,18],[18,19],[19,20],[0,17]
    ];

    ctx.strokeStyle = "#ffff00";
    ctx.lineWidth = 2;
    for (const [a, b] of connections) {
        ctx.beginPath();
        ctx.moveTo(landmarks[a].x * W, landmarks[a].y * H);
        ctx.lineTo(landmarks[b].x * W, landmarks[b].y * H);
        ctx.stroke();
    }

    ctx.fillStyle = "#00c8ff";
    for (const lm of landmarks) {
        ctx.beginPath();
        ctx.arc(lm.x * W, lm.y * H, 3, 0, Math.PI * 2);
        ctx.fill();
    }
}

function renderEffect() {
    ctx.drawImage(video, 0, 0, W, H);

    if (currentMode === "V_SIGN") {
        applyVsignEffect();
    } else if (currentMode === "THUMBS_UP") {
        applyThumbsUpEffect();
    } else if (currentMode === "FIST") {
        applyFistEffect();
    }

    drawStatus();
}

function applyVsignEffect() {
    offCtx.save();
    offCtx.filter = `blur(${blurIntensity}px) brightness(0.85)`;
    offCtx.drawImage(video, 0, 0, PROCESS_W, PROCESS_H);
    offCtx.restore();

    ctx.drawImage(offscreen, 0, 0, W, H);

    const elapsed = (performance.now() - vsignStartTime) / 1000;
    drawTypewriter(TYPEWRITER_TEXT, elapsed, W, H);
    drawFloatingHearts(W, H);
}

function drawTypewriter(text, elapsed, w, h) {
    unmirror(() => {
        const totalChars = text.length;
        const charProgress = elapsed / TYPEWRITER_CHAR_DELAY;
        const visibleCount = Math.min(Math.floor(charProgress) + 1, totalChars);
        const solidText = text.slice(0, visibleCount - 1);

        ctx.font = "bold 48px 'Segoe UI', sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";

        const fullWidth = ctx.measureText(text).width;
        const baseX = (w - fullWidth) / 2;
        const baseY = h / 2;

        if (solidText) {
            ctx.strokeStyle = "#000";
            ctx.lineWidth = 7;
            ctx.strokeText(solidText, baseX + ctx.measureText(solidText).width / 2, baseY);
            ctx.fillStyle = "#fff";
            ctx.fillText(solidText, baseX + ctx.measureText(solidText).width / 2, baseY);
        }

        if (visibleCount <= totalChars) {
            const fadeChar = text[visibleCount - 1];
            const prefixW = ctx.measureText(solidText).width;
            const charX = baseX + prefixW;
            const frac = charProgress - Math.floor(charProgress);
            const alpha = Math.min(frac / (0.08 / TYPEWRITER_CHAR_DELAY), 1.0);

            ctx.globalAlpha = alpha;
            ctx.strokeStyle = "#000";
            ctx.lineWidth = 7;
            ctx.strokeText(fadeChar, charX + ctx.measureText(fadeChar).width / 2, baseY);
            ctx.fillStyle = "#fff";
            ctx.fillText(fadeChar, charX + ctx.measureText(fadeChar).width / 2, baseY);
            ctx.globalAlpha = 1.0;
        }
    });
}

function drawFloatingHearts(w, h) {
    const now = performance.now() / 1000;
    unmirror(() => {
        for (let i = 0; i < 6; i++) {
            const phase = (now * 0.7 + i * 1.0) % 6;
            const x = w * 0.15 + (i * w * 0.14);
            const y = h - phase * (h / 6);
            const size = 14 + Math.sin(now * 3 + i) * 3;
            const alpha = Math.max(0, 1 - phase / 6);
            drawHeart(x, y, size, `rgba(255, ${60 + i * 25}, ${80 + i * 18}, ${alpha})`);
        }
    });
}

function drawHeart(x, y, size, color) {
    ctx.save();
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(x, y + size * 0.6);
    ctx.bezierCurveTo(x - size * 1.2, y - size * 0.2, x - size * 0.6, y - size, x, y - size * 0.4);
    ctx.bezierCurveTo(x + size * 0.6, y - size, x + size * 1.2, y - size * 0.2, x, y + size * 0.6);
    ctx.fill();
    ctx.restore();
}

function applyThumbsUpEffect() {
    offCtx.save();
    offCtx.filter = "grayscale(1) contrast(8) brightness(0.4)";
    offCtx.drawImage(video, 0, 0, PROCESS_W, PROCESS_H);
    offCtx.restore();

    ctx.globalCompositeOperation = "screen";
    ctx.drawImage(offscreen, 0, 0, W, H);
    ctx.globalCompositeOperation = "source-over";

    const elapsed = (performance.now() - thumbsAnimStart) / 1000;
    const scale = elapsed < FADE_DURATION
        ? 0.5 + (2.0 - 0.5) * (elapsed / FADE_DURATION)
        : 2.0;

    unmirror(() => {
        ctx.font = `bold ${Math.round(scale * 48)}px 'Segoe UI', sans-serif`;
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.strokeStyle = "#000";
        ctx.lineWidth = 7;
        ctx.strokeText("Mantap!", W / 2, H / 2);
        ctx.fillStyle = "#00ffc8";
        ctx.fillText("Mantap!", W / 2, H / 2);
    });
}

function applyFistEffect() {
    ctx.save();
    ctx.globalCompositeOperation = "multiply";
    ctx.fillStyle = "rgba(255, 80, 80, 1)";
    ctx.fillRect(0, 0, W, H);
    ctx.globalCompositeOperation = "source-over";
    ctx.restore();

    ctx.fillStyle = "rgba(180, 0, 0, 0.15)";
    ctx.fillRect(0, 0, W, H);

    const elapsed = (performance.now() - fistAnimStart) / 1000;
    let scale;
    if (elapsed < 0.15) {
        scale = 0.3 + (2.5 - 0.3) * (elapsed / 0.15);
    } else if (elapsed < 0.3) {
        scale = 2.5 - 0.5 * ((elapsed - 0.15) / 0.15);
    } else {
        scale = 2.0;
    }

    unmirror(() => {
        ctx.font = `bold ${Math.round(scale * 48)}px 'Segoe UI', sans-serif`;
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.strokeStyle = "#fff";
        ctx.lineWidth = 8;
        ctx.strokeText("Hidup Jokowi!!!", W / 2, H / 2);
        ctx.fillStyle = "#ff0000";
        ctx.fillText("Hidup Jokowi!!!", W / 2, H / 2);
    });
}

function drawStatus() {
    const statusMap = {
        "NORMAL": { text: "b aja", color: "#b4b4b4" },
        "V_SIGN": { text: "peace", color: "#00dcff" },
        "THUMBS_UP": { text: "mantabbb", color: "#00ff64" },
        "FIST": { text: "jokowii", color: "#ff0000" }
    };
    const s = statusMap[currentMode];
    unmirror(() => {
        ctx.fillStyle = "rgba(0,0,0,0.6)";
        ctx.fillRect(0, 0, 220, 32);
        ctx.font = "bold 14px 'Segoe UI', sans-serif";
        ctx.textAlign = "left";
        ctx.textBaseline = "middle";
        ctx.fillStyle = s.color;
        ctx.fillText(s.text, 10, 16);
    });
}

window.startApp = startApp;
