"""Tests for the adaptive engine."""

from adaptive_learning.adaptive_engine import AdaptiveEngine


def test_engine_init():
    assert AdaptiveEngine().state == {}
