class LearningPathGenerator:

    def generate_path(
        self,
        emotion,
        predicted_performance,
        difficulty
    ):

        emotion = emotion.lower()

        # --------------------------------------------------
        # LOW PERFORMANCE / SUPPORT
        # --------------------------------------------------

        if predicted_performance < 50:

            path = [
                "Review fundamental concepts",
                "Study a simplified explanation",
                "Solve 3 basic practice questions",
                "Take a short easy quiz"
            ]

        # --------------------------------------------------
        # CONFUSED STUDENT
        # --------------------------------------------------

        elif emotion == "confused":

            path = [
                "Review the difficult concept",
                "Study a visual or simplified explanation",
                "Use hints while solving examples",
                "Attempt an easy quiz"
            ]

        # --------------------------------------------------
        # FRUSTRATED STUDENT
        # --------------------------------------------------

        elif emotion == "frustrated":

            path = [
                "Take a short learning break",
                "Review the concept step-by-step",
                "Solve guided practice questions",
                "Attempt a basic quiz"
            ]

        # --------------------------------------------------
        # BORED STUDENT
        # --------------------------------------------------

        elif emotion == "bored":

            path = [
                "Start an interactive activity",
                "Try a practical example",
                "Solve a timed challenge",
                "Attempt an interactive quiz"
            ]

        # --------------------------------------------------
        # HIGH PERFORMANCE
        # --------------------------------------------------

        elif predicted_performance >= 80:

            path = [
                "Review the current concept briefly",
                "Study an advanced concept",
                "Solve challenging problems",
                "Attempt an advanced quiz"
            ]

        # --------------------------------------------------
        # NORMAL LEARNING
        # --------------------------------------------------

        else:

            path = [
                "Continue the current lesson",
                "Study the next concept",
                "Practice example questions",
                "Take a standard quiz"
            ]

        return {
            "difficulty": difficulty,
            "learning_path": path
        }


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    generator = LearningPathGenerator()

    result = generator.generate_path(
        emotion="Confused",
        predicted_performance=62,
        difficulty="Easy"
    )

    print("\n===== PERSONALIZED LEARNING PATH =====")

    print("Difficulty:", result["difficulty"])

    print("\nRecommended Steps:")

    for number, step in enumerate(
        result["learning_path"],
        start=1
    ):
        print(f"{number}. {step}")