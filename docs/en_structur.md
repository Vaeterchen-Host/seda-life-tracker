# Project Structure (AI-generated)

> This document describes the current workspace layout of the SEDA project.

## Quick Overview

SEDA is currently a Python project with the following main areas:

- application logic in `model/`
- user interfaces in `ui/`
- data in `data/`
- tests in `tests/`
- documentation in `docs/`

There are also utility files, older experiments, and some legacy code that are not part of the main runtime path.

## Project Folders

### `model/`
This folder contains the core application logic.

Important files:
- `classes.py`: core classes such as `User`, `WaterLog`, `WeightLog`, `Food`, and `Meal`
- `database.py`: SQLite access, table creation, and database methods
- `controller.py`: CLI controller that connects user input, logic, and persistence

### `ui/`
This folder contains everything related to the user interface.

Important files:
- `ui.py`: graphical user interface built with Flet
- `cli_view.py`: command-line input and output helpers
- `tutorial/`: small Flet learning examples

### `data/`
This folder stores persistent project data.

Current content:
- `database.db`: the main SQLite database

### `tests/`
This folder contains automated tests.

Current content:
- `test_classes.py`: tests for classes from `model/classes.py`
- `test_cli_view.py`: tests for CLI view behavior
- `test_database.py`: tests for database behavior
- `test.db`: an additional test database file

### `test_db/`
This folder is intended for isolated test databases.

It is referenced in `tests/test_database.py` and may exist locally or be created during tests, even if it is not permanently present in the repository.

### `docs/`
This folder contains project documentation.

Current content:
- `de_struktur.md`: German structure overview
- `en_structur.md`: English structure overview
- several exported diagrams as `.png`
- `Anforderungsanalyse Tabelle.ods`: supporting analysis document

### `utils/`
This folder currently acts as a utility and staging area.

Examples:
- `tobi_classes.py`
- `bine_cli_main.py`
- `test_bine.py`

### `legacy/`
This folder stores older code that is no longer part of the main path, but is still kept for reference.

Current content:
- `ui_german.py`

## Important Files in the Project Root

### `main.py`
This is the main entry point of the project.

Current behavior:
- asks whether the GUI or CLI should be started
- can also show the license text
- launches the Flet interface for `y`
- launches the CLI controller for `n`

### `config.py`
This file stores central settings and shared paths.

Current content includes:
- `BASE_DIR`
- `DB_PATH`
- `LICENSE_PATH`
- `DB_TEST_PATH`
- `DEVS`
- `VERSION`

### `bug_tracker.py`
This file collects known issues and technical debt.

It is not part of runtime logic, but it is useful for planning and maintenance.

### `requirements.txt`
This file lists the Python dependencies, for example:
- `flet`
- `Flask`
- `pytest`
- several supporting libraries

## What Is Not Core Application Structure

The workspace also contains:

- `venv/`: local virtual environment
- `__pycache__/`: automatically generated Python cache files
- `.git/`: Git metadata
- `.codex/`: local tool or editor file

These are useful for development, but they are not part of the actual application architecture.

## What Does `.gitignore` Do?

The `.gitignore` file tells Git which files or folders should not be tracked.

In this project, that includes for example:
- Python cache files
- virtual environments
- editor files

Important:
`.gitignore` does not delete anything. It only prevents selected files from being added to version control by mistake.

- `utils/` should ideally contain only helper functions, or be split into clearer folders later.
- `legacy/` is useful for old code, but should not be confused with active UI code.
- older UI files in `legacy/` could later be cleaned up further or marked more clearly.