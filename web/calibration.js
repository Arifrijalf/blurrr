class CalibrationManager {
    constructor() {
        this.key = "fotokitablur_calibration_v2";
        this.templates = {};
        this.recording = false;
        this.currentGesture = null;
        this.recordedLandmarks = [];
        this.calibrationSteps = ["V_SIGN", "THUMBS_UP", "FIST"];
        this.currentStep = 0;
    }

    startCalibration() {
        this.currentStep = 0;
        this.templates = {};
        return this.calibrationSteps[this.currentStep];
    }

    currentStepName() {
        return this.calibrationSteps[this.currentStep];
    }

    startRecordingStep() {
        this.recording = true;
        this.currentGesture = this.calibrationSteps[this.currentStep];
        this.recordedLandmarks = [];
    }

    recordFrame(landmarks) {
        if (this.recording && this.recordedLandmarks.length < 90) {
            this.recordedLandmarks.push(landmarks.map(l => ({...l})));
        }
    }

    stopRecording() {
        if (!this.recording) return;
        this.recording = false;

        if (this.recordedLandmarks.length < 10) return;

        const avgLandmarks = [];
        for (let i = 0; i < 21; i++) {
            const avg = {
                x: this.recordedLandmarks.reduce((sum, lm) => sum + lm[i].x, 0) / this.recordedLandmarks.length,
                y: this.recordedLandmarks.reduce((sum, lm) => sum + lm[i].y, 0) / this.recordedLandmarks.length,
                z: this.recordedLandmarks.reduce((sum, lm) => sum + lm[i].z, 0) / this.recordedLandmarks.length
            };
            avgLandmarks.push(avg);
        }

        this.templates[this.currentGesture] = {
            landmarks: avgLandmarks,
            recordedAt: Date.now(),
            sampleCount: this.recordedLandmarks.length
        };
    }

    nextStep() {
        this.currentStep++;
        if (this.currentStep >= this.calibrationSteps.length) {
            return null;
        }
        return this.calibrationSteps[this.currentStep];
    }

    save() {
        try {
            localStorage.setItem(this.key, JSON.stringify(this.templates));
            return true;
        } catch (e) {
            return false;
        }
    }

    load() {
        try {
            const data = localStorage.getItem(this.key);
            if (data) {
                this.templates = JSON.parse(data);
                return true;
            }
        } catch (e) {}
        return false;
    }

    matchGesture(landmarks) {
        if (Object.keys(this.templates).length === 0) return null;

        let bestGesture = null;
        let bestScore = 0;

        for (const [gesture, template] of Object.entries(this.templates)) {
            const score = this.calculateSimilarity(landmarks, template.landmarks);
            if (score > bestScore) {
                bestScore = score;
                bestGesture = gesture;
            }
        }

        return bestScore > 0.7 ? bestGesture : null;
    }

    calculateSimilarity(current, template) {
        let totalDistance = 0;
        for (let i = 0; i < 21; i++) {
            const dx = current[i].x - template[i].x;
            const dy = current[i].y - template[i].y;
            const dz = (current[i].z || 0) - (template[i].z || 0);
            totalDistance += Math.sqrt(dx * dx + dy * dy + dz * dz);
        }
        const avgDistance = totalDistance / 21;
        return Math.max(0.0, 1.0 - avgDistance * 8);
    }

    isCalibrated() {
        return Object.keys(this.templates).length === 3;
    }
}

window.CalibrationManager = CalibrationManager;
