from typing import Any

from mlops_core_lib.interfaces import TrainingWrapper


class DummyTrainer(TrainingWrapper):
    def train(self, config: dict[str, Any]) -> dict[str, Any]:
        return {"status": "ok", "epochs": config.get("epochs", 1)}


def test_training_wrapper_implementation() -> None:
    trainer = DummyTrainer()
    output = trainer.train({"epochs": 5})

    assert output["epochs"] == 5
