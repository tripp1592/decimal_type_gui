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
from PyQt6.QtGui import QFont

# ── Load config.json ───────────────────────────────────────────────────────
with open("config.json", "r") as f:
    cfg = json.load(f)

getcontext().prec = cfg["precision"]
decimal_places = cfg.get("decimal_places", 2)

# ── Wrap literals into Decimal(…) ──────────────────────────────────────────
_decimal_pattern = re.compile(r"(\d+(\.\d+)?)")


def to_decimal_expr(txt: str) -> str:
    return _decimal_pattern.sub(lambda m: f"Decimal('{m.group(1)}')", txt)


# ── Create app + apply dark style ──────────────────────────────────────────
app = QApplication([])
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())

# ── Build main window & layout ─────────────────────────────────────────────
win = QWidget()
win.setWindowTitle("Decimal Calculator")
win.resize(400, 550)  # a reasonable starting size
layout = QGridLayout(win)
layout.setContentsMargins(8, 8, 8, 8)
layout.setSpacing(6)

# ── Display ────────────────────────────────────────────────────────────────
disp = QLineEdit()
disp.setReadOnly(True)
disp.setAlignment(Qt.AlignmentFlag.AlignRight)
disp.setFixedHeight(50)
disp.setFont(QFont("Consolas", 20))  # bigger display font
layout.addWidget(disp, 0, 0, 1, 4)

# ── State & routines ───────────────────────────────────────────────────────
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


# ── Button factory ─────────────────────────────────────────────────────────
btn_font = QFont("Consolas", 16)  # bigger button font


def make_button(text, r, c, colspan=1, handler=None):
    btn = QPushButton(text)
    btn.setFont(btn_font)
    btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    layout.addWidget(btn, r, c, 1, colspan)
    if handler:
        btn.clicked.connect(handler)
    return btn


# ── Digit & operator rows ─────────────────────────────────────────────────
rows = [
    ("7", "8", "9", "/"),
    ("4", "5", "6", "*"),
    ("1", "2", "3", "-"),
]
for i, row in enumerate(rows, start=1):
    for j, ch in enumerate(row):
        make_button(ch, i, j, handler=lambda _, s=ch: update_display(expr + s))

# ── Bottom two rows (0, ., +) and (C, ⌫, =) ───────────────────────────────
make_button("0", 4, 0, colspan=2, handler=lambda *_: update_display(expr + "0"))
make_button(".", 4, 2, handler=lambda *_: update_display(expr + "."))
make_button("+", 4, 3, handler=lambda *_: update_display(expr + "+"))

make_button("C", 5, 0, colspan=2, handler=lambda *_: clear_display())
make_button("⌫", 5, 2, handler=lambda *_: update_display(expr[:-1]))
make_button("=", 5, 3, handler=lambda *_: calculate())


# ── Keyboard support ──────────────────────────────────────────────────────
def keyPressEvent(e):
    k = e.key()
    if k == Qt.Key.Key_Return:
        calculate()
    elif k == Qt.Key.Key_Backspace:
        update_display(expr[:-1])
    else:
        t = e.text()
        if t in "0123456789.+-*/":
            update_display(expr + t)


win.keyPressEvent = keyPressEvent

# ── Launch ─────────────────────────────────────────────────────────────────
win.show()
sys.exit(app.exec())
