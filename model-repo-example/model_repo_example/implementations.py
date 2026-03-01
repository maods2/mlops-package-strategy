"""Concrete implementations of core abstractions."""

from __future__ import annotations

from typing import Any

from mlops_core_lib.interfaces import ExperimentTracker, PredictionWrapper, TrainingWrapper


class ConsoleTracker(ExperimentTracker):
    """Simple tracker that writes metrics to stdout."""

    def log_metric(self, key: str, value: float) -> None:
        print(f"metric::{key}={value}")


class ExampleTrainer(TrainingWrapper):
    """Minimal deterministic training simulation."""

    def __init__(self, tracker: ExperimentTracker) -> None:
        self._tracker = tracker

    def train(self, config: dict[str, Any]) -> dict[str, Any]:
        epochs = int(config.get("training", {}).get("epochs", 1))
        learning_rate = float(config.get("training", {}).get("learning_rate", 0.1))
        score = min(0.99, 0.5 + epochs * learning_rate * 0.05)
        self._tracker.log_metric("train_score", score)
        return {"status": "trained", "score": score, "epochs": epochs}


class ExamplePredictor(PredictionWrapper):
    """Simple prediction simulation."""

    def predict(self, features: list[float], config: dict[str, Any]) -> float:
        bias = float(config.get("serving", {}).get("bias", 0.0))
        weight = float(config.get("serving", {}).get("weight", 1.0))
        return sum(features) * weight + bias
