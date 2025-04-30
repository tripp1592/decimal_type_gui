# main.py (in src/)
import json
from pathlib import Path
from decimal import getcontext
from PySide6.QtWidgets import QApplication

from .config import cfg
from .gui    import Calculator

def main():
    getcontext().prec = cfg["precision"]
    app = QApplication([])
    if cfg["theme"] == "dark":
        # TODO: supply actual dark‑theme stylesheet
        app.setStyleSheet("")
    win = Calculator()
    win.show()
    app.exec()

if __name__ == "__main__":
    main()
