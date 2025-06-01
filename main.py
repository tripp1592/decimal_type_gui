"""
Decimal Calculator - Entry Point
A PyQt6-based calculator using Python's Decimal type for precise arithmetic.
"""

import sys

from src import CalculatorApp, Config


def main():
    """Main entry point for the decimal calculator application."""
    # Load configuration
    config = Config()

    # Create and run the application
    app = CalculatorApp(config)
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
