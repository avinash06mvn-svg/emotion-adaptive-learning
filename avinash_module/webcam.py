"""Real-time OpenCV capture loop feeding validated learner-state payloads."""

from __future__ import annotations

from typing import Callable, Optional

from .emotion_detector import EmotionDetector
from .learning_state import LearnerStatePayload, TemporalEmotionSmoother, build_payload


def stream_from_webcam(
    student_id: str,
    on_payload: Callable[[LearnerStatePayload], None],
    camera_index: int = 0,
    window_size: int = 5,
    confidence_threshold: float = 0.70,
    detector: Optional[EmotionDetector] = None,
) -> None:
    """Capture until q/Esc is pressed, invoking on_payload for stable states."""
    try:
        import cv2
    except ImportError as exc:
        raise RuntimeError("Install opencv-python to use webcam capture.") from exc

    capture = cv2.VideoCapture(camera_index)
    if not capture.isOpened():
        raise RuntimeError(f"Could not open webcam index {camera_index}")

    detector = detector or EmotionDetector()
    smoother = TemporalEmotionSmoother(window_size, confidence_threshold)
    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            observation = detector.detect(frame)
            if observation is not None:
                payload = build_payload(student_id, observation, smoother)
                if payload is not None:
                    on_payload(payload)
            cv2.imshow("Emotion Detection (press q to quit)", frame)
            if cv2.waitKey(1) & 0xFF in (ord("q"), 27):
                break
    finally:
        capture.release()
        cv2.destroyAllWindows()


def send_to_raghaves_engine(payload: LearnerStatePayload, engine_handler: Callable[[dict], object]) -> object:
    """Example integration: pass the exact JSON-compatible dictionary to the engine."""
    return engine_handler(payload.to_engine_dict())
