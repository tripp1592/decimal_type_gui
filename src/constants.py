# src/constants.py
"""Constants for the calculator application."""

from typing import List, Tuple

# Window dimensions
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 550

# Display settings
DISPLAY_HEIGHT = 50
DISPLAY_FONT_SIZE = 20
DISPLAY_FONT_FAMILY = "Consolas"

# Button settings
BUTTON_FONT_SIZE = 16
BUTTON_FONT_FAMILY = "Consolas"

# Layout settings
LAYOUT_MARGIN = 8
LAYOUT_SPACING = 6

# Button layout definition
BUTTON_LAYOUT: List[Tuple[str, ...]] = [
    ("7", "8", "9", "/"),
    ("4", "5", "6", "*"),
    ("1", "2", "3", "-"),
]

# Special buttons configuration
SPECIAL_BUTTONS = {
    "0": {"row": 4, "col": 0, "rowspan": 1, "colspan": 2},
    ".": {"row": 4, "col": 2, "rowspan": 1, "colspan": 1},
    "+": {"row": 4, "col": 3, "rowspan": 1, "colspan": 1},
    "C": {"row": 5, "col": 0, "rowspan": 1, "colspan": 2},
    "⌫": {"row": 5, "col": 2, "rowspan": 1, "colspan": 1},
    "=": {"row": 5, "col": 3, "rowspan": 1, "colspan": 1},
}

# Valid input characters
VALID_INPUT_CHARS = "0123456789.+-*/"

# Default configuration
DEFAULT_CONFIG = {"precision": 28, "decimal_places": 2, "theme": "DarkGrey13"}

# Error messages
ERROR_MESSAGES = {
    "INVALID_EXPRESSION": "Invalid Expression",
    "DIVISION_BY_ZERO": "Division by Zero",
    "OVERFLOW": "Number Too Large",
    "GENERAL_ERROR": "Error",
}
