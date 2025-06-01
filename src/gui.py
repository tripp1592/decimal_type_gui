# src/gui.py
from typing import Dict

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QKeyEvent
from PyQt6.QtWidgets import QGridLayout, QLineEdit, QPushButton, QSizePolicy, QWidget

from .constants import (
    BUTTON_FONT_FAMILY,
    BUTTON_FONT_SIZE,
    BUTTON_LAYOUT,
    DISPLAY_FONT_FAMILY,
    DISPLAY_FONT_SIZE,
    DISPLAY_HEIGHT,
    LAYOUT_MARGIN,
    LAYOUT_SPACING,
    SPECIAL_BUTTONS,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from .core import DecimalCalculator


class CalculatorWidget(QWidget):
    """Main calculator UI widget."""

    def __init__(self, calculator: DecimalCalculator):
        super().__init__()
        self.calculator = calculator
        self.buttons: Dict[str, QPushButton] = {}

        self._setup_ui()
        self._connect_signals()
        self._update_display()

    def _setup_ui(self) -> None:
        """Initialize the user interface."""
        self.setWindowTitle("Decimal Calculator")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Main layout
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(
            LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN, LAYOUT_MARGIN
        )
        self.layout.setSpacing(LAYOUT_SPACING)

        # Setup components
        self._setup_display()
        self._setup_buttons()

    def _setup_display(self) -> None:
        """Setup the calculator display."""
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setFont(QFont(DISPLAY_FONT_FAMILY, DISPLAY_FONT_SIZE))
        self.layout.addWidget(self.display, 0, 0, 1, 4)

    def _setup_buttons(self) -> None:
        """Setup all calculator buttons."""
        btn_font = QFont(BUTTON_FONT_FAMILY, BUTTON_FONT_SIZE)

        # Create main grid buttons
        self._create_grid_buttons(btn_font)

        # Create special buttons
        self._create_special_buttons(btn_font)

    def _create_grid_buttons(self, font: QFont) -> None:
        """Create the main grid of number and operator buttons."""
        for row_idx, row in enumerate(BUTTON_LAYOUT, start=1):
            for col_idx, char in enumerate(row):
                btn = self._create_button(char, font)
                btn.clicked.connect(lambda checked, c=char: self._on_input_button(c))
                self.layout.addWidget(btn, row_idx, col_idx)
                self.buttons[char] = btn

    def _create_special_buttons(self, font: QFont) -> None:
        """Create special buttons (0, ., +, C, ⌫, =) with custom layouts."""
        special_handlers = {
            "0": lambda: self._on_input_button("0"),
            ".": lambda: self._on_input_button("."),
            "+": lambda: self._on_input_button("+"),
            "C": self._on_clear,
            "⌫": self._on_backspace,
            "=": self._on_calculate,
        }

        for text, config in SPECIAL_BUTTONS.items():
            btn = self._create_button(text, font)
            btn.clicked.connect(special_handlers[text])
            self.layout.addWidget(
                btn, config["row"], config["col"], config["rowspan"], config["colspan"]
            )
            self.buttons[text] = btn

    def _create_button(self, text: str, font: QFont) -> QPushButton:
        """Create a calculator button with consistent styling."""
        btn = QPushButton(text)
        btn.setFont(font)
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        return btn

    def _connect_signals(self) -> None:
        """Connect signals and setup keyboard support."""
        # Enable keyboard focus and handle key events
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Handle keyboard input."""
        key = event.key()

        if key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
            self._on_calculate()
        elif key == Qt.Key.Key_Backspace:
            self._on_backspace()
        elif key == Qt.Key.Key_Escape:
            self._on_clear()
        else:
            text = event.text()
            if text and self.calculator.is_valid_input(text):
                self._on_input_button(text)

    def _update_display(self) -> None:
        """Update the display with current expression."""
        self.display.setText(self.calculator.expression)

    def _on_input_button(self, char: str) -> None:
        """Handle input button press."""
        # Clear error state on new input
        if self.calculator.is_error_state():
            self.calculator.clear_expression()

        self.calculator.append_to_expression(char)
        self._update_display()

    def _on_clear(self) -> None:
        """Handle clear button press."""
        self.calculator.clear_expression()
        self._update_display()

    def _on_backspace(self) -> None:
        """Handle backspace button press."""
        # Clear entire expression if in error state
        if self.calculator.is_error_state():
            self.calculator.clear_expression()
        else:
            self.calculator.remove_last_character()
        self._update_display()

    def _on_calculate(self) -> None:
        """Handle equals button press."""
        self.calculator.calculate()
        self._update_display()
