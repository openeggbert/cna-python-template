# cna-python-template

> **Status: In progress - ZATÍM NEFUNKČNÍ**


A starter project for **[CNA](https://github.com/openeggbert/cna)** — a reimplementation of the XNA 4.0 game framework, using the **Python binding**.

This template provides a standard XNA-like project structure with support for multiple platforms including Desktop, Android, and Web.

## Features

- **XNA 4.0 API**: Familiar `Initialize`, `LoadContent`, `Update`, and `Draw` pattern in PascalCase.
- **Adaptive Rendering**: Automatically switches between a 3D rotating cube and a 2D bouncing logo based on renderer capabilities.
- **Renderer Banner**: Built-in banner showing the active renderer name using an internal bitmap font.
- **Multi-platform**: Designed to run on Windows, Linux, macOS, Android, and Web.
- **Smoke Test**: Support for `--smoke-test` to verify basic execution.

## Quick Start

### Desktop (Linux/Windows/macOS)

Ensure you have `cna-python` installed or in your `PYTHONPATH`.

```bash
python3 main.py
```

### Web

This template is compatible with **PyScript** and **Pyodide**. 

1. Serve the project root with a web server.
2. Access `index.html` (if provided) or use a PyScript wrapper.

### Android

Mobile support is provided via **Briefcase** (BeeWare) or similar tools.

```bash
briefcase dev
```

## Project Structure

- `game/`: Shared game logic.
  - `HelloGame.py`: The main game class with XNA logic.
- `Content/`: Game assets (textures, etc.).
- `main.py`: Entry point for the application.
- `requirements.txt`: Python dependencies.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
