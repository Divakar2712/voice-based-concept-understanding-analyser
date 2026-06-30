import streamlit as st

from modules.speech_to_text import speech_to_text
from modules.audio_features import extract_audio_features
from modules.semantic_similarity import calculate_similarity
from modules.filler_detection import detect_fillers
from modules.scoring import calculate_final_score
from modules.gemini_feedback import generate_feedback
from datetime import datetime
from database.database import save_result, fetch_recent_results

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Voice-Based Concept Understanding Analyser",
    page_icon="🎤",
    layout="wide"
)
# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.image(
        "https://streamlit.io/images/brand/streamlit-mark-color.png",
        width=90
    )

    st.title("🎤 Project Info")

    st.markdown("---")

    st.write("### 👨‍💻 Developer")
    st.write("**Nataraj Divakar**")

    st.write("### 🎓 College")
    st.write("AITS, Tirupati")

    st.write("### 💼 Internship")
    st.write("SmartBridge AI Internship")

    st.write("### 🚀 Version")
    st.write("Version 1.0")

    st.markdown("---")

    st.write("### 🛠 Technologies")

    st.success("✔ Faster Whisper")
    st.success("✔ Sentence Transformers")
    st.success("✔ Google Gemini")
    st.success("✔ Librosa")
    st.success("✔ SQLite")
    st.success("✔ Streamlit")

    st.markdown("---")

    st.info(
        "This project evaluates a student's conceptual understanding using Artificial Intelligence."
    )
# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown("""
<style>

.main-title{
    text-align:center;
    font-size:40px;
    font-weight:bold;
    color:#0E76A8;
}

.subtitle{
    text-align:center;
    color:gray;
    margin-bottom:25px;
}

.metric-card{
    background-color:#F7F7F7;
    padding:15px;
    border-radius:12px;
    border:1px solid #E6E6E6;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown("""
<h1 style='text-align:center;color:#0E76A8;'>
🎤 Voice-Based Concept Understanding Analyser
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<h4 style='text-align:center;color:gray;'>
Speech Recognition • Audio Analysis • Semantic Similarity • Gemini AI
</h4>
""", unsafe_allow_html=True)

st.divider()

# --------------------------------------------------
# Input Layout
# --------------------------------------------------

left_col, right_col = st.columns([2, 1])

with left_col:

    st.subheader("🎙 Upload Student Audio")

    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=["wav", "mp3", "m4a"]
    )

    if uploaded_file is not None:
        st.audio(uploaded_file)

with right_col:

    st.subheader("📚 Reference Concept")

    reference_text = st.text_area(
        "Expected Answer",
        height=220,
        placeholder="Enter the expected concept or model answer..."
    )

st.divider()

# --------------------------------------------------
# Analyze Button
# --------------------------------------------------

analyze = st.button(
    "🚀 Analyze Concept Understanding",
    use_container_width=True
)

if analyze:

    if uploaded_file is None:
        st.warning("⚠ Please upload an audio file.")

    elif reference_text.strip() == "":
        st.warning("⚠ Please enter the reference concept.")

    else:

        # ------------------------------------------
        # Speech To Text
        # ------------------------------------------

        with st.spinner("🎙 Transcribing Audio..."):

            transcript = speech_to_text(uploaded_file)

        st.success("✅ Speech successfully transcribed.")

        st.subheader("📝 Student Transcript")

        st.write(transcript)

        st.divider()

        # ------------------------------------------
        # Audio Feature Extraction
        # ------------------------------------------

        with st.spinner("🎧 Extracting Audio Features..."):

            features = extract_audio_features(uploaded_file)

        st.subheader("🎧 Audio Features")

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "⏱ Duration",
                f"{features['Duration']} sec"
            )

            st.metric(
                "🔊 RMS Energy",
                features["RMS Energy"]
            )

            st.metric(
                "🎵 Zero Crossing Rate",
                features["Zero Crossing Rate"]
            )

        with c2:

            st.metric(
                "🔇 Pause Ratio",
                features["Pause Ratio"]
            )

            st.metric(
                "🗣 Speech Rate",
                features["Speech Rate"]
            )

        st.divider()

        # ------------------------------------------
        # Semantic Similarity
        # ------------------------------------------

        with st.spinner("🧠 Calculating Semantic Similarity..."):

            similarity = float(
                calculate_similarity(
                    reference_text,
                    transcript
                )
            )

        st.subheader("🧠 Semantic Similarity")

        st.metric(
            "Similarity Score",
            f"{similarity:.2f}%"
        )

        progress_value = max(0.0, min(1.0, float(similarity) / 100))
        st.progress(progress_value)

        if similarity >= 80:
            st.success("🟢 Excellent Concept Understanding")

        elif similarity >= 60:
            st.info("🟡 Good Concept Understanding")

        elif similarity >= 40:
            st.warning("🟠 Moderate Concept Understanding")

        else:
            st.error("🔴 Poor Concept Understanding")

        st.divider()
        # ------------------------------------------
        # Filler Word Detection
        # ------------------------------------------

        with st.spinner("💬 Detecting Filler Words..."):

            filler_result = detect_fillers(transcript)

        st.subheader("💬 Filler Word Analysis")

        if filler_result["counts"]:

            st.write("### Detected Filler Words")

            for word, count in filler_result["counts"].items():

                st.write(f"• **{word}** : {count}")

        else:

            st.success("🎉 No filler words detected!")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Fillers",
                filler_result["total_fillers"]
            )

        with col2:
            st.metric(
                "Total Words",
                filler_result["total_words"]
            )

        with col3:
            st.metric(
                "Filler Density",
                f"{filler_result['filler_density']}%"
            )

        if filler_result["filler_density"] < 3:
            st.success("⭐⭐⭐ Excellent Fluency")

        elif filler_result["filler_density"] < 7:
            st.info("⭐⭐ Good Fluency")

        elif filler_result["filler_density"] < 12:
            st.warning("⭐ Average Fluency")

        else:
            st.error("⚠ Needs Improvement (Too many filler words)")

        st.divider()

        # ------------------------------------------
        # Final Score Calculation
        # ------------------------------------------

        with st.spinner("📊 Calculating Final Score..."):

            score = calculate_final_score(
                similarity,
                features,
                filler_result
            )

        st.subheader("📊 Final Performance Score")

        score_col1, score_col2 = st.columns(2)

        with score_col1:

            st.metric(
                "🏆 Final Score",
                f"{score['Final Score']:.2f}/100"
            )

            st.progress(float(score["Final Score"]) / 100)

        with score_col2:

            st.metric(
                "🎓 Grade",
                score["Grade"]
            )

        st.write("### Score Breakdown")

        b1, b2, b3 = st.columns(3)

        with b1:
            st.metric(
                "Semantic Score",
                f"{score['Semantic Score']} / 60"
            )

        with b2:
            st.metric(
                "Fluency Score",
                f"{score['Fluency Score']} / 20"
            )

        with b3:
            st.metric(
                "Audio Score",
                f"{score['Audio Score']} / 20"
            )

        if score["Final Score"] >= 85:

            st.success("🌟 Excellent Overall Performance")

        elif score["Final Score"] >= 70:

            st.info("👍 Good Overall Performance")

        elif score["Final Score"] >= 50:

            st.warning("🙂 Moderate Overall Performance")

        else:

            st.error("📘 Needs More Practice")

        st.divider()
                # ------------------------------------------
        # Gemini AI Feedback
        # ------------------------------------------

        st.subheader("🤖 Gemini AI Feedback")
        st.info("Gemini temporarily disabled for testing.")
        data = {

            "transcript": transcript,

            "reference_text": reference_text,

            "similarity": similarity,

            "duration": features["Duration"],

            "rms_energy": features["RMS Energy"],

            "zero_crossing_rate": features["Zero Crossing Rate"],

            "pause_ratio": features["Pause Ratio"],

            "speech_rate": features["Speech Rate"],

            "filler_count": filler_result["total_fillers"],

            "filler_density": filler_result["filler_density"],

            "final_score": score["Final Score"],

            "grade": score["Grade"],

            "gemini_feedback": "Gemini Disabled"

        }

        save_result(data)

        st.divider()

        # ------------------------------------------
        # Performance Summary
        # ------------------------------------------

        st.subheader("📋 Performance Summary")

        summary_col1, summary_col2 = st.columns(2)

        with summary_col1:

            st.info(f"""
### 📖 Transcript

{transcript}
""")

        with summary_col2:

            st.success(f"""
### 📊 Overall Results

- **Similarity:** {similarity:.2f}%
- **Final Score:** {score['Final Score']}/100
- **Grade:** {score['Grade']}
- **Fillers:** {filler_result['total_fillers']}
- **Filler Density:** {filler_result['filler_density']}%
""")

        st.divider()

        # ------------------------------------------
        # Detailed Audio Statistics
        # ------------------------------------------

        st.subheader("🎧 Detailed Audio Statistics")

        audio_df = {
            "Feature": [
                "Duration",
                "Speech Rate",
                "Pause Ratio",
                "RMS Energy",
                "Zero Crossing Rate"
            ],
            "Value": [
                features["Duration"],
                features["Speech Rate"],
                features["Pause Ratio"],
                features["RMS Energy"],
                features["Zero Crossing Rate"]
            ]
        }

        st.table(audio_df)

        st.divider()
                # ------------------------------------------
        # Analysis Completed
        # ------------------------------------------

        st.success("✅ Analysis Completed Successfully!")

        st.balloons()

        st.divider()

        # ------------------------------------------
        # Recommendations
        # ------------------------------------------

        st.subheader("📌 Recommendations")

        if score["Final Score"] >= 85:

            st.success("""
✅ Excellent understanding of the concept.

Keep maintaining your fluency and confidence.
You are presentation-ready.
""")

        elif score["Final Score"] >= 70:

            st.info("""
👍 Good understanding.

Improve concept explanation with a little more detail.
Reduce filler words for an even better presentation.
""")

        elif score["Final Score"] >= 50:

            st.warning("""
⚠ Moderate understanding.

Revise the topic once again.
Speak more confidently and reduce pauses.
Practice explaining concepts in your own words.
""")

        else:

            st.error("""
❌ Significant improvement needed.

Study the concept again.
Practice speaking clearly.
Avoid excessive pauses and filler words.
Focus on explaining the key ideas.
""")

        st.divider()

        # ------------------------------------------
        # Project Information
        # ------------------------------------------

        with st.expander("ℹ About this Project"):

            st.markdown("""
### 🎤 Voice-Based Concept Understanding Analyser

This application evaluates a student's conceptual understanding using Artificial Intelligence.

### Features

- 🎙 Speech-to-Text (Faster Whisper)
- 🧠 Semantic Similarity (Sentence-BERT)
- 🎧 Audio Feature Extraction
- 💬 Filler Word Detection
- 📊 Intelligent Scoring Engine
- 🤖 Gemini AI Feedback

Developed using:

- Python
- Streamlit
- Faster Whisper
- Sentence Transformers
- Google Gemini
- Librosa
""")

        st.divider()

        st.caption(
            "SmartBridge Internship Project • Voice-Based Concept Understanding Analyser"
        )
        st.divider()

st.subheader("📚 Previous Analyses")

history = fetch_recent_results()

if history:

    history_data = []

    for row in history:

        history_data.append({

            "Date": row[0],

            "Similarity (%)": round(row[1], 2),

            "Final Score": round(row[2], 2),

            "Grade": row[3]

        })

    st.dataframe(

        history_data,

        use_container_width=True,

        hide_index=True

    )

else:

    st.info("No previous analyses found.")
