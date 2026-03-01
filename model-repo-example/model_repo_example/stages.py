"""Pipeline stage handlers for training and prediction DAGs."""

from __future__ import annotations

from collections.abc import Callable

from mlops_core_lib.config_processor import RuntimeConfig

from model_repo_example.implementations import ConsoleTracker, ExamplePredictor, ExampleTrainer


def preprocess_step(config: RuntimeConfig) -> None:
    print(f"preprocess::dataset={config.data['dataset']}")


def train_step(config: RuntimeConfig) -> None:
    trainer = ExampleTrainer(tracker=ConsoleTracker())
    trainer.train(config.model_dump())


def predict_step(config: RuntimeConfig) -> None:
    predictor = ExamplePredictor()
    prediction = predictor.predict(features=[0.2, 0.3, 0.8], config=config.model_dump())
    print(f"prediction::{prediction:.4f}")


def get_stage_handlers() -> dict[str, Callable[[RuntimeConfig], None]]:
    return {
        "preprocess_step": preprocess_step,
        "train_step": train_step,
        "predict_step": predict_step,
    }
