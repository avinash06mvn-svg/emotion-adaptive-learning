def show_payload(payload) -> None:
    print("CALLBACK FIRED")
    try:
        data = payload.to_engine_dict()
        print("DATA:", data)
        result = engine.process_student(
            emotion=data["emotion"],
            previous_score=60,
            study_time=2,
            quiz_accuracy=62,
            engagement=emotion_to_engagement(data["learning_state"]),
            consistency=55,
        )
        print(
            f"{data['emotion']:>8} -> {data['learning_state']:<11} | "
            f"difficulty={result['difficulty']:<8} | activity={result['activity']}"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
