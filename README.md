# Decimal Calculator GUI

A cross-platform Python GUI calculator using the `decimal` module for precise arithmetic.  
Configurable precision, formatting, and light/dark theme via `config.json`.

## Project structure

```
.
├── .gitignore
├── .venv/              # Virtual environment
├── config.json         # User settings (precision, decimal_places, theme)
├── README.md
├── TODO.md
└── src/                # Source package
    ├── __init__.py
    ├── config.py
    ├── core.py
    ├── gui.py
    └── main.py
```

## Requirements

- Python 3.8+  
- [PySide6](https://pypi.org/project/PySide6/)  
- (Optional) [UV](https://github.com/jazzband/poetry) for environment & task management  

## Installation

```bash
# create & activate venv
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# install deps
pip install PySide6
```

## Configuration

Populate or adjust `config.json` at the project root. Example:

```json
{
  "precision": 28,
  "decimal_places": 2,
  "theme": "light"
}
```

- **precision**: total significant digits for all calculations  
- **decimal_places**: digits shown after the decimal point  
- **theme**: `"light"` or `"dark"`

## Running

- **With UV**  
  ```bash
  uv run --module src.main
  ```

- **Directly**  
  ```bash
  python -m src.main
  ```

## Features

- Decimal-based arithmetic for full precision  
- Operations: `+`, `-`, `*`, `/`, `^` (exponent), parentheses  
- Configurable precision & display format  
- Light/dark theming  
- Both button clicks and keyboard input  

## Testing

Add tests under a `tests/` folder and run with `pytest`.

## Packaging

Once you’ve refactored and tested, you can bundle into a single executable. For example with PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile -n DecimalCalc src/main.py
```
```

---

With these in place you’ll have a clean, well-structured codebase and up-to-date docs. Let me know if you’d like to add unit tests or CI next!