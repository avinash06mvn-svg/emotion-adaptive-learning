from performance_prediction import PerformancePredictor
from recommendation import AdaptiveLearningEngine
from learning_path import LearningPathGenerator


class AdaptiveEngine:

    def __init__(self):

        self.predictor = PerformancePredictor()
        self.recommender = AdaptiveLearningEngine()
        self.path_generator = LearningPathGenerator()

    def process_student(
        self,
        emotion,
        previous_score,
        study_time,
        quiz_accuracy,
        engagement,
        consistency
    ):

        # 1. Predict future performance
        predicted_performance = self.predictor.predict(
            previous_score=previous_score,
            study_time=study_time,
            quiz_accuracy=quiz_accuracy,
            engagement=engagement,
            consistency=consistency
        )

        # 2. Generate adaptive recommendation
        recommendation = self.recommender.get_recommendation(
            emotion=emotion,
            predicted_performance=predicted_performance,
            engagement=engagement
        )

        # 3. Generate personalized learning path
        learning_path = self.path_generator.generate_path(
            emotion=emotion,
            predicted_performance=predicted_performance,
            difficulty=recommendation["difficulty"]
        )

        return {
            "emotion": emotion,
            "predicted_performance": predicted_performance,
            "difficulty": recommendation["difficulty"],
            "content": recommendation["content"],
            "activity": recommendation["activity"],
            "reason": recommendation["message"],
            "learning_path": learning_path["learning_path"]
        }


# --------------------------------------------------
# TEST COMPLETE ENGINE
# --------------------------------------------------

if __name__ == "__main__":

    engine = AdaptiveEngine()

    result = engine.process_student(
        emotion="Confused",
        previous_score=60,
        study_time=2,
        quiz_accuracy=62,
        engagement=45,
        consistency=55
    )

    print("\n")
    print("=" * 55)
    print("       ADAPTIVE LEARNING ENGINE")
    print("=" * 55)

    print(f"\nEmotion: {result['emotion']}")

    print(
        f"Predicted Performance: "
        f"{result['predicted_performance']}%"
    )

    print(
        f"Difficulty: "
        f"{result['difficulty']}"
    )

    print(
        f"Content: "
        f"{result['content']}"
    )

    print(
        f"Activity: "
        f"{result['activity']}"
    )

    print(
        f"\nReason: "
        f"{result['reason']}"
    )

    print("\n----- PERSONALIZED LEARNING PATH -----")

    for i, step in enumerate(
        result["learning_path"],
        start=1
    ):
        print(f"{i}. {step}")

    print("\n" + "=" * 55)