"""Live webcam test wired into the adaptive engine.

Run with:
    python test_webcam.py
Press Q or Esc in the camera window to stop.
"""

from pathlib import Path
import sys

ENGINE_DIR = Path(__file__).resolve().parent / "adaptive_learning"
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from adaptive_engine import AdaptiveEngine
from avinash_module.webcam import stream_from_webcam

ENGAGEMENT_BY_STATE = {
    "engaged": 85,
    "normal": 65,
    "struggling": 45,
    "frustrated": 30,
    "anxious": 35,
    "bored": 25,
}

def emotion_to_engagement(learning_state: str) -> int:
    return ENGAGEMENT_BY_STATE.get(learning_state.lower(), 60)

engine = AdaptiveEngine()

def show_payload(payload) -> None:
    data = payload.to_engine_dict()
    result = engine.process_student(
        emotion=data["emotion"],
        previous_score=60,
        study_time=2,
        quiz_accuracy=62,
        engagement=emotion_to_engagement(data["learning_state"]),
        consistency=55,
    )
    print(
        f"{data['emotion']:>8} -> {data['learning_state']:<11} | "
        f"difficulty={result['difficulty']:<8} | activity={result['activity']}"
    )

if __name__ == "__main__":
    print("Starting webcam. Press Q or Esc in the camera window to stop.")
    stream_from_webcam(
        student_id="STU001",
        on_payload=show_payload,
    )
