import sys
from pathlib import Path

import cv2
import numpy as np
import streamlit as st

from avinash_module.emotion_detector import EmotionDetector
from avinash_module.learning_state import (
    TemporalEmotionSmoother,
    build_payload,
)
from learning_content import get_learning_content

# The existing adaptive engine uses local imports, so expose its folder.
ROOT = Path(__file__).resolve().parent
ENGINE_DIR = ROOT / "adaptive_learning"
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from adaptive_engine import AdaptiveEngine  # noqa: E402


st.set_page_config(
    page_title="Emotion-Aware Adaptive Learning",
    page_icon="🎓",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main-title { font-size: 42px; font-weight: 700; text-align: center; margin-bottom: 5px; }
    .subtitle { text-align: center; font-size: 20px; color: #666; margin-bottom: 30px; }
    .feature-card { padding: 25px; border-radius: 15px; border: 1px solid #ddd; min-height: 180px; }
    .step-card { text-align: center; padding: 20px; }
    </style>
    """,
    unsafe_allow_html=True,
)


def emotion_to_engagement(learning_state: str) -> int:
    return {
        "engaged": 85,
        "normal": 65,
        "struggling": 45,
        "frustrated": 30,
        "anxious": 35,
        "bored": 25,
    }.get(learning_state.lower(), 60)


@st.cache_resource
def get_detector() -> EmotionDetector:
    return EmotionDetector()


@st.cache_resource
def get_engine() -> AdaptiveEngine:
    return AdaptiveEngine()


if "emotion_smoother" not in st.session_state:
    st.session_state.emotion_smoother = TemporalEmotionSmoother(window_size=5)
if "smoother_student_id" not in st.session_state:
    st.session_state.smoother_student_id = ""

st.markdown(
    '<div class="main-title">🎓 Emotion-Aware Adaptive Learning</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">AI-Powered Personalized Education</div>',
    unsafe_allow_html=True,
)
st.write(
    "A smart learning system that adapts educational content "
    "according to the student's emotional state and learning performance."
)
st.divider()

st.subheader("🌟 Personalized Learning with AI")
col1, col2 = st.columns([1.4, 1])
with col1:
    st.write(
        """
        Traditional learning systems provide the same content to every student.

        Our **Emotion-Aware Adaptive Learning System** considers:

        - 🧠 Student emotional state
        - 📈 Previous learning performance
        - 📝 Quiz accuracy
        - ⏱️ Study time
        - 🎯 Engagement and consistency
        """
    )
with col2:
    st.info(
        """
        ### 🤖 How AI Helps

        **Emotion Detection**

        ↓

        **Performance Prediction**

        ↓

        **Adaptive Recommendation**

        ↓

        **Personalized Learning**
        """
    )

st.divider()
st.subheader("🚀 System Features")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        <div class="feature-card">
        <h3>😊 Emotion Detection</h3>
        Identifies the student's current emotional learning state.
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="feature-card">
        <h3>🧠 Adaptive Learning</h3>
        Adjusts difficulty, content type, activity, and learning path.
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """
        <div class="feature-card">
        <h3>📊 Learning Analytics</h3>
        Tracks quiz performance, predictions, progress, and emotions.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()
st.subheader("⚙️ How the System Works")
steps = [
    ("👤", "Student", "Starts a learning session"),
    ("📷", "Webcam", "Captures a face image"),
    ("😊", "Emotion", "Emotion is detected"),
    ("🤖", "Prediction", "Performance is predicted"),
    ("📚", "Adaptation", "Content is personalized"),
]
cols = st.columns(len(steps))
for column, (icon, title, description) in zip(cols, steps):
    with column:
        st.markdown(
            f'<div class="step-card"><h2>{icon}</h2><b>{title}</b><p>{description}</p></div>',
            unsafe_allow_html=True,
        )

st.divider()
st.subheader("📷 Live Emotion Monitor")
st.caption(
    "Allow camera access, capture a frame, and the system will send the detected "
    "learning state to Raghave's adaptive engine."
)

left, right = st.columns(2)
with left:
    student_id = st.text_input("Student ID", value="STUDENT001")
    subject = st.text_input("Subject", value="Java Loops")
    camera_image = st.camera_input("Take a webcam picture")
with right:
    st.markdown("**Student performance information**")
    previous_score = st.number_input("Previous score", min_value=0.0, max_value=100.0, value=68.0)
    study_time = st.number_input("Study time (hours)", min_value=0.0, value=2.5, step=0.5)
    quiz_accuracy = st.number_input("Quiz accuracy (%)", min_value=0.0, max_value=100.0, value=70.0)
    consistency = st.number_input("Consistency (%)", min_value=0.0, max_value=100.0, value=65.0)

if student_id != st.session_state.smoother_student_id:
    st.session_state.emotion_smoother = TemporalEmotionSmoother(window_size=5)
    st.session_state.smoother_student_id = student_id

if camera_image is not None:
    image_bytes = np.frombuffer(camera_image.getvalue(), dtype=np.uint8)
    frame = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
    if frame is None:
        st.error("The camera image could not be read.")
    else:
        st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), caption="Captured frame", use_container_width=True)
        observation = get_detector().detect(frame)
        if observation is None:
            st.warning("No face or reliable emotion was detected. Try another picture with your face clearly visible.")
        else:
            payload = build_payload(student_id, observation, st.session_state.emotion_smoother)
            if payload is None:
                st.warning("The prediction was below the 70% confidence threshold.")
            else:
                data = payload.to_engine_dict()
                engagement = emotion_to_engagement(data["learning_state"])
                result = get_engine().process_student(
                    emotion=data["emotion"],
                    previous_score=previous_score,
                    study_time=study_time,
                    quiz_accuracy=quiz_accuracy,
                    engagement=engagement,
                    consistency=consistency,
                )
                content = get_learning_content(subject, result["difficulty"], result["activity"])

                st.success("Emotion processed and sent to the adaptive engine.")
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Emotion", data["emotion"].title())
                m2.metric("Confidence", f"{data['emotion_confidence']:.0%}")
                m3.metric("Learning state", data["learning_state"].title())
                m4.metric("Predicted performance", f"{result['predicted_performance']:.2f}%")

                st.subheader("📚 Adaptive Recommendation")
                st.write(f"**Difficulty:** {result['difficulty']}")
                st.write(f"**Content:** {content['title']}")
                st.write(f"**Activity:** {result['activity']}")
                st.write(f"**Reason:** {result['reason']}")
                st.json(data)

st.divider()
st.caption("🎓 Emotion-Aware Adaptive Learning System | AI-Powered Personalized Education")
