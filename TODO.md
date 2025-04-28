# To-Do

- [ ] Define and document the MVP feature set (e.g. scientific functions, memory buttons)
- [ ] Write unit tests for `evaluate()` (cover basic ops, edge cases, invalid input)
- [ ] Refactor UI code into modules (`config.py`, `core.py`, `ui.py`) for maintainability
- [ ] Add in-app settings dialog to edit `config.json` without restarting
- [ ] Implement memory buttons (MC, MR, M+, M–) and wire up associated Decimal storage
- [ ] Package as a standalone executable with UV + PyInstaller or Nuitka
- [ ] Enhance error handling: show user-friendly messages for malformed expressions
- [ ] Add logging of all calculations (timestamp, input, result) to a file via config
- [ ] Improve UI: add a toggle button for light/dark theme at runtime
- [ ] Support scientific notation (e.g. `1e3`, `2.5E-4`) in `evaluate()`
- [ ] Integrate clipboard support (Ctrl+C/V) for copy/paste of expressions and results
- [ ] Update README with screenshots, usage examples, and contribution guidelines
