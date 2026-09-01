# CNA-Python desktop starter

This is a small real desktop CNA application. It runs through the installed
`cna-python` package and an external CNA `0.21.x` C ABI library. It has no fake
renderer label, 3D branch, `DrawRect`, Web/Pyodide, Briefcase, Android, or
mobile claim.

It is qualified on Linux x86-64 against two CNA artifacts: a non-windowed
control that does not rasterize, and an OPENGLES3 renderer that does. Both run
60 and 600 real frames from the installed wheel. Windows and macOS have not been
verified.

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
raw 128×128 `Content/logo.png` with `Texture2D.FromStream` and loads a tiny
legal synthetic `Content/logo.xnb` through `ContentManager.Load` and the XNB
Texture2D reader. It polls keyboard, mouse, and gamepad, clears Cornflower Blue,
and draws both textures with the real SpriteBatch path.

`--verify-frame` additionally reads the back buffer after the last frame and
checks that something was actually drawn over the clear colour. A backend with
no pixel storage refuses that read, and the check reports it as unavailable
rather than passing: on such a backend the frame count is the claim, and it does
not mean pixels.
