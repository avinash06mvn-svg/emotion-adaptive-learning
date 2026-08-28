"""Simple local test for the emotion webcam pipeline.

Run with:
    python test_webcam.py
Press Q or Esc in the camera window to stop.
"""

from avinash_module.webcam import stream_from_webcam


def show_payload(payload) -> None:
    print(payload.to_engine_json())


if __name__ == "__main__":
    print("Starting webcam. Press Q or Esc in the camera window to stop.")
    stream_from_webcam(
        student_id="STU001",
        on_payload=show_payload,
    )
