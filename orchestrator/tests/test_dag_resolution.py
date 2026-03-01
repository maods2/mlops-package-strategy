from orchestrator.dag import DAGEngine, StageDefinition


def test_dag_resolution_orders_dependencies_first() -> None:
    engine = DAGEngine(handlers={})
    stages = [
        StageDefinition(name="train", run="train_step", depends_on=["preprocess"]),
        StageDefinition(name="preprocess", run="preprocess_step", depends_on=[]),
    ]

    ordered = engine.resolve_stage_order(stages)

    assert [stage.name for stage in ordered] == ["preprocess", "train"]
