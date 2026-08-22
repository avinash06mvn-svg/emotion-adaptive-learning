"""Main application entry point."""

from adaptive_learning.adaptive_engine import AdaptiveEngine


def main() -> None:
    engine = AdaptiveEngine()
    print("Emotion Adaptive Learning app running", engine)


if __name__ == "__main__":
    main()
