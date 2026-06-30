from faster_whisper import WhisperModel
import tempfile
import os
import streamlit as st

# Load model only once
@st.cache_resource
def load_model():
    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8"
    )
    return model


def speech_to_text(uploaded_file):

    model = load_model()

    suffix = os.path.splitext(uploaded_file.name)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        temp_path = tmp.name

    segments, info = model.transcribe(
        temp_path,
        beam_size=5
    )

    transcript = " ".join([segment.text for segment in segments])

    os.remove(temp_path)

    return transcript