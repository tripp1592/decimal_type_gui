# src/main.py
import json, sys
from decimal import Decimal, getcontext
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QGridLayout
from PyQt6.QtCore import Qt

# ── load config ─────────────────────────────────────────────────────────────
with open("config.json", "r") as f:
    cfg = json.load(f)

getcontext().prec = cfg["precision"]
decimal_places = cfg.get("decimal_places", 2)
theme = cfg.get("theme", "light").lower()

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

# state
expr = ""


def update(txt):
    global expr
    expr = txt
    disp.setText(txt)


# button handler
def make_btn(text, r, c, colspan=1):
    btn = QPushButton(text)
    btn.setFixedSize(60, 40)
    layout.addWidget(btn, r, c, 1, colspan)
    return btn


# digits & ops
buttons = [
    ("7", "8", "9", "/"),
    ("4", "5", "6", "*"),
    ("1", "2", "3", "-"),
]
for i, row in enumerate(buttons, start=1):
    for j, ch in enumerate(row):
        btn = make_btn(ch, i, j)
        btn.clicked.connect(lambda _, s=ch: update(expr + s))

# bottom row
make_btn("0", 4, 0, colspan=2).clicked.connect(lambda _: update(expr + "0"))
make_btn(".", 4, 2).clicked.connect(lambda _: update(expr + "."))
make_btn("=", 4, 3).clicked.connect(lambda _: calculate())
make_btn("+", 5, 3).clicked.connect(lambda _: update(expr + "+"))
make_btn("C", 5, 0, colspan=2).clicked.connect(lambda _: update(""))
make_btn("⌫", 5, 2).clicked.connect(lambda _: update(expr[:-1]))


# calculation logic
def calculate():
    try:
        # safe eval: only Decimal in locals
        result = eval(expr, {"__builtins__": None}, {"Decimal": Decimal})
        formatted = f"{Decimal(result):.{decimal_places}f}"
    except Exception:
        formatted = "ERROR"
    update(formatted)


# keybindings
win.keyPressEvent = lambda e: {
    Qt.Key_Return: (calculate,),
    Qt.Key_Backspace: (lambda: update(expr[:-1]),),
}.get(e.key(), (lambda: None))[0]()

# ── run ────────────────────────────────────────────────────────────────────────
win.show()
sys.exit(app.exec())
