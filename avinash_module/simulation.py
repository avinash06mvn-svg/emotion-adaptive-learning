"""Deterministic simulator for testing the adaptive engine without a webcam."""

from __future__ import annotations

import argparse
import time
from datetime import datetime, timedelta, timezone
from typing import Callable, Iterable, Optional

from .learning_state import EmotionObservation, LearnerStatePayload, TemporalEmotionSmoother, build_payload
from .webcam import send_to_raghaves_engine


def emotion_timeline() -> Iterable[tuple[str, float]]:
    """Normal -> struggling -> frustrated -> engaged, with five samples per phase."""
    for emotion, confidence in (
        ("neutral", 0.86),
        ("confused", 0.91),
        ("angry", 0.88),
        ("happy", 0.94),
    ):
        yield from ((emotion, confidence) for _ in range(5))


def simulate(
    student_id: str = "STU001",
    on_payload: Optional[Callable[[LearnerStatePayload], None]] = None,
    interval_seconds: float = 0.0,
) -> list[LearnerStatePayload]:
    smoother = TemporalEmotionSmoother(window_size=5, confidence_threshold=0.70)
    start = datetime.now(timezone.utc).replace(microsecond=0)
    emitted: list[LearnerStatePayload] = []
    for index, (emotion, confidence) in enumerate(emotion_timeline()):
        observation = EmotionObservation(
            emotion=emotion,
            confidence=confidence,
            timestamp=start + timedelta(seconds=index),
        )
        payload = build_payload(student_id, observation, smoother)
        if payload is not None:
            emitted.append(payload)
            if on_payload:
                on_payload(payload)
        if interval_seconds:
            time.sleep(interval_seconds)
    return emitted


def mock_raghaves_engine(payload: dict) -> dict:
    """Drop-in stand-in showing exactly what Raghave's engine receives."""
    return {"received": payload, "accepted": True}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the emotion-to-learning-state simulation")
    parser.add_argument("--student-id", default="STU001")
    parser.add_argument("--interval", type=float, default=0.0)
    args = parser.parse_args()
    payloads = simulate(args.student_id, interval_seconds=args.interval)
    for payload in payloads:
        result = send_to_raghaves_engine(payload, mock_raghaves_engine)
        print(payload.to_engine_json())
        print(f"engine_result={result}")


if __name__ == "__main__":
    main()
