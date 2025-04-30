# src/main.py
import json
import re
import sys
from decimal import Decimal, getcontext
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QGridLayout
from PyQt6.QtCore import Qt

# ── load config ─────────────────────────────────────────────────────────────
with open("config.json", "r") as f:
    cfg = json.load(f)

getcontext().prec = cfg["precision"]
decimal_places = cfg.get("decimal_places", 2)
theme = cfg.get("theme", "light").lower()

# ── helper: wrap all numeric literals in Decimal('…') ─────────────────────────
_decimal_pattern = re.compile(r"(\d+(\.\d+)?)")


def to_decimal_expr(txt: str) -> str:
    # e.g. "1+2.5" → "Decimal('1')+Decimal('2.5')"
    return _decimal_pattern.sub(lambda m: f"Decimal('{m.group(1)}')", txt)


# ── app + optional dark theme ───────────────────────────────────────────────
app = QApplication([])

if theme == "dark":
    palette = app.palette()
    palette.setColor(palette.ColorRole.Window, Qt.GlobalColor.black)
    palette.setColor(palette.ColorRole.WindowText, Qt.GlobalColor.white)
    app.setPalette(palette)

# ── main window & layout ────────────────────────────────────────────────────
win = QWidget()
win.setWindowTitle("Decimal Calculator")
layout = QGridLayout(win)

# display
disp = QLineEdit()
disp.setReadOnly(True)
disp.setAlignment(Qt.AlignmentFlag.AlignRight)
disp.setFixedHeight(40)
layout.addWidget(disp, 0, 0, 1, 4)

expr = ""  # holds the raw user input


def update(txt: str):
    global expr
    expr = txt
    disp.setText(txt)


# calculation logic using wrapped Decimal literals
def calculate():
    global expr
    try:
        wrapped = to_decimal_expr(expr)
        # evaluate with Decimal only
        result = eval(wrapped, {"__builtins__": None}, {"Decimal": Decimal})
        expr = f"{Decimal(result):.{decimal_places}f}"
    except Exception:
        expr = "ERROR"
    disp.setText(expr)


# button factory
def make_btn(text: str, r: int, c: int, colspan: int = 1):
    btn = QPushButton(text)
    btn.setFixedSize(60, 40)
    layout.addWidget(btn, r, c, 1, colspan)
    return btn


# digits & ops rows
buttons = [
    ("7", "8", "9", "/"),
    ("4", "5", "6", "*"),
    ("1", "2", "3", "-"),
]
for i, row in enumerate(buttons, start=1):
    for j, ch in enumerate(row):
        make_btn(ch, i, j).clicked.connect(lambda _, s=ch: update(expr + s))

# bottom row
make_btn("0", 4, 0, colspan=2).clicked.connect(lambda _: update(expr + "0"))
make_btn(".", 4, 2).clicked.connect(lambda _: update(expr + "."))
make_btn("=", 4, 3).clicked.connect(lambda _: calculate())
make_btn("+", 5, 3).clicked.connect(lambda _: update(expr + "+"))
make_btn("C", 5, 0, colspan=2).clicked.connect(lambda _: update(""))
make_btn("⌫", 5, 2).clicked.connect(lambda _: update(expr[:-1]))


# keybindings
def keypress(e):
    k = e.key()
    if k == Qt.Key.Key_Return:
        calculate()
    elif k == Qt.Key.Key_Backspace:
        update(expr[:-1])
    else:
        text = e.text()
        if text in "0123456789.+-*/":
            update(expr + text)


win.keyPressEvent = keypress

# ── run ────────────────────────────────────────────────────────────────────────
win.show()
sys.exit(app.exec())
