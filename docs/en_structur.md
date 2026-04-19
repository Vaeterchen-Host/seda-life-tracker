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
- `classes.py`: core domain classes such as `User`, `WaterLog`, `WeightLog`, `Food`, `Meal`, `MealItem`, and nutrient helper objects
- `database.py`: SQLite access, table creation, and database methods for users, water logs, weight logs, activity logs, food logs, meals, and meal items
- `controller.py`: CLI controller that connects user input, logic, and persistence
- `open_food_api.py`: experimental API access for Open Food Facts lookups by barcode or product name

### `ui/`
This folder contains everything related to the user interface.

Important files:
- `ui.py`: graphical user interface built with Flet
- `cli_view.py`: command-line input and output helpers
- `theme_utils.py`: small helper functions for switching the Flet theme

### `data/`
This folder stores persistent project data.

Current content:
- `database.db`: the main SQLite database
- `bls_foods.sqlite`: a separate food database used by `model/database.py` through `FoodDatabase`

### `tests/`
This folder contains automated tests.

Current content:
- `test_classes.py`: tests for classes from `model/classes.py`
- `test_cli_view.py`: tests for CLI view behavior
- `test_database.py`: tests for database behavior
- `test.db`: an additional test database file

### `test_db/`
This path is intended for isolated temporary test databases.

It is referenced in `tests/test_database.py` and `utils/test_bine.py`, but it is not a regular tracked project folder at the moment.
The tests create temporary `.db` files there when needed.

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
- `paginator.py`: helper for paginated CLI output, currently used for long license text
- `tobi_classes.py`: older or parallel class implementation used during development
- `bine_cli_main.py`: alternative CLI controller prototype
- `test_bine.py`: additional development-side database tests
- `tobi_cli_controller`: executable Python script without `.py` suffix, apparently kept as another experimental controller variant

This folder currently mixes helpers, prototypes, and development leftovers.

### `legacy/`
This folder stores older code that is no longer part of the main path, but is still kept for reference.

Current content:
- `ui_german.py`
- `ui_discardable.py`

## Important Files in the Project Root

### `main.py`
This is the main entry point of the project.

Current behavior:
- asks whether the GUI or CLI should be started
- can also show the license text
- launches the Flet interface for `g`
- launches the CLI controller for `c`
- still contains an outdated error message that mentions `y/n/l`, even though the actual prompt uses `g/c/l`

### `config.py`
This file stores central settings and shared paths.

Current content includes:
- `BASE_DIR`
- `DB_PATH`
- `FOOD_DB_PATH`
- `LICENSE_PATH`
- `DB_TEST_PATH`
- `DEVS`
- `VERSION`

### `data/bls_foods.sqlite`
This database contains a large static food collection.

Important:
- it serves as a lookup database for food data
- it should only be used read-only
- changing this file is not part of the normal project workflow

### `bug_tracker.py`
This file collects known issues and technical debt.

It is not part of runtime logic, but it is useful for planning and maintenance.

### `requirements.txt`
This file lists the Python dependencies, for example:
- `flet`
- `Flask`
- `pytest`
- several supporting libraries

### `LICENSE.md`
This file contains the full GPL license text shown by the CLI and referenced in the GUI.

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
- parts of the codebase already prepare food and meal tracking, but the currently visible runtime focus is still mainly user, water, and weight tracking.
