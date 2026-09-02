"""One-shot Avinash -> Raghave integration check."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
ENGINE_DIR = ROOT / "adaptive_learning"
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from adaptive_engine import AdaptiveEngine  # noqa: E402
from avinash_module.learning_state import LearnerStatePayload  # noqa: E402
from learning_content import get_learning_content  # noqa: E402


def run_integration_test() -> None:
    emotion_payload = LearnerStatePayload(
        student_id="STUDENT001",
        emotion="happy",
        emotion_confidence=0.92,
        learning_state="engaged",
        timestamp="2026-08-18T10:00:00Z",
    )
    payload = emotion_payload.to_engine_dict()

    print("\n===== AVINASH -> RAGHAVE INTEGRATION =====")
    print("Payload received:", payload)

    engine = AdaptiveEngine()
    result = engine.process_student(
        emotion=payload["emotion"],
        previous_score=68,
        study_time=2.5,
        quiz_accuracy=70,
        engagement=60,
        consistency=65,
    )

    content = get_learning_content("Java Loops", result["difficulty"], result["activity"])
    print("\n===== ADAPTIVE ENGINE RESULT =====")
    print("Emotion:", result["emotion"])
    print("Predicted Performance:", result["predicted_performance"], "%")
    print("Difficulty:", result["difficulty"])
    print("Content:", content["title"])
    print("Activity:", result["activity"])
    print("Reason:", result["reason"])
    print("Learning Path:")
    for i, step in enumerate(result["learning_path"], 1):
        print(f"{i}. {step}")


if __name__ == "__main__":
    run_integration_test()
