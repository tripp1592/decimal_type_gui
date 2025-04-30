# src/gui.py

from decimal import Decimal, ROUND_HALF_UP
from PySide6.QtWidgets import QWidget, QGridLayout, QLineEdit, QPushButton
from PySide6.QtCore import Qt
from .core import evaluate


class Calculator(QWidget):
    def __init__(self, cfg):
        super().__init__()
        self.decimal_places = cfg["decimal_places"]
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Decimal Calculator")
        self.display = QLineEdit("0", readOnly=True, alignment=Qt.AlignRight)
        layout = QGridLayout(self)
        layout.addWidget(self.display, 0, 0, 1, 4)

        buttons = [
            ("7", 1, 0),
            ("8", 1, 1),
            ("9", 1, 2),
            ("/", 1, 3),
            ("4", 2, 0),
            ("5", 2, 1),
            ("6", 2, 2),
            ("*", 2, 3),
            ("1", 3, 0),
            ("2", 3, 1),
            ("3", 3, 2),
            ("-", 3, 3),
            ("0", 4, 0),
            (".", 4, 1),
            ("=", 4, 2),
            ("+", 4, 3),
            ("C", 5, 0),
            ("(", 5, 1),
            (")", 5, 2),
            ("^", 5, 3),
        ]

        for text, row, col in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(lambda _, t=text: self.on_button(t))
            layout.addWidget(btn, row, col)

    def on_button(self, char):
        if char == "C":
            self.display.setText("0")
            return

        if char == "=":
            expr = self.display.text().replace("^", "**")
            try:
                result = evaluate(expr)
                quant = Decimal(1).scaleb(-self.decimal_places)
                out = result.quantize(quant, rounding=ROUND_HALF_UP)
                self.display.setText(str(out))
            except Exception:
                self.display.setText("Error")
            return

        cur = self.display.text()
        if cur == "0" and char not in (".", "+", "-", "(", ")"):
            new = char
        else:
            new = cur + char
        self.display.setText(new)

    def keyPressEvent(self, event):
        key_map = {
            Qt.Key_0: "0",
            Qt.Key_1: "1",
            Qt.Key_2: "2",
            Qt.Key_3: "3",
            Qt.Key_4: "4",
            Qt.Key_5: "5",
            Qt.Key_6: "6",
            Qt.Key_7: "7",
            Qt.Key_8: "8",
            Qt.Key_9: "9",
            Qt.Key_Plus: "+",
            Qt.Key_Minus: "-",
            Qt.Key_Asterisk: "*",
            Qt.Key_Slash: "/",
            Qt.Key_Period: ".",
            Qt.Key_ParenLeft: "(",
            Qt.Key_ParenRight: ")",
            Qt.Key_AsciiCircum: "^",
            Qt.Key_Return: "=",
            Qt.Key_Enter: "=",
        }
        char = key_map.get(event.key())
        if char:
            self.on_button(char)
        else:
            super().keyPressEvent(event)
