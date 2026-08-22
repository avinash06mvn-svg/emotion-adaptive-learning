class AdaptiveLearningEngine:
    """
    Adaptive Learning Engine

    Uses:
    - Student emotion
    - Predicted performance
    - Engagement level

    to decide:
    - Learning difficulty
    - Content type
    - Learning activity
    """

    def get_recommendation(
        self,
        emotion,
        predicted_performance,
        engagement
    ):

        # --------------------------------------------------
        # LOW PERFORMANCE
        # --------------------------------------------------

        if predicted_performance < 50:

            difficulty = "Easy"
            content = "Simplified Explanation"
            activity = "Hints + Basic Practice"
            message = "Student needs additional support."

        # --------------------------------------------------
        # MEDIUM PERFORMANCE
        # --------------------------------------------------

        elif predicted_performance < 75:

            difficulty = "Moderate"
            content = "Concept Explanation + Examples"
            activity = "Practice Quiz"
            message = "Continue with guided learning."

        # --------------------------------------------------
        # HIGH PERFORMANCE
        # --------------------------------------------------

        else:

            difficulty = "Advanced"
            content = "Advanced Concepts"
            activity = "Challenge Quiz"
            message = "Student is ready for higher difficulty."

        # --------------------------------------------------
        # EMOTION ADAPTATION
        # --------------------------------------------------

        if emotion.lower() == "confused":

            difficulty = "Easy"
            content = "Simplified Explanation"
            activity = "Hints + Easy Quiz"
            message = "Student appears confused. Simplifying the learning material."

        elif emotion.lower() == "frustrated":

            difficulty = "Easy"
            content = "Step-by-Step Explanation"
            activity = "Guided Practice"
            message = "Student appears frustrated. Reducing difficulty."

        elif emotion.lower() == "bored":

            activity = "Interactive Quiz"
            message = "Student appears bored. Increasing interaction."

        elif emotion.lower() == "happy":

            if predicted_performance >= 70:
                difficulty = "Advanced"
                activity = "Challenge Quiz"

            message = "Student is engaged. Continue with challenging content."

        # --------------------------------------------------
        # LOW ENGAGEMENT
        # --------------------------------------------------

        if engagement < 40:

            activity = "Interactive Activity"
            message += " Low engagement detected, so an interactive activity is recommended."

        # --------------------------------------------------
        # RETURN RESULT
        # --------------------------------------------------

        return {
            "difficulty": difficulty,
            "content": content,
            "activity": activity,
            "message": message
        }


# --------------------------------------------------
# TEST THE ADAPTIVE ENGINE
# --------------------------------------------------

if __name__ == "__main__":

    engine = AdaptiveLearningEngine()

    result = engine.get_recommendation(
        emotion="Confused",
        predicted_performance=62,
        engagement=45
    )

    print("\n===== ADAPTIVE LEARNING RESULT =====")

    print("Difficulty :", result["difficulty"])
    print("Content    :", result["content"])
    print("Activity   :", result["activity"])
    print("Reason     :", result["message"])