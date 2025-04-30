# src/core.py

import ast
import operator
from decimal import Decimal

# Map AST operator nodes to actual functions
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def evaluate(expression: str) -> Decimal:
    """
    Safely evaluate a mathematical expression using Decimal arithmetic.
    Supported: +, -, *, /, **, unary +/-, and parentheses.
    """
    try:
        node = ast.parse(expression, mode="eval")
        return _eval(node.body)
    except Exception as e:
        raise ValueError(f"Error evaluating '{expression}': {e}")


def _eval(node):
    # Expression wrapper
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numeric literal
    if isinstance(node, ast.Num):  # <py3.8
        return Decimal(str(node.n))
    if hasattr(ast, "Constant") and isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float, str)):
            return Decimal(str(node.value))

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        fn = _OPERATORS.get(type(node.op))
        if fn:
            return fn(left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        val = _eval(node.operand)
        fn = _OPERATORS.get(type(node.op))
        if fn:
            return fn(val)

    # Disallow everything else
    raise ValueError(f"Unsupported expression: {ast.dump(node)}")
