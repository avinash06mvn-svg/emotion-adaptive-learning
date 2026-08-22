class StudentState:

    def __init__(
        self,
        student_name,
        current_difficulty="Moderate"
    ):
        self.student_name = student_name
        self.current_difficulty = current_difficulty

        self.performance_history = []
        self.emotion_history = []
        self.engagement_history = []

    def update(
        self,
        performance,
        emotion,
        engagement
    ):
        """
        Store the latest learning session.
        """

        self.performance_history.append(performance)
        self.emotion_history.append(emotion)
        self.engagement_history.append(engagement)

        self._adjust_difficulty()

    def _adjust_difficulty(self):

        latest_performance = self.performance_history[-1]
        latest_emotion = self.emotion_history[-1]
        latest_engagement = self.engagement_history[-1]

        # --------------------------------------------------
        # DOWNGRADE DIFFICULTY
        # --------------------------------------------------

        if (
            latest_performance < 50
            or latest_emotion.lower() == "frustrated"
        ):
            self.current_difficulty = "Easy"

        # --------------------------------------------------
        # UPGRADE DIFFICULTY
        # --------------------------------------------------

        elif (
            latest_performance >= 80
            and latest_engagement >= 70
            and latest_emotion.lower() in ["happy", "neutral"]
        ):
            self.current_difficulty = "Advanced"

        # --------------------------------------------------
        # MODERATE
        # --------------------------------------------------

        elif latest_performance >= 60:
            self.current_difficulty = "Moderate"

    def get_state(self):

        return {
            "student": self.student_name,
            "difficulty": self.current_difficulty,
            "latest_performance": (
                self.performance_history[-1]
                if self.performance_history
                else None
            ),
            "latest_emotion": (
                self.emotion_history[-1]
                if self.emotion_history
                else None
            ),
            "latest_engagement": (
                self.engagement_history[-1]
                if self.engagement_history
                else None
            )
        }


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    student = StudentState(
        student_name="Student A"
    )

    print("\nSESSION 1")

    student.update(
        performance=48,
        emotion="Frustrated",
        engagement=35
    )

    print(student.get_state())

    print("\nSESSION 2")

    student.update(
        performance=68,
        emotion="Neutral",
        engagement=65
    )

    print(student.get_state())

    print("\nSESSION 3")

    student.update(
        performance=86,
        emotion="Happy",
        engagement=88
    )

    print(student.get_state())