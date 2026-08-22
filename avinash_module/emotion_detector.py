"""DeepFace adapter with a lightweight injectable backend for tests."""

from __future__ import annotations

from typing import Any, Callable, Optional

from .learning_state import EmotionObservation


class EmotionDetector:
    def __init__(self, backend: Optional[Callable[[Any], Any]] = None, enforce_detection: bool = False):
        self._backend = backend
        self.enforce_detection = enforce_detection

    def _analyze(self, frame: Any) -> Any:
        if self._backend is not None:
            return self._backend(frame)
        try:
            from deepface import DeepFace
        except ImportError as exc:
            raise RuntimeError("Install deepface to use webcam detection, or inject a backend.") from exc
        return DeepFace.analyze(
            img_path=frame,
            actions=["emotion"],
            enforce_detection=self.enforce_detection,
            detector_backend="opencv",
            silent=True,
        )

    def detect(self, frame: Any) -> Optional[EmotionObservation]:
        try:
            result = self._analyze(frame)
        except Exception:
            # A frame with no detectable face should not stop the stream.
            return None
        result = result[0] if isinstance(result, list) else result
        emotions = result.get("emotion", {})
        if not emotions:
            return None
        emotion, score = max(emotions.items(), key=lambda item: item[1])
        # DeepFace confidence is normally a percentage (0-100).
        confidence = float(score) / 100.0 if float(score) > 1.0 else float(score)
        return EmotionObservation(emotion=emotion, confidence=confidence)
