from dataclasses import dataclass


@dataclass
class AnalysisResult:

    timestamp: str

    transcript: str

    reference_text: str

    similarity: float

    duration: float

    rms_energy: float

    zero_crossing_rate: float

    pause_ratio: float

    speech_rate: float

    filler_count: int

    filler_density: float

    final_score: float

    grade: str

    gemini_feedback: str