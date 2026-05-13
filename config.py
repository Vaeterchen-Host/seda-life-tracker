# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Project configuration for SEDA."""

# By using this configfile, we can easily change the database path.
# Other wise we need to write the path in everyfile where we need it.
# Example: DB_PATH = "data/database.db"

# AI-Generated content.
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
