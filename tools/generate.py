#!/usr/bin/env python3
"""Generate an isolated ordinary Python consumer from the maintained starter."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]


def identifier(value: str, label: str) -> str:
    if not value.isidentifier():
        raise ValueError(f"{label} must be a Python identifier")
    return value


def distribution(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9]+(?:[-_.][A-Za-z0-9]+)*", value):
        raise ValueError("distribution name is invalid")
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("destination")
    parser.add_argument("--distribution-name", default="my-cna-game")
    parser.add_argument("--module-name", default="my_cna_game")
    parser.add_argument("--game-class", default="MyGame")
    args = parser.parse_args()
    destination = Path(args.destination).resolve()
    if destination.exists() and any(destination.iterdir()):
        raise ValueError("destination must not exist or must be empty")
    destination.mkdir(parents=True, exist_ok=True)
    module_name = identifier(args.module_name, "module name")
    game_class = identifier(args.game_class, "game class")
    distribution_name = distribution(args.distribution_name)
    module = destination / module_name
    module.mkdir()
    source = (ROOT / "game/hello_game.py").read_text()
    source = source.replace("class HelloGame(Game):", f"class {game_class}(Game):")
    source = source.replace('parents[1] / "Content"', 'parents[1] / "Content"')
    (module / "game.py").write_text(source)
    (module / "__init__.py").write_text(f"from .game import {game_class}\n\n__all__ = [\"{game_class}\"]\n")
    main_source = (ROOT / "main.py").read_text().replace("from game import HelloGame", f"from {module_name} import {game_class}")
    main_source = main_source.replace("HelloGame(frames)", f"{game_class}(frames)")
    main_source = main_source.replace("cna-python-template:", f"{distribution_name}:")
    (destination / "main.py").write_text(main_source)
    content = destination / "Content"
    content.mkdir()
    shutil.copyfile(ROOT / "Content/logo.png", content / "logo.png")
    shutil.copyfile(ROOT / "Content/logo.xnb", content / "logo.xnb")
    pyproject = (ROOT / "pyproject.toml").read_text()
    pyproject = pyproject.replace('name = "cna-python-starter"', f'name = "{distribution_name}"')
    pyproject = pyproject.replace('include = ["game*"]', f'include = ["{module_name}*"]')
    (destination / "pyproject.toml").write_text(pyproject)
    (destination / "README.md").write_text(
        f"# {distribution_name}\n\nGenerated desktop CNA-Python consumer.\n"
    )
    print(f"generated {destination}")


if __name__ == "__main__":
    main()
