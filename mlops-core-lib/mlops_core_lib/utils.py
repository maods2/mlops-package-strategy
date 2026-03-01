"""Utility helpers for CLI argument parsing and profile handling."""

from __future__ import annotations


def parse_config_arg(argument: str) -> list[str]:
    """Parse CLI value like "config=global,dev" into profile list."""
    if not argument.startswith("config="):
        msg = "Config argument must start with 'config='"
        raise ValueError(msg)
    raw_profiles = argument.split("=", maxsplit=1)[1]
    profiles = [profile.strip() for profile in raw_profiles.split(",") if profile.strip()]
    if not profiles:
        msg = "At least one config profile must be provided"
        raise ValueError(msg)
    return profiles
