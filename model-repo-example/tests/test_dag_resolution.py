from orchestrator.dag import DAGEngine

from model_repo_example.stages import get_stage_handlers


def test_pipeline_stage_handlers_resolve() -> None:
    engine = DAGEngine(handlers=get_stage_handlers())
    assert "train_step" in engine._handlers
