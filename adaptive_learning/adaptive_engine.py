"""Core adaptive engine that combines emotion and performance signals."""


class AdaptiveEngine:
    def __init__(self) -> None:
        self.state = {}

    def next_action(self, student_id: str, emotion: str, score: float):
        raise NotImplementedError
