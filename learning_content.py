"""Small content selector used by the adaptive-learning demo."""


def get_learning_content(subject: str, difficulty: str, activity: str) -> dict:
    content = {
        "Easy": {
            "title": f"{subject} - Basic Concepts",
            "description": "Review the fundamental concepts with simple explanations and examples.",
            "activity": "Hints + Easy Quiz",
        },
        "Moderate": {
            "title": f"{subject} - Concept Practice",
            "description": "Study the main concepts with examples and practice questions.",
            "activity": "Practice Quiz",
        },
        "Advanced": {
            "title": f"{subject} - Advanced Concepts",
            "description": "Explore advanced concepts and solve challenging problems.",
            "activity": "Challenge Quiz",
        },
    }
    return content.get(difficulty, content["Moderate"])
