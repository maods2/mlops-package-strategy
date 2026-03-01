"""YAML configuration processor with profile-based deep merge."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def _parse_scalar(value: str) -> Any:
    stripped = value.strip()
    if stripped in {"true", "True"}:
        return True
    if stripped in {"false", "False"}:
        return False
    if stripped in {"null", "None", "~"}:
        return None
    if stripped.startswith('"') and stripped.endswith('"'):
        return stripped[1:-1]
    if stripped.startswith("'") and stripped.endswith("'"):
        return stripped[1:-1]
    try:
        if "." in stripped:
            return float(stripped)
        return int(stripped)
    except ValueError:
        return stripped


def _parse_block(lines: list[tuple[int, str]], start: int, indent: int) -> tuple[Any, int]:
    result_dict: dict[str, Any] = {}
    result_list: list[Any] = []
    mode: str | None = None
    index = start

    while index < len(lines):
        line_indent, content = lines[index]
        if line_indent < indent:
            break
        if line_indent > indent:
            msg = f"Invalid indentation near '{content}'"
            raise ValueError(msg)

        if content.startswith("- "):
            if mode is None:
                mode = "list"
            if mode != "list":
                msg = "Cannot mix mapping and list items at same indentation"
                raise ValueError(msg)
            item_content = content[2:].strip()
            if ":" in item_content:
                key, value = item_content.split(":", maxsplit=1)
                item: dict[str, Any] = {key.strip(): _parse_scalar(value) if value.strip() else None}
                index += 1
                if index < len(lines) and lines[index][0] > indent:
                    nested, index = _parse_block(lines, index, indent + 2)
                    if item[key.strip()] is None and isinstance(nested, dict):
                        item[key.strip()] = nested
                    elif isinstance(nested, dict):
                        item.update(nested)
                    else:
                        item["nested"] = nested
                result_list.append(item)
                continue
            if not item_content:
                index += 1
                nested_item, index = _parse_block(lines, index, indent + 2)
                result_list.append(nested_item)
                continue
            result_list.append(_parse_scalar(item_content))
            index += 1
            continue

        if mode is None:
            mode = "dict"
        if mode != "dict":
            msg = "Cannot mix list and mapping items at same indentation"
            raise ValueError(msg)

        key, value = content.split(":", maxsplit=1)
        key = key.strip()
        value = value.strip()
        index += 1
        if value:
            result_dict[key] = _parse_scalar(value)
        else:
            if index < len(lines) and lines[index][0] > indent:
                nested, index = _parse_block(lines, index, indent + 2)
                result_dict[key] = nested
            else:
                result_dict[key] = {}

    return (result_list if mode == "list" else result_dict), index


def load_yaml_file(path: str | Path) -> dict[str, Any]:
    """Parse a YAML file with lightweight support for mappings/lists."""
    raw_lines = Path(path).read_text(encoding="utf-8").splitlines()
    lines: list[tuple[int, str]] = []
    for line in raw_lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        lines.append((indent, line.strip()))
    if not lines:
        return {}
    parsed, _ = _parse_block(lines, start=0, indent=0)
    if not isinstance(parsed, dict):
        msg = "YAML root must be a mapping"
        raise TypeError(msg)
    return parsed


class RuntimeConfig:
    """Runtime configuration container with dot-access."""

    def __init__(self, values: dict[str, Any]) -> None:
        self._values = values

    def __getattr__(self, item: str) -> Any:
        if item not in self._values:
            msg = f"Unknown configuration key: {item}"
            raise AttributeError(msg)
        return self._values[item]

    @classmethod
    def model_validate(cls, values: dict[str, Any]) -> "RuntimeConfig":
        return cls(values=values)

    def model_dump(self) -> dict[str, Any]:
        return dict(self._values)


def deep_merge_dicts(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Deep merge two dictionaries with override semantics."""
    result: dict[str, Any] = dict(base)
    for key, value in override.items():
        current = result.get(key)
        if isinstance(current, dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(current, value)
        else:
            result[key] = value
    return result


class ConfigProcessor:
    """Load and merge YAML configuration profiles from a directory."""

    def __init__(self, config_dir: str | Path) -> None:
        self._config_dir = Path(config_dir)

    def load_profile(self, profile: str) -> dict[str, Any]:
        path = self._config_dir / f"{profile}.yaml"
        if not path.exists():
            msg = f"Configuration profile not found: {path}"
            raise FileNotFoundError(msg)
        data = load_yaml_file(path)
        if not isinstance(data, dict):
            msg = f"Profile {profile} must contain a dictionary at root"
            raise TypeError(msg)
        return data

    def load_profiles(self, profiles: list[str]) -> RuntimeConfig:
        merged: dict[str, Any] = {}
        for profile in profiles:
            merged = deep_merge_dicts(merged, self.load_profile(profile))
        return RuntimeConfig.model_validate(merged)


__all__ = ["ConfigProcessor", "RuntimeConfig", "deep_merge_dicts", "load_yaml_file"]
