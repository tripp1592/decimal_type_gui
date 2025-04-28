# main.py

import json
import re
from decimal import Decimal, getcontext
from pathlib import Path

from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QPushButton
from PySide6.QtCore import Qt

# ─── Load settings ─────────────────────────────────────────────────────────────
cfg_path = Path(__file__).parent / "config.json"
if not cfg_path.exists():
    raise FileNotFoundError(f"Missing config.json at {cfg_path}")
with open(cfg_path, "r") as f:
    cfg = json.load(f)

precision = cfg.get("precision", 28)
decimal_places = cfg.get("decimal_places", None)
getcontext().prec = precision


# ─── Evaluation helper ─────────────────────────────────────────────────────────
def evaluate(expr: str):
    def wrap_num(m):
        return f'Decimal("{m.group(0)}")'

    safe = re.sub(r"\d+(\.\d+)?", wrap_num, expr)
    try:
        return eval(safe, {"__builtins__": None}, {"Decimal": Decimal})
    except Exception:
        return None


# ─── Calculator UI ─────────────────────────────────────────────────────────────
class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Decimal Calculator")
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)

        self._raw_value = None
        self._just_evaluated = False

        grid = QGridLayout(self)
        grid.addWidget(self.display, 0, 0, 1, 4)

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
        ]
        for txt, r, c in buttons:
            btn = QPushButton(txt)
            btn.clicked.connect(lambda _, t=txt: self.on_click(t))
            grid.addWidget(btn, r, c)

    def keyPressEvent(self, event):
        text = event.text()
        if self._just_evaluated and text in "0123456789.":
            # start new entry after =
            self.display.clear()
            self._just_evaluated = False

        if text in "0123456789.":
            self.on_click(text)
        elif text in "+-*/":
            self.on_click(text)
        elif text == "=":
            self.on_click("=")
        elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.on_click("=")
        elif event.key() == Qt.Key_Backspace:
            self.on_click("C")
        else:
            super().keyPressEvent(event)

        def on_click(self, ch):
        # 1) Ignore repeated “=” so we don’t lose precision
        if ch == '=' and self._just_evaluated:
            return

        # 2) After “=”, a digit click means start a new number
        if self._just_evaluated and ch in '0123456789.':
            self.display.clear()
            self._just_evaluated = False

        # 3) After “=”, an operator chains using the full-precision raw_value
        if self._just_evaluated and ch in '+-*/':
            base = str(self._raw_value)
            self.display.setText(f"{base} {ch} ")
            self._just_evaluated = False
            return

        # 4) Normal behavior for digits/operators/C/=
        if ch in '0123456789.':
            self.display.setText(self.display.text() + ch)

        elif ch in '+-*/':
            self.display.setText(self.display.text() + f' {ch} ')

        elif ch == 'C':
            self.display.clear()

        elif ch == '=':
            expr = self.display.text()
            result = evaluate(expr)
            if result is None:
                self.display.setText("Error")
            else:
                self._raw_value = result
                if decimal_places is not None:
                    quant = Decimal('1.' + ('0'*decimal_places))
                    disp = result.quantize(quant)
                else:
                    disp = result
                self.display.setText(str(disp))
            self._just_evaluated = True



def main():
    app = QApplication([])
    win = Calculator()
    win.show()
    app.exec()


if __name__ == "__main__":
    main()
