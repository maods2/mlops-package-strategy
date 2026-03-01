"""DAG parsing and execution primitives."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from mlops_core_lib.config_processor import ConfigProcessor, RuntimeConfig, load_yaml_file


@dataclass(frozen=True)
class StageDefinition:
    """Single DAG stage declaration."""

    name: str
    run: str
    depends_on: list[str]


class DAGEngine:
    """Load DAG YAML, resolve dependencies, and execute stages."""

    def __init__(self, handlers: dict[str, Callable[[RuntimeConfig], None]]) -> None:
        self._handlers = handlers

    def load_pipeline(self, pipeline_path: str | Path) -> dict[str, Any]:
        payload = load_yaml_file(pipeline_path)
        if not isinstance(payload, dict) or "pipeline" not in payload:
            msg = "Pipeline YAML must define a top-level 'pipeline' object"
            raise ValueError(msg)
        return payload

    def parse_stages(self, payload: dict[str, Any]) -> list[StageDefinition]:
        stages_raw = payload["pipeline"].get("stages", [])
        stages: list[StageDefinition] = []
        for stage in stages_raw:
            depends_raw = stage.get("depends_on", [])
            depends = [depends_raw] if isinstance(depends_raw, str) else list(depends_raw)
            stages.append(
                StageDefinition(name=stage["name"], run=stage["run"], depends_on=depends),
            )
        return stages

    def resolve_stage_order(self, stages: list[StageDefinition]) -> list[StageDefinition]:
        ordered: list[StageDefinition] = []
        stage_map = {stage.name: stage for stage in stages}
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(stage_name: str) -> None:
            if stage_name in visited:
                return
            if stage_name in visiting:
                msg = f"Cycle detected at stage: {stage_name}"
                raise ValueError(msg)
            if stage_name not in stage_map:
                msg = f"Unknown dependency: {stage_name}"
                raise ValueError(msg)
            visiting.add(stage_name)
            stage = stage_map[stage_name]
            for dep in stage.depends_on:
                visit(dep)
            visiting.remove(stage_name)
            visited.add(stage_name)
            ordered.append(stage)

        for stage in stages:
            visit(stage.name)

        return ordered

    def run(
        self,
        pipeline_path: str | Path,
        config_dir: str | Path,
        override_profiles: list[str] | None = None,
    ) -> None:
        payload = self.load_pipeline(pipeline_path)
        pipeline = payload["pipeline"]
        profiles = override_profiles or [str(item) for item in pipeline.get("config", [])]

        config_processor = ConfigProcessor(config_dir=config_dir)
        runtime_config = config_processor.load_profiles(profiles)

        ordered_stages = self.resolve_stage_order(self.parse_stages(payload))
        for stage in ordered_stages:
            handler = self._handlers.get(stage.run)
            if handler is None:
                msg = f"No handler registered for stage run='{stage.run}'"
                raise KeyError(msg)
            handler(runtime_config)
