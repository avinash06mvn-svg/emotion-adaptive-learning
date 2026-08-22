"""Validated contracts, confidence filtering, smoothing, and state mapping."""

from __future__ import annotations

from collections import Counter, deque
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


CONFIDENCE_THRESHOLD = 0.70


class LearningState(str, Enum):
    ENGAGED = "engaged"
    STRUGGLING = "struggling"
    FRUSTRATED = "frustrated"
    ANXIOUS = "anxious"
    NORMAL = "normal"
    BORED = "bored"


class EmotionObservation(BaseModel):
    """One detector result after normalizing DeepFace's output."""

    model_config = ConfigDict(extra="ignore")

    emotion: str
    confidence: float = Field(ge=0.0, le=1.0)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("emotion")
    @classmethod
    def normalize_emotion(cls, value: str) -> str:
        value = value.strip().lower()
        if not value:
            raise ValueError("emotion must not be empty")
        return value


class LearnerStatePayload(BaseModel):
    """Exact contract consumed by Raghave's adaptive learning engine."""

    model_config = ConfigDict(extra="forbid")

    student_id: str = Field(min_length=1)
    emotion: str
    emotion_confidence: float = Field(ge=0.70, le=1.0)
    learning_state: LearningState
    timestamp: datetime

    @field_validator("emotion")
    @classmethod
    def normalize_emotion(cls, value: str) -> str:
        return value.strip().lower()

    def to_engine_dict(self) -> dict:
        """Return the JSON-compatible dictionary, with enum values serialized."""
        return self.model_dump(mode="json")

    def to_engine_json(self) -> str:
        return self.model_dump_json()


EMOTION_TO_STATE = {
    "happy": LearningState.ENGAGED,
    "surprise": LearningState.ENGAGED,
    "surprised": LearningState.ENGAGED,
    "confused": LearningState.STRUGGLING,
    "sad": LearningState.STRUGGLING,
    "angry": LearningState.FRUSTRATED,
    "disgust": LearningState.FRUSTRATED,
    "fear": LearningState.ANXIOUS,
    "neutral": LearningState.NORMAL,
    "bored": LearningState.BORED,
}


def map_emotion_to_learning_state(emotion: str) -> LearningState:
    return EMOTION_TO_STATE.get(emotion.strip().lower(), LearningState.NORMAL)


class TemporalEmotionSmoother:
    """Majority-vote smoother that ignores low-confidence observations."""

    def __init__(self, window_size: int = 5, confidence_threshold: float = CONFIDENCE_THRESHOLD):
        if window_size < 1:
            raise ValueError("window_size must be at least 1")
        if not 0.0 <= confidence_threshold <= 1.0:
            raise ValueError("confidence_threshold must be between 0 and 1")
        self.window = deque(maxlen=window_size)
        self.confidence_threshold = confidence_threshold

    def add(self, observation: EmotionObservation) -> Optional[EmotionObservation]:
        if observation.confidence < self.confidence_threshold:
            return self.stable_observation
        self.window.append(observation)
        return self.stable_observation

    @property
    def stable_emotion(self) -> Optional[str]:
        if not self.window:
            return None
        counts = Counter(item.emotion for item in self.window)
        # Counter preserves insertion order on ties, making transitions deterministic.
        return counts.most_common(1)[0][0]

    @property
    def stable_observation(self) -> Optional[EmotionObservation]:
        emotion = self.stable_emotion
        if emotion is None:
            return None
        matching = [item for item in reversed(self.window) if item.emotion == emotion]
        return matching[0] if matching else None


def build_payload(
    student_id: str,
    observation: EmotionObservation,
    smoother: TemporalEmotionSmoother,
) -> Optional[LearnerStatePayload]:
    """Add an observation and return the latest stable payload, if available."""
    stable = smoother.add(observation)
    if stable is None:
        return None
    return LearnerStatePayload(
        student_id=student_id,
        emotion=stable.emotion,
        emotion_confidence=stable.confidence,
        learning_state=map_emotion_to_learning_state(stable.emotion),
        timestamp=stable.timestamp,
    )
