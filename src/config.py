# src/config.py

import json
from pathlib import Path

DEFAULTS = {"precision": 28, "decimal_places": 2, "theme": "light"}


class ConfigError(Exception):
    """Raised when the configuration is invalid."""

    pass


def load_config():
    # Expect config.json at project root
    config_path = Path(__file__).parent.parent / "config.json"
    if not config_path.exists():
        cfg = DEFAULTS.copy()
    else:
        try:
            raw = config_path.read_text()
            data = json.loads(raw) if raw.strip() else {}
        except json.JSONDecodeError as e:
            raise ConfigError(f"Invalid JSON in config.json: {e}")
        cfg = DEFAULTS.copy()
        for key in DEFAULTS:
            if key in data:
                cfg[key] = data[key]

    # Validate
    if not isinstance(cfg["precision"], int) or cfg["precision"] <= 0:
        raise ConfigError("`precision` must be a positive integer")
    if not isinstance(cfg["decimal_places"], int) or cfg["decimal_places"] < 0:
        raise ConfigError("`decimal_places` must be a non-negative integer")
    if cfg["theme"] not in ("light", "dark"):
        raise ConfigError("`theme` must be 'light' or 'dark'")

    return cfg


cfg = load_config()
