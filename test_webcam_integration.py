"""Live webcam -> Avinash module -> Raghave engine demonstration."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
ENGINE_DIR = ROOT / "adaptive_learning"
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from adaptive_engine import AdaptiveEngine  # noqa: E402
from avinash_module.webcam import stream_from_webcam  # noqa: E402


ENGAGEMENT_BY_STATE = {
    "engaged": 85,
    "normal": 65,
    "struggling": 45,
    "frustrated": 30,
    "anxious": 35,
    "bored": 25,
}

engine = AdaptiveEngine()


def emotion_to_engagement(learning_state: str) -> int:
    return ENGAGEMENT_BY_STATE.get(learning_state.lower(), 60)


def process_emotion(payload) -> None:
    data = payload.to_engine_dict()
    result = engine.process_student(
        emotion=data["emotion"],
        # Replace these demo values with the student's real session metrics.
        previous_score=68,
        study_time=2.5,
        quiz_accuracy=70,
        engagement=emotion_to_engagement(data["learning_state"]),
        consistency=65,
    )

    print("\n========================================")
    print("REAL WEBCAM -> ADAPTIVE ENGINE")
    print("========================================")
    print("Student ID:", data["student_id"])
    print("Emotion:", data["emotion"])
    print("Confidence:", round(data["emotion_confidence"], 2))
    print("Learning State:", data["learning_state"])
    print("Predicted Performance:", result["predicted_performance"], "%")
    print("Difficulty:", result["difficulty"])
    print("Content:", result["content"])
    print("Activity:", result["activity"])
    print("Reason:", result["reason"])


if __name__ == "__main__":
    print("Starting REAL webcam integration...")
    print("Look at the camera. Press Q or Esc in the camera window to stop.")
    stream_from_webcam(
        student_id="STUDENT001",
        on_payload=process_emotion,
        camera_index=0,
        window_size=5,
        confidence_threshold=0.70,
    )
