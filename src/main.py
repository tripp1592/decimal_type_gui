# src/main.py
import json
import re
import sys
from decimal import Decimal, getcontext
import qdarkstyle
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLineEdit,
    QPushButton,
    QGridLayout,
    QSizePolicy,
)
from PyQt6.QtCore import Qt

# ── Load config.json ───────────────────────────────────────────────────────
with open("config.json", "r") as f:
    cfg = json.load(f)

getcontext().prec = cfg["precision"]
decimal_places = cfg.get("decimal_places", 2)
theme = cfg.get("theme", "light").lower()

# ── Helper: wrap all numeric literals in Decimal('…') ───────────────────────
_decimal_pattern = re.compile(r"(\d+(\.\d+)?)")


def to_decimal_expr(txt: str) -> str:
    return _decimal_pattern.sub(lambda m: f"Decimal('{m.group(1)}')", txt)


# ── Create QApplication & apply QDarkStyle if dark theme ──────────────────
app = QApplication([])
if theme == "dark":
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())

# ── Main window & grid layout ──────────────────────────────────────────────
win = QWidget()
win.setWindowTitle("Decimal Calculator")
layout = QGridLayout(win)
layout.setContentsMargins(12, 12, 12, 12)
layout.setSpacing(8)

# ── Display widget ─────────────────────────────────────────────────────────
disp = QLineEdit()
disp.setReadOnly(True)
disp.setAlignment(Qt.AlignmentFlag.AlignRight)
disp.setFixedHeight(40)
layout.addWidget(disp, 0, 0, 1, 4)

# ── Expression state ───────────────────────────────────────────────────────
expr = ""


def update_display(txt: str):
    global expr
    expr = txt
    disp.setText(txt)


def clear_display():
    update_display("")


def calculate():
    global expr
    try:
        wrapped = to_decimal_expr(expr)
        result = eval(wrapped, {"__builtins__": None}, {"Decimal": Decimal})
        expr = f"{Decimal(result):.{decimal_places}f}"
    except Exception:
        expr = "ERROR"
    disp.setText(expr)


def make_button(text: str, row: int, col: int, colspan: int = 1, handler=None):
    btn = QPushButton(text)
    btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    layout.addWidget(btn, row, col, 1, colspan)
    if handler:
        btn.clicked.connect(handler)
    return btn


# ── Digit & operator buttons ───────────────────────────────────────────────
rows = [
    ("7", "8", "9", "/"),
    ("4", "5", "6", "*"),
    ("1", "2", "3", "-"),
]
for r, row in enumerate(rows, start=1):
    for c, ch in enumerate(row):
        make_button(ch, r, c, handler=lambda *args, s=ch: update_display(expr + s))

# ── Bottom row ─────────────────────────────────────────────────────────────
make_button("0", 4, 0, colspan=2, handler=lambda *args: update_display(expr + "0"))
make_button(".", 4, 2, handler=lambda *args: update_display(expr + "."))
make_button("=", 4, 3, handler=lambda *args: calculate())
make_button("+", 5, 3, handler=lambda *args: update_display(expr + "+"))
make_button("C", 5, 0, colspan=2, handler=lambda *args: clear_display())
make_button("⌫", 5, 2, handler=lambda *args: update_display(expr[:-1]))


# ── Keyboard bindings ──────────────────────────────────────────────────────
def keyPressEvent(e):
    k = e.key()
    if k == Qt.Key.Key_Return:
        calculate()
    elif k == Qt.Key.Key_Backspace:
        update_display(expr[:-1])
    else:
        txt = e.text()
        if txt in "0123456789.+-*/":
            update_display(expr + txt)


win.keyPressEvent = keyPressEvent

# ── Run the app ─────────────────────────────────────────────────────────────
win.show()
sys.exit(app.exec())
