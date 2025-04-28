# main.py

import json
import re
from decimal import Decimal, getcontext
from pathlib import Path

from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# ─── Load settings ─────────────────────────────────────────────────────────────
cfg_path = Path(__file__).parent / "config.json"
if not cfg_path.exists():
    raise FileNotFoundError(f"Missing config.json at {cfg_path}")
with open(cfg_path, "r") as f:
    cfg = json.load(f)

precision = cfg.get("precision", 28)
decimal_places = cfg.get("decimal_places", None)
strip_trailing_zeros = cfg.get("strip_trailing_zeros", False)
use_commas = cfg.get("use_commas", False)
allow_parentheses = cfg.get("allow_parentheses", True)
max_history = cfg.get("max_history", 0)
theme = cfg.get("theme", "light")
font_size = cfg.get("font_size", None)
window_size = cfg.get("window_size", {})

getcontext().prec = precision


# ─── Evaluation helper ─────────────────────────────────────────────────────────
def evaluate(expr: str):
    # 1) optionally block parentheses
    if not allow_parentheses and ("(" in expr or ")" in expr):
        return None

    # 2) wrap numbers as Decimal("…")
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

        # apply initial window size
        w = window_size.get("width")
        h = window_size.get("height")
        if w and h:
            self.resize(w, h)

        # font sizing
        if font_size:
            font = QFont()
            font.setPointSize(font_size)
            self.setFont(font)

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)

        # history buffer
        self.history = []
        self.history_index = 0
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
        txt = event.text()
        # history navigation
        if event.key() == Qt.Key_Up and self.history:
            if self.history_index > 0:
                self.history_index -= 1
            self.display.setText(self.history[self.history_index])
            return
        if event.key() == Qt.Key_Down and self.history:
            if self.history_index < len(self.history) - 1:
                self.history_index += 1
                self.display.setText(self.history[self.history_index])
            else:
                self.history_index = len(self.history)
                self.display.clear()
            return

        # map keys to our buttons
        if txt in "0123456789.+-*/":
            self.on_click(txt)
        elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.on_click("=")
        elif event.key() == Qt.Key_Backspace:
            self.on_click("C")
        else:
            super().keyPressEvent(event)

    def on_click(self, ch):
        # 1) ignore repeated “=”
        if ch == "=" and self._just_evaluated:
            return

        # 2) after “=” start fresh on digit
        if self._just_evaluated and ch in "0123456789.":
            self.display.clear()
            self._just_evaluated = False

        # 3) chain operator after “=”
        if self._just_evaluated and ch in "+-*/":
            base = str(self._raw_value)
            self.display.setText(f"{base} {ch} ")
            self._just_evaluated = False
            return

        # 4) normal entry
        if ch in "0123456789.":
            self.display.setText(self.display.text() + ch)
        elif ch in "+-*/":
            self.display.setText(self.display.text() + f" {ch} ")
        elif ch == "C":
            self.display.clear()
            return
        elif ch == "=":
            expr = self.display.text()
            result = evaluate(expr)
            if result is None:
                self.display.setText("Error")
            else:
                # store full precision
                self._raw_value = result

                # quantize if needed
                disp = result
                if decimal_places is not None:
                    quant = Decimal("1." + ("0" * decimal_places))
                    disp = result.quantize(quant)

                # format with commas or plain
                if use_commas:
                    if decimal_places is not None:
                        disp_str = f"{disp:,.{decimal_places}f}"
                    else:
                        disp_str = f"{disp:,}"
                else:
                    disp_str = str(disp)

                # strip trailing zeros
                if strip_trailing_zeros and "." in disp_str:
                    disp_str = disp_str.rstrip("0").rstrip(".")

                self.display.setText(disp_str)

                # record history
                if max_history > 0:
                    self.history.append(expr)
                    if len(self.history) > max_history:
                        self.history.pop(0)
                    self.history_index = len(self.history)

            self._just_evaluated = True


def main():
    app = QApplication([])

    # apply dark theme if requested
    if theme == "dark":
        app.setStyleSheet(
            """
            QWidget { background: #2b2b2b; color: #ffffff; }
            QPushButton { background: #3c3f41; color: #ffffff; }
            QLineEdit { background: #212325; color: #ffffff; }
        """
        )

    win = Calculator()
    win.show()
    app.exec()


if __name__ == "__main__":
    main()
