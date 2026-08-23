# CNA-Python desktop starter

This is a small real desktop CNA application. It runs through the installed
`cna-python` package and an external exact CNA C ABI 0.7.0 library. It has no
fake renderer label, 3D branch, `DrawRect`, Web/Pyodide, Briefcase, Android, or
mobile claim.

The measured runtime configuration for this milestone is Linux x86-64 with a
qualified HEADLESS/NULL-audio CNA artifact. A GPU/windowed renderer, Windows,
and macOS have not yet been verified.

Build/install the `cna-python` 0.1.0.dev0 wheel, then set an absolute native
library path:

```bash
python3 -m pip install /path/to/cna_python-0.1.0.dev0-py3-none-any.whl
export CNA_NATIVE_LIBRARY=/absolute/path/to/libcna_c_api.so
python3 main.py
```

Deterministic real-frame modes are:

```bash
python3 main.py --smoke-test       # exactly 60 successful Draw calls
python3 main.py --stability-test   # exactly 600 successful Draw calls
python3 main.py --frames 120
```

The success line is printed only after `Game.Run` returns with exactly the
requested number of CNA-backed `Draw` calls completed. The game decodes the
raw 128×128 `Content/logo.png` with `Texture2D.FromStream`, polls keyboard,
mouse, and gamepad, clears Cornflower Blue, and draws the moving, rotating,
scaling logo with the real SpriteBatch path.
