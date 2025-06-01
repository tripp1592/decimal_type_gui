# src/config.py
import json
from decimal import getcontext
from pathlib import Path
from typing import Any, Dict, Union

from .constants import DEFAULT_CONFIG


class Config:
    """Configuration manager for the calculator application."""

    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
        self._load_config()
        self._validate_config()
        self._apply_decimal_settings()

    def _load_config(self) -> None:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, "r") as f:
                self._config = json.load(f)
        except FileNotFoundError:
            self._config = DEFAULT_CONFIG.copy()
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in {self.config_path}, using defaults")
            self._config = DEFAULT_CONFIG.copy()

    def _validate_config(self) -> None:
        """Validate and sanitize configuration values."""
        # Ensure all required keys exist with defaults
        for key, default_value in DEFAULT_CONFIG.items():
            if key not in self._config:
                self._config[key] = default_value

        # Validate precision (must be positive integer)
        if (
            not isinstance(self._config["precision"], int)
            or self._config["precision"] <= 0
        ):
            self._config["precision"] = DEFAULT_CONFIG["precision"]

        # Validate decimal_places (must be non-negative integer)
        if (
            not isinstance(self._config["decimal_places"], int)
            or self._config["decimal_places"] < 0
        ):
            self._config["decimal_places"] = DEFAULT_CONFIG["decimal_places"]

        # Validate theme (must be string)
        if not isinstance(self._config["theme"], str):
            self._config["theme"] = DEFAULT_CONFIG["theme"]

    def _apply_decimal_settings(self) -> None:
        """Apply decimal precision settings."""
        getcontext().prec = self.precision

    def save_config(self) -> None:
        """Save current configuration to file."""
        try:
            with open(self.config_path, "w") as f:
                json.dump(self._config, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save config to {self.config_path}: {e}")

    @property
    def precision(self) -> int:
        return self._config["precision"]

    @precision.setter
    def precision(self, value: int) -> None:
        if isinstance(value, int) and value > 0:
            self._config["precision"] = value
            self._apply_decimal_settings()

    @property
    def decimal_places(self) -> int:
        return self._config["decimal_places"]

    @decimal_places.setter
    def decimal_places(self, value: int) -> None:
        if isinstance(value, int) and value >= 0:
            self._config["decimal_places"] = value

    @property
    def theme(self) -> str:
        return self._config["theme"]

    @theme.setter
    def theme(self, value: str) -> None:
        if isinstance(value, str):
            self._config["theme"] = value
