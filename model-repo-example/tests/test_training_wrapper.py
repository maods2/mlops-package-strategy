from model_repo_example.implementations import ConsoleTracker, ExampleTrainer


def test_example_trainer_returns_training_metadata() -> None:
    trainer = ExampleTrainer(tracker=ConsoleTracker())
    result = trainer.train({"training": {"epochs": 3, "learning_rate": 0.2}})

    assert result["status"] == "trained"
    assert result["epochs"] == 3
