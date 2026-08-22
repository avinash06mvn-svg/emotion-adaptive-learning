from datetime import datetime, timezone

from avinash_module.learning_state import (
    EmotionObservation,
    LearningState,
    TemporalEmotionSmoother,
    build_payload,
)
from avinash_module.simulation import simulate
from avinash_module.webcam import send_to_raghaves_engine


def test_low_confidence_is_ignored():
    smoother = TemporalEmotionSmoother(window_size=5)
    result = build_payload(
        "STU001",
        EmotionObservation(emotion="angry", confidence=0.69),
        smoother,
    )
    assert result is None


def test_majority_vote_smooths_transient_jump():
    smoother = TemporalEmotionSmoother(window_size=5)
    timestamp = datetime.now(timezone.utc)
    for emotion in ("neutral", "neutral", "happy", "neutral", "neutral"):
        payload = build_payload("STU001", EmotionObservation(emotion=emotion, confidence=.9, timestamp=timestamp), smoother)
    assert payload is not None
    assert payload.emotion == "neutral"
    assert payload.learning_state == LearningState.NORMAL


def test_payload_matches_engine_contract():
    payloads = simulate()
    assert payloads[-1].to_engine_dict()["learning_state"] == "engaged"
    assert set(payloads[-1].to_engine_dict()) == {
        "student_id", "emotion", "emotion_confidence", "learning_state", "timestamp"
    }


def test_adapter_passes_dictionary_unchanged():
    payload = simulate()[0]
    received = []
    send_to_raghaves_engine(payload, received.append)
    assert received[0] == payload.to_engine_dict()
