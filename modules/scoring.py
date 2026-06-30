"""
=========================================================
Voice-Based Concept Understanding Analyser
Scoring Engine
=========================================================
Calculates the final score based on:

1. Semantic Similarity
2. Filler Word Density
3. Audio Features

Final Score = 100
=========================================================
"""


def calculate_final_score(similarity, audio_features, filler_result):
    """
    Calculate final score (0-100)

    Parameters
    ----------
    similarity : float
        Semantic similarity percentage (0-100)

    audio_features : dict
        Output from extract_audio_features()

    filler_result : dict
        Output from detect_fillers()

    Returns
    -------
    dict
    """

    # -----------------------------------
    # Semantic Similarity (60 Marks)
    # -----------------------------------

    semantic_score = (similarity / 100) * 60

    # -----------------------------------
    # Fluency Score (20 Marks)
    # -----------------------------------

    filler_density = filler_result["filler_density"]

    if filler_density <= 2:
        fluency_score = 20

    elif filler_density <= 5:
        fluency_score = 18

    elif filler_density <= 8:
        fluency_score = 15

    elif filler_density <= 12:
        fluency_score = 10

    else:
        fluency_score = 5

    # -----------------------------------
    # Audio Quality Score (20 Marks)
    # -----------------------------------

    pause_ratio = audio_features["Pause Ratio"]

    if pause_ratio <= 0.10:
        audio_score = 20

    elif pause_ratio <= 0.20:
        audio_score = 18

    elif pause_ratio <= 0.30:
        audio_score = 15

    elif pause_ratio <= 0.40:
        audio_score = 10

    else:
        audio_score = 5

    # -----------------------------------
    # Final Score
    # -----------------------------------

    final_score = round(
        semantic_score +
        fluency_score +
        audio_score,
        2
    )

    # -----------------------------------
    # Grade
    # -----------------------------------

    if final_score >= 85:
        grade = "Excellent"

    elif final_score >= 70:
        grade = "Good"

    elif final_score >= 50:
        grade = "Moderate"

    else:
        grade = "Poor"

    return {

        "Semantic Score": round(semantic_score, 2),

        "Fluency Score": fluency_score,

        "Audio Score": audio_score,

        "Final Score": final_score,

        "Grade": grade
    }