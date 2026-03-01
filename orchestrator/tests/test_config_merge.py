from pathlib import Path

from mlops_core_lib.config_processor import ConfigProcessor


def test_profile_override_logic(tmp_path: Path) -> None:
    (tmp_path / "global.yaml").write_text("service:\n  retries: 1\n", encoding="utf-8")
    (tmp_path / "dev.yaml").write_text("service:\n  retries: 3\n", encoding="utf-8")

    processor = ConfigProcessor(config_dir=tmp_path)
    merged = processor.load_profiles(["global", "dev"])

    assert merged.service["retries"] == 3
