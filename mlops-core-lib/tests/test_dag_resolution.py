from mlops_core_lib.utils import parse_config_arg


def test_parse_config_arg_returns_profiles() -> None:
    assert parse_config_arg("config=global,dev") == ["global", "dev"]
