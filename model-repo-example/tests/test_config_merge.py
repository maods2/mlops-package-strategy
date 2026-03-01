from pathlib import Path

from mlops_core_lib.config_processor import ConfigProcessor


def test_profile_merging_for_model_repo(tmp_path: Path) -> None:
    (tmp_path / "global.yaml").write_text("training:\n  epochs: 2\n", encoding="utf-8")
    (tmp_path / "dev.yaml").write_text("training:\n  epochs: 9\n", encoding="utf-8")

    processor = ConfigProcessor(config_dir=tmp_path)
    config = processor.load_profiles(["global", "dev"])

    assert config.training["epochs"] == 9
