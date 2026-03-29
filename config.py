"""This is the config file of the project."""

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

# -----------------------------
# This content ist not AI-generated.
DB_TEST_PATH = BASE_DIR / "tests" / "test.db"

# devs:
DEVS = "Sabine Steverding & Tobias Mignat"
VERSION = "0.1.0"

if __name__ == "__main__":
    print(f"Database path is set to: {DB_PATH}")
    print(f"Base directory is: {BASE_DIR}")
    print(f"test.db is in: {DB_TEST_PATH}")
