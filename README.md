# Decimal Calculator

A precision-first desktop calculator built with PySide6 and Python’s `decimal` module. All arithmetic uses `Decimal` for maximum accuracy, while results are displayed with configurable rounding and formatting via **`config.json`**.

## Features

- **Full-precision arithmetic** (configurable `precision`)  
- **Display rounding** (`decimal_places`) with optional trailing-zero stripping  
- **Thousands-separator formatting** (`use_commas`)  
- **Parentheses support** (toggleable via `allow_parentheses`)  
- **Calculation history** (navigate with ↑/↓ keys, up to `max_history` entries)  
- **Light & dark themes** (`theme`)  
- **Adjustable font size** (`font_size`) and **window dimensions** (`window_size`) 

## Requirements

- Python 3.x  
- [PySide6](https://pypi.org/project/PySide6/)  
- [UV package manager](https://astral.sh/blog/uv) (for venv & dependency management) 

## Installation

In PowerShell:

```powershell
# create & activate a .venv via UV
uv venv

# install Qt bindings
uv add PySide6
```

## Running

```powershell
uv run main.py
```

The calculator window will launch immediately.

## Configuration

Edit **`config.json`** in your project root to tweak behavior:

```json
{
  "precision": 28,
  "decimal_places": 2,
  "strip_trailing_zeros": true,
  "use_commas": true,
  "allow_parentheses": true,
  "max_history": 50,
  "theme": "light",
  "font_size": 14,
  "window_size": {
    "width": 400,
    "height": 300
  }
}
```

- **`precision`**: total significant digits for all operations  
- **`decimal_places`**: digits after the decimal point in the display  
- **`strip_trailing_zeros`**: remove unnecessary `0`’s (e.g. `2.00` → `2`)  
- **`use_commas`**: format results with thousands separators (e.g. `1,234.56`)  
- **`allow_parentheses`**: enable or disable `(`…`)` in expressions  
- **`max_history`**: number of past expressions to remember (↑/↓ navigation)  
- **`theme`**: `"light"` or `"dark"` UI color scheme  
- **`font_size`**: global font size for widgets  
- **`window_size`**: initial window `width` and `height` in pixels 

## Logging

All code changes are appended to **`changes.log`** with ISO-format timestamps.

## Contributing

Feel free to open issues or submit pull requests to add features or fix bugs. 