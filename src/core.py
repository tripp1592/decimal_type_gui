# src/core.py
import re
from decimal import Decimal, InvalidOperation
from typing import Union

from .constants import ERROR_MESSAGES, VALID_INPUT_CHARS
from .exceptions import DivisionByZeroError, InvalidExpressionError, OverflowError


class DecimalCalculator:
    """Core calculator logic using Decimal arithmetic."""

    def __init__(self, decimal_places: int = 2):
        self.decimal_places = decimal_places
        self._decimal_pattern = re.compile(r"(\d+(\.\d+)?)")
        self.reset()

    def reset(self) -> None:
        """Reset calculator state."""
        self._expression = ""

    @property
    def expression(self) -> str:
        """Get current expression."""
        return self._expression

    def append_to_expression(self, text: str) -> None:
        """Add text to current expression."""
        if self.is_valid_input(text):
            self._expression += text

    def remove_last_character(self) -> None:
        """Remove last character from expression."""
        self._expression = self._expression[:-1]

    def clear_expression(self) -> None:
        """Clear the current expression."""
        self._expression = ""

    def _to_decimal_expr(self, txt: str) -> str:
        """Wrap numeric literals in Decimal() calls."""
        return self._decimal_pattern.sub(lambda m: f"Decimal('{m.group(1)}')", txt)

    def _validate_expression(self, expression: str) -> None:
        """Validate expression before evaluation."""
        if not expression.strip():
            raise InvalidExpressionError("Empty expression")

        # Check for division by zero patterns
        if "/0" in expression or "/ 0" in expression:
            raise DivisionByZeroError("Division by zero detected")

        # Check for invalid character sequences
        invalid_patterns = ["++", "--", "**", "//", "..", "+-", "-+", "*+", "/+"]
        for pattern in invalid_patterns:
            if pattern in expression:
                raise InvalidExpressionError(f"Invalid pattern: {pattern}")

    def calculate(self) -> str:
        """
        Evaluate the current expression and return result.
        Returns appropriate error message if evaluation fails.
        """
        if not self._expression:
            return ""

        try:
            self._validate_expression(self._expression)
            wrapped = self._to_decimal_expr(self._expression)

            # Safe evaluation with restricted builtins
            allowed_names = {"Decimal": Decimal}
            result = eval(wrapped, {"__builtins__": {}}, allowed_names)

            if not isinstance(result, Decimal):
                result = Decimal(str(result))

            # Check for overflow or very large numbers
            if abs(result) > Decimal("1e100"):
                raise OverflowError("Result too large")

            formatted_result = f"{result:.{self.decimal_places}f}"
            self._expression = formatted_result
            return formatted_result

        except ZeroDivisionError:
            self._expression = ERROR_MESSAGES["DIVISION_BY_ZERO"]
            return ERROR_MESSAGES["DIVISION_BY_ZERO"]
        except (DivisionByZeroError,):
            self._expression = ERROR_MESSAGES["DIVISION_BY_ZERO"]
            return ERROR_MESSAGES["DIVISION_BY_ZERO"]
        except (InvalidOperation, InvalidExpressionError):
            self._expression = ERROR_MESSAGES["INVALID_EXPRESSION"]
            return ERROR_MESSAGES["INVALID_EXPRESSION"]
        except (OverflowError,):
            self._expression = ERROR_MESSAGES["OVERFLOW"]
            return ERROR_MESSAGES["OVERFLOW"]
        except Exception:
            self._expression = ERROR_MESSAGES["GENERAL_ERROR"]
            return ERROR_MESSAGES["GENERAL_ERROR"]

    def is_valid_input(self, char: str) -> bool:
        """Check if character is valid calculator input."""
        return char in VALID_INPUT_CHARS

    def is_error_state(self) -> bool:
        """Check if calculator is in an error state."""
        return self._expression in ERROR_MESSAGES.values()
