# Project Structure (AI-generated)

> AI-updated for the current V0.5 project status.

> This document describes the current workspace layout of the SEDA project.

## Quick Overview

SEDA is currently a Python project with the following active main areas:

- application logic in `model/`
- user interfaces in `ui/`
- data in `data/`
- tests in `tests/`
- documentation in `docs/`

There are also utility files, older experiments, release subfolders, and some legacy code that are not part of the main runtime path.

## Project Folders

### `model/`
This folder contains the core application logic.

Important files:
- `class_user.py`: central `User` class with age, water, BMI, and calorie-related calculations
- `classes_log.py`: log classes and handlers for water, weight, meals, and activities
- `classes_food.py`: domain classes for `Food`, `Meal`, `BigSeven`, and `NutrientSummary`
- `database.py`: SQLite access, table creation, and database methods for users, water logs, weight logs, activity logs, food logs, meals, and meal items
- `controller.py`: CLI controller that connects user input, logic, the external food DB, and persistence
- `open_food_api.py`: experimental API access for Open Food Facts lookups by barcode or product name, currently not the main search path

### `ui/`
This folder contains everything related to the user interface.

Important files:
- `gui.py`: graphical user interface built with Flet
- `gui copy.py`: older or parallel GUI working copy
- `cli_view.py`: command-line input and output helpers
- `translations.py`: GUI translations for German and English

### `data/`
This folder stores persistent project data.

Current content:
- `database.db`: the main SQLite database
- `bls_foods.sqlite`: a separate food database used by `model/database.py` through `FoodDatabase`

### `tests/`
This folder contains automated tests.

Current content:
- `test_user_class.py`: tests for the `User` class
- `test_log_classes.py`: tests for log classes and handlers
- `test_food_classes.py`: tests for `Food`, `Meal`, and nutrient-related behavior
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
- `gui_backlog.md`: GUI, UX, and product-facing follow-up backlog
- `design_system.md`: lightweight GUI style and layout conventions
- `v0.1/`: older exported diagrams from an earlier project phase
- `v0.5/`: release folder reserved for the current version
- several exported diagrams as `.png`
- `Anforderungsanalyse Tabelle.ods`: supporting analysis document

### `utils/`
This folder currently acts as a utility and staging area.

Examples:
- `paginator.py`: helper for paginated CLI output, currently used for long license text
- `test_bine.py`: additional development-side database tests
- the folder currently contains mostly helper and experiment material, no central runtime module anymore

This folder currently mixes helpers, prototypes, and development leftovers.

### `legacy/`
This folder stores older code that is no longer part of the main path, but is still kept for reference.

Current content:
- `bine_cli_main.py`
- `cli_controller.py`
- `theme_utils.py`
- `tobi_classes.py`
- `ui_german.py`
- `ui_discardable.py`
- `ui_v0.1.py`

### `BLS_4_0_2025_DE/`
This folder contains source material related to the external BLS food database.

Current content:
- Excel files and PDF documentation for the BLS source data
- `bls_foods.sqlite`: another SQLite version of the food dataset
- `import_bls_to_sqlite.py`: import helper for that dataset

This folder appears to be data and import working material, not part of the normal application runtime path.

### `Beispiele/`
This folder contains learning, tutorial, and experiment files.

Current content:
- several small Python examples
- `flet_tutorial/` with multiple Flet learning scripts

This folder is not part of the actual application runtime path, but it makes sense in the repository context of a student project.

## Important Files in the Project Root

### `main.py`
This is the main entry point of the project.

Current behavior:
- asks whether the GUI or CLI should be started
- can also show the license text
- launches the Flet interface for `g`
- launches the CLI controller for `c`
- uses `ui.cli_view.show_welcome()` for the startup message
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

Note:
- `VERSION` is still set to `0.1.0` in code, even though the current release context you requested is V0.5.

### `data/bls_foods.sqlite`
This database contains a large static food collection.

Important:
- it serves as a lookup database for food data
- it should only be used read-only
- changing this file is not part of the normal project workflow

### `bug_tracker.py`
This file collects known issues and technical debt.

It is not part of runtime logic, but it is useful for planning and maintenance.
GUI and UX planning now live separately in `docs/gui_backlog.md`.

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
- food, meal, and activity tracking are now visibly part of the active runtime path, not only preparation work.
