from mlops_core_lib.config_processor import deep_merge_dicts


def test_deep_merge_dicts_overrides_nested_values() -> None:
    base = {"service": {"host": "localhost", "port": 8000}, "mode": "prod"}
    override = {"service": {"port": 9000}, "mode": "dev"}

    merged = deep_merge_dicts(base, override)

    assert merged == {"service": {"host": "localhost", "port": 9000}, "mode": "dev"}
