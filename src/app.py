# src/app.py
"""Application management for the calculator."""

import sys
from typing import Optional

import qdarkstyle  # type: ignore
from PyQt6.QtWidgets import QApplication  # type: ignore

from .config import Config
from .core import DecimalCalculator
from .gui import CalculatorWidget


class CalculatorApp:
    """Main calculator application manager."""

    def __init__(self, config: Config):
        self.config = config
        self.app: Optional[QApplication] = None
        self.calculator: Optional[DecimalCalculator] = None
        self.main_widget: Optional[CalculatorWidget] = None

        self._initialize_application()

    def _initialize_application(self) -> None:
        """Initialize the Qt application and components."""
        self.app = QApplication(sys.argv)
        self._setup_styling()

        # Create calculator and UI
        self.calculator = DecimalCalculator(self.config.decimal_places)
        self.main_widget = CalculatorWidget(self.calculator)

    def _setup_styling(self) -> None:
        """Apply application styling based on configuration."""
        if self.app:
            self.app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())

    def run(self) -> int:
        """Run the application and return exit code."""
        if self.main_widget:
            self.main_widget.show()

        if self.app:
            return self.app.exec()

        return 1

    def quit(self) -> None:
        """Quit the application gracefully."""
        if self.app:
            self.app.quit()
