"""Student state tracking."""

from dataclasses import dataclass, field


@dataclass
class StudentState:
    student_id: str
    emotion: str = "neutral"
    mastery: dict = field(default_factory=dict)
