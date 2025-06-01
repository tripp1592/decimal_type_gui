# src/exceptions.py
"""Custom exceptions for the calculator application."""


class CalculatorError(Exception):
    """Base exception for calculator errors."""

    pass


class InvalidExpressionError(CalculatorError):
    """Raised when an expression cannot be evaluated."""

    pass


class DivisionByZeroError(CalculatorError):
    """Raised when division by zero is attempted."""

    pass


class OverflowError(CalculatorError):
    """Raised when a calculation results in overflow."""

    pass
