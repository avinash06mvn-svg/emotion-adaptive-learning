from performance_prediction import PerformancePredictor
from recommendation import AdaptiveLearningEngine


def run_student_scenario(
    name,
    emotion,
    previous_score,
    study_time,
    quiz_accuracy,
    engagement,
    consistency
):

    predictor = PerformancePredictor()
    engine = AdaptiveLearningEngine()

    predicted_score = predictor.predict(
        previous_score=previous_score,
        study_time=study_time,
        quiz_accuracy=quiz_accuracy,
        engagement=engagement,
        consistency=consistency
    )

    recommendation = engine.get_recommendation(
        emotion=emotion,
        predicted_performance=predicted_score,
        engagement=engagement
    )

    print("\n" + "=" * 50)
    print(f"STUDENT: {name}")
    print("=" * 50)

    print(f"Emotion              : {emotion}")
    print(f"Previous Score       : {previous_score}%")
    print(f"Engagement           : {engagement}%")
    print(f"Predicted Performance: {predicted_score}%")

    print("\n--- ADAPTIVE DECISION ---")
    print(f"Difficulty           : {recommendation['difficulty']}")
    print(f"Content              : {recommendation['content']}")
    print(f"Activity             : {recommendation['activity']}")
    print(f"Reason               : {recommendation['message']}")


if __name__ == "__main__":

    # Student 1: Confused learner
    run_student_scenario(
        name="Student A",
        emotion="Confused",
        previous_score=60,
        study_time=2,
        quiz_accuracy=62,
        engagement=45,
        consistency=55
    )

    # Student 2: High-performing learner
    run_student_scenario(
        name="Student B",
        emotion="Happy",
        previous_score=88,
        study_time=4,
        quiz_accuracy=90,
        engagement=90,
        consistency=88
    )

    # Student 3: Frustrated learner
    run_student_scenario(
        name="Student C",
        emotion="Frustrated",
        previous_score=48,
        study_time=1.5,
        quiz_accuracy=45,
        engagement=30,
        consistency=40
    )

    # Student 4: Bored learner
    run_student_scenario(
        name="Student D",
        emotion="Bored",
        previous_score=72,
        study_time=3,
        quiz_accuracy=75,
        engagement=25,
        consistency=70
    )