"""Core interface definitions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ExperimentTracker(ABC):
    """Abstract experiment tracking interface."""

    @abstractmethod
    def log_metric(self, key: str, value: float) -> None:
        """Log a scalar metric."""


class ModelRegistry(ABC):
    """Abstract model registry interface."""

    @abstractmethod
    def register_model(self, model_name: str, artifact_uri: str) -> str:
        """Register a model artifact and return version identifier."""


class CloudClient(ABC):
    """Abstract cloud interface."""

    @abstractmethod
    def upload_file(self, local_path: str, remote_uri: str) -> None:
        """Upload local artifact to remote URI."""


class TrainingWrapper(ABC):
    """Training workflow contract."""

    @abstractmethod
    def train(self, config: dict[str, Any]) -> dict[str, Any]:
        """Run training and return metadata."""


class PredictionWrapper(ABC):
    """Prediction workflow contract."""

    @abstractmethod
    def predict(self, features: list[float], config: dict[str, Any]) -> float:
        """Generate prediction from features."""
