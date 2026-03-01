"""CLI entrypoint for orchestrator package."""

from __future__ import annotations

import argparse

from orchestrator.dag import DAGEngine


def _noop_handler(_: object) -> None:
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a YAML pipeline DAG")
    parser.add_argument("pipeline", help="Path to pipeline YAML")
    parser.add_argument("config_dir", help="Directory containing config profiles")
    args = parser.parse_args()

    engine = DAGEngine(handlers={"noop": _noop_handler})
    engine.run(args.pipeline, args.config_dir)


if __name__ == "__main__":
    main()
