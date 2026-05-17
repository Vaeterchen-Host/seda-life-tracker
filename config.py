# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Project configuration for SEDA."""

# By using this configfile, we can easily change the database path.
# Other wise we need to write the path in everyfile where we need it.
# Example: DB_PATH = "data/database.db"

import json
from pathlib import Path  # For handling file paths in a platform-independent way.

# Get the directory of the current file (config.py) and resolve it to an absolute path.
# This will be used as the base directory for other paths in the project.
BASE_DIR = Path(__file__).resolve().parent

# Path(something) == create a path object with the given string as path
# __file__ == current file path
# resolve() == get absolute path
# parent == get the directory of the file /.../OOP-Praktikum/config.py -> /.../OOP-Praktikum

# This is where the SQLite database will be stored.
DB_PATH = BASE_DIR / "data" / "database.db"
FOOD_DB_PATH = BASE_DIR / "data" / "bls_foods.sqlite"
LICENSE_PATH = BASE_DIR / "LICENSE.md"
ASSETS_DIR = BASE_DIR / "assets"
GUI_SETTINGS_PATH = BASE_DIR / "data" / "gui_settings.json"

DEFAULT_GUI_SETTINGS = {
    "user_id": None,
    "language": "de",
    "dark_mode": False,
    "energy_unit": "kcal",
}

_UNSET = object()


def _write_gui_settings_file(settings, settings_path=GUI_SETTINGS_PATH):
    """Persist normalized GUI settings to disk. AI-generated."""
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(
        json.dumps(settings, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _normalize_gui_settings(raw_settings):
    """Return safe GUI settings with defaults for invalid values. AI-generated."""
    if not isinstance(raw_settings, dict):
        return DEFAULT_GUI_SETTINGS.copy(), False

    settings = DEFAULT_GUI_SETTINGS.copy()
    is_valid = True

    user_id = raw_settings.get("user_id")
    if user_id is None or isinstance(user_id, int):
        settings["user_id"] = user_id
    else:
        is_valid = False

    language = raw_settings.get("language")
    if language in {"de", "en"}:
        settings["language"] = language
    else:
        is_valid = False

    dark_mode = raw_settings.get("dark_mode")
    if isinstance(dark_mode, bool):
        settings["dark_mode"] = dark_mode
    else:
        is_valid = False

    energy_unit = raw_settings.get("energy_unit")
    if energy_unit in {"kcal", "kj"}:
        settings["energy_unit"] = energy_unit
    else:
        is_valid = False

    return settings, is_valid


def get_gui_settings(settings_path=GUI_SETTINGS_PATH):
    """Load GUI settings from disk and fall back to defaults safely. AI-generated."""
    try:
        raw_settings = json.loads(settings_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        settings = DEFAULT_GUI_SETTINGS.copy()
        _write_gui_settings_file(settings, settings_path)
        return settings

    settings, is_valid = _normalize_gui_settings(raw_settings)
    if not is_valid:
        _write_gui_settings_file(settings, settings_path)
    return settings


def update_gui_settings(
    user_id=_UNSET,
    language=_UNSET,
    dark_mode=_UNSET,
    energy_unit=_UNSET,
    settings_path=GUI_SETTINGS_PATH,
):
    """Update selected GUI settings and persist the merged result. AI-generated."""
    settings = get_gui_settings(settings_path)
    if user_id is not _UNSET:
        settings["user_id"] = user_id
    if language is not _UNSET:
        settings["language"] = language
    if dark_mode is not _UNSET:
        settings["dark_mode"] = dark_mode
    if energy_unit is not _UNSET:
        settings["energy_unit"] = energy_unit

    settings, _ = _normalize_gui_settings(settings)
    _write_gui_settings_file(settings, settings_path)
    return settings

# -----------------------------
# This content ist not AI-generated.
DB_TEST_PATH = BASE_DIR / "tests" / "test.db"

# devs:
DEVS = "Sabine Steverding & Tobias Mignat"
VERSION = "1.0.0"

if __name__ == "__main__":
    print(f"Database path is set to: {DB_PATH}")
    print(f"Base directory is: {BASE_DIR}")
    print(f"test.db is in: {DB_TEST_PATH}")
    print(f"License file is in: {LICENSE_PATH}")
    print(f"Food database is in: {FOOD_DB_PATH}")
    print(f"Assets directory is: {ASSETS_DIR}")
    print(f"GUI settings are in: {GUI_SETTINGS_PATH}")
