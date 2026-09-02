"""Low-level webcam test for Avinash's emotion detector."""

import cv2

from avinash_module.emotion_detector import EmotionDetector


def main() -> None:
    detector = EmotionDetector()
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise RuntimeError("Could not open webcam")

    print("Camera started. Press Q or Esc in the camera window to quit.")
    try:
        while True:
            success, frame = camera.read()
            if not success:
                print("Could not read frame")
                break

            observation = detector.detect(frame)
            if observation is None:
                print("No emotion detected")
            else:
                print(f"Emotion: {observation.emotion} | Confidence: {observation.confidence:.2f}")

            cv2.imshow("Emotion Test - Press Q to quit", frame)
            if cv2.waitKey(1) & 0xFF in (ord("q"), 27):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
