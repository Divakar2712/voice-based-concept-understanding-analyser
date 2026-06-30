import librosa
import numpy as np
import tempfile
import os


def extract_audio_features(uploaded_file):
    """
    Extract basic audio features.
    """

    suffix = os.path.splitext(uploaded_file.name)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        temp_path = tmp.name

    try:

        y, sr = librosa.load(temp_path, sr=None)

        # Duration
        duration = librosa.get_duration(y=y, sr=sr)

        # RMS Energy
        rms = librosa.feature.rms(y=y)
        rms_energy = float(np.mean(rms))

        # Zero Crossing Rate
        zcr = librosa.feature.zero_crossing_rate(y)
        zcr_value = float(np.mean(zcr))

        # Pause Ratio
        silence_threshold = 0.02

        pauses = np.sum(np.abs(y) < silence_threshold)

        pause_ratio = pauses / len(y)

        # Estimated Speech Rate
        speech_rate = round(len(y) / sr / duration, 2)

        return {
            "Duration": round(duration, 2),
            "RMS Energy": round(rms_energy, 4),
            "Zero Crossing Rate": round(zcr_value, 4),
            "Pause Ratio": round(pause_ratio, 4),
            "Speech Rate": speech_rate
        }

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)