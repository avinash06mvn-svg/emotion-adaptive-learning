import numpy as np
from sklearn.ensemble import RandomForestRegressor


class PerformancePredictor:
    """
    Predicts a student's expected learning performance
    using previous performance and engagement-related features.
    """

    def __init__(self):
        # Training data for prototype/demo
        #
        # Features:
        # 1. Previous score
        # 2. Study time (hours)
        # 3. Quiz accuracy
        # 4. Engagement level
        # 5. Learning consistency

        X = np.array([
            [40, 1, 45, 30, 35],
            [50, 1.5, 55, 40, 45],
            [60, 2, 60, 50, 55],
            [65, 2.5, 68, 60, 60],
            [70, 3, 72, 65, 68],
            [75, 3, 78, 70, 72],
            [80, 3.5, 82, 75, 78],
            [85, 4, 88, 82, 85],
            [90, 4.5, 92, 90, 90],
            [95, 5, 96, 95, 94]
        ])

        # Target = expected future performance
        y = np.array([
            45, 52, 61, 66, 71,
            76, 81, 86, 91, 95
        ])

        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

        self.model.fit(X, y)

    def predict(
        self,
        previous_score,
        study_time,
        quiz_accuracy,
        engagement,
        consistency
    ):
        """
        Predict future student performance.
        """

        features = np.array([[
            previous_score,
            study_time,
            quiz_accuracy,
            engagement,
            consistency
        ]])

        prediction = self.model.predict(features)[0]

        # Keep prediction between 0 and 100
        prediction = max(0, min(100, prediction))

        return round(prediction, 2)


# --------------------------------------------------
# TEST THE MODEL
# --------------------------------------------------

if __name__ == "__main__":

    predictor = PerformancePredictor()

    predicted_score = predictor.predict(
        previous_score=68,
        study_time=2.5,
        quiz_accuracy=70,
        engagement=60,
        consistency=65
    )

    print("Predicted Future Performance:", predicted_score, "%")