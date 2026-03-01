"""CLI runner for the model repository."""

from __future__ import annotations

import argparse
from pathlib import Path

from mlops_core_lib.config_processor import ConfigProcessor
from mlops_core_lib.utils import parse_config_arg
from orchestrator.dag import DAGEngine

from model_repo_example.stages import get_stage_handlers


def main() -> None:
    parser = argparse.ArgumentParser(description="Run model repository pipelines")
    parser.add_argument("pipeline", choices=["train", "predict"], help="Pipeline to execute")
    parser.add_argument("config_arg", help="Config profiles in form config=global,dev")
    args = parser.parse_args()

    package_root = Path(__file__).resolve().parent
    pipeline_path = package_root / "pipelines" / f"{args.pipeline}.yaml"
    config_dir = package_root / "configs"

    selected_profiles = parse_config_arg(args.config_arg)
    processor = ConfigProcessor(config_dir=config_dir)
    _ = processor.load_profiles(selected_profiles)

    engine = DAGEngine(handlers=get_stage_handlers())
    engine.run(pipeline_path=pipeline_path, config_dir=config_dir, override_profiles=selected_profiles)


if __name__ == "__main__":
    main()
