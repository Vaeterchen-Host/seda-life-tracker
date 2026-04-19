# Project Structure

> This file describes the repository as it currently exists. It is meant as a status-quo inventory, not as a claim that every part is already clean, finished, or bug-free.

## Authorship Note

- The repository structure and the underlying project files are not purely AI-generated.
- This revised structure document was updated with AI assistance.
- The notes about active, experimental, and transitional areas are based on the current file layout in the repository.

## Quick Overview

SEDA is currently a Python project with two active entry paths:

- a CLI started through `main.py` and `model/controller.py`
- a Flet GUI started through `ui/ui.py`

Alongside the active app code, the repository also contains transition and development areas:

- a main SQLite database in `data/database.db`
- a separate food database in `data/bls_foods.sqlite`
- prototypes and intermediate work in `utils/`
- older UI states in `legacy/`
- learning and example code in `Beispiele/`
- raw BLS source material and an import script in `BLS_4_0_2025_DE/`

## Active Project Areas

### `model/`

This folder contains the domain and persistence logic.

Important files:

- `classes.py`: central domain classes such as `User`, `WaterLog`, `WeightLog`, `Food`, `Meal`, `MealItem`, `FoodLog`, and related helper classes
- `database.py`: SQLite access for the main application database and a separate `FoodDatabase` wrapper for the BLS food database; the file contains comments indicating partial AI-assisted adjustments
- `controller.py`: current CLI control flow connecting `ui.cli_view`, the model classes, and persistence; appears mostly manually evolved
- `open_food_api.py`: experimental Open Food Facts access; currently more of a development module than a fully integrated core component

### `ui/`

This folder contains the user interface layer.

Important files:

- `ui.py`: active Flet GUI; the file itself describes its base as AI-generated code with manual adaptations
- `cli_view.py`: command-line prompts and output helpers; includes some explicitly marked AI-generated sections
- `theme_utils.py`: small Flet theme helpers

Note:
Both the GUI and the CLI currently reach into `model/` directly. The project is not yet fully separated into strict layers.

### `data/`

This folder currently stores the project databases:

- `database.db`: main application database
- `bls_foods.sqlite`: separate SQLite database for food data

Both database files are runtime or generated data artifacts, not AI-generated source files.

### `tests/`

This folder contains automated tests for the active code.

Current contents:

- `test_classes.py`: tests for domain classes; includes explicitly marked AI-generated test parts
- `test_cli_view.py`: tests for CLI behavior; includes individual AI-marked sections
- `test_database.py`: tests for database behavior; contains several explicitly marked AI-generated sections
- `test.db`: empty or locally used test database file

### `docs/`

This folder contains project documentation.

Current contents:

- `de_struktur.md`: German structure overview; currently revised with AI assistance
- `en_structur.md`: this English structure overview; currently revised with AI assistance
- several exported diagrams as PNG files
- `Anforderungsanalyse Tabelle.ods`: analysis and planning material

## Additional Folders with Prototype or Transition Status

### `legacy/`

Older UI code that is no longer the main path, but is still kept for reference.

Current files:

- `ui_german.py`: older German-language GUI version; described in the file comments as AI-generated code with adjustments
- `ui_discardable.py`: explicitly discardable UI experiment; described in comments as test/example code and partly AI-generated

### `utils/`

Mixed area for helpers, prototypes, and personal intermediate work.

Current contents:

- `paginator.py`: active small helper for paginated CLI output; the docstring mentions partly AI-generated content
- `bine_cli_main.py`: alternative CLI prototype
- `tobi_cli_controller`: older CLI prototype
- `tobi_classes.py`: older or parallel class implementation; includes marked AI-generated helper parts
- `test_bine.py`: additional prototype-style tests; includes marked AI-generated fixture/test parts

Important:
`utils/` is not just a pure helper module folder at the moment. It also acts as a staging area for work-in-progress code.

### `Beispiele/`

Learning and example code that is not part of the main application path.

It includes:

- general Python practice files
- `flet_tutorial/` with Flet example code

### `BLS_4_0_2025_DE/`

Working area for the BLS food dataset.

Current contents include:

- original Excel and PDF source files for the BLS data
- `import_bls_to_sqlite.py` for building the SQLite food database
- a separate `venv/` inside that subfolder

The source files in this folder are external data assets rather than AI-generated project documentation.

## Important Files in the Repository Root

### `main.py`

Current application entry point.

Current behavior:

- shows a welcome message
- asks whether to start CLI, GUI, or show the license
- starts the Flet GUI for `g`
- starts the CLI controller for `c`
- shows the long-form license text for `l`

Origin note:
`main.py` does not currently contain an explicit AI-generation marker in its header.

### `config.py`

Central configuration for shared paths and project metadata.

Currently defines:

- `BASE_DIR`
- `DB_PATH`
- `FOOD_DB_PATH`
- `LICENSE_PATH`
- `DB_TEST_PATH`
- `DEVS`
- `VERSION`

Origin note:
`config.py` explicitly labels some parts as AI-generated and other parts as not AI-generated.

### `README.md`

Short project introduction with setup, run, and test notes. It is useful as an entry point, but not fully synchronized with every current repository detail.

Origin note:
The README describes itself as partly AI-generated.

### `bug_tracker.py`

Collection of known issues and technical debt. Not runtime logic, but relevant for planning and maintenance.

### `requirements.txt`

Lists the Python dependencies used by the project.

## Folders That Are More Environment Than Architecture

These exist in the repository, but are not part of the actual application structure:

- `venv/`: main virtual environment
- `BLS_4_0_2025_DE/venv/`: additional virtual environment in the BLS subfolder
- `__pycache__/`: Python cache files
- `.pytest_cache/`: pytest cache
- `.git/`: Git metadata
- `.codex`: local tool or editor artifact
- `test_db/`: target folder for temporary databases created during tests

## Status-Quo Summary

The current repository can be read in four practical layers:

- active application: `main.py`, `model/`, `ui/`, `data/`, `tests/`
- documentation and project tracking: `docs/`, `README.md`, `bug_tracker.py`
- prototypes and transition code: `utils/`, `legacy/`
- data preparation and learning material: `BLS_4_0_2025_DE/`, `Beispiele/`

That makes the project usable, but structurally mixed: active product code, prototypes, data preparation, and learning material still live fairly close together.
