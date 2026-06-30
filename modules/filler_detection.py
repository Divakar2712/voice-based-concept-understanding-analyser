import re


# Common filler words and phrases
FILLER_WORDS = [
    "uh",
    "um",
    "er",
    "ah",
    "like",
    "you know",
    "actually",
    "basically",
    "literally",
    "okay",
    "so",
    "well",
    "right",
    "hmm"
]


def detect_fillers(transcript):
    """
    Detect filler words in the transcript.

    Returns:
        {
            "counts": {...},
            "total_fillers": int,
            "total_words": int,
            "filler_density": float
        }
    """

    transcript = transcript.lower()

    counts = {}

    total_fillers = 0

    for filler in FILLER_WORDS:

        pattern = r"\b" + re.escape(filler) + r"\b"

        matches = re.findall(pattern, transcript)

        count = len(matches)

        if count > 0:
            counts[filler] = count
            total_fillers += count

    total_words = len(transcript.split())

    if total_words == 0:
        density = 0.0
    else:
        density = round((total_fillers / total_words) * 100, 2)

    return {
        "counts": counts,
        "total_fillers": total_fillers,
        "total_words": total_words,
        "filler_density": density
    }