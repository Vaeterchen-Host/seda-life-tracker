# SEDA

> This README is partly ai-generated.
> AI-updated for the current V0.5 project status.

SEDA is a Python fitness tracking project with both a command-line interface and a graphical interface. The current codebase supports user data, water logs, weight logs, meal and food tracking, activity logs, and SQLite-backed persistence.

## Current Features

- start either the CLI or GUI from `main.py`
- manage one user profile
- store water intake entries
- store weight entries
- search foods in the external BLS food database
- build and save meal templates
- log meals and direct single-food intake
- store activity entries with burned calories
- calculate values such as daily water intake, BMI, calorie target, and daily calorie balance
- switch GUI language between German and English
- persist data in SQLite
- cover core behavior with automated tests

## Project Layout

- `main.py` starts the application
- `model/` contains domain classes, database code, and CLI control flow
- `ui/` contains the Flet GUI, CLI view helpers, and GUI translations
- `data/` stores the main SQLite database
- `test_db/` contains isolated test database fixtures
- `tests/` contains automated tests
- `docs/` contains structure notes and release documentation folders
- `docs/gui_backlog.md` collects GUI and UX follow-up work
- `docs/design_system.md` captures stable GUI style conventions
- `BLS_4_0_2025_DE/` contains the source material and import helper for the external food database
- `Beispiele/` contains learning and tutorial files that are not part of the runtime path
- `legacy/` keeps older code for reference
- `utils/` contains helper and experimental files

For a more detailed overview, see [docs/de_struktur.md](/home/vaeterchen_host/Documents/3_Programmierung/Python/Projekte/seda/docs/de_struktur.md) and [docs/en_structur.md](/home/vaeterchen_host/Documents/3_Programmierung/Python/Projekte/seda/docs/en_structur.md).

## Requirements

The project currently stores its dependencies in `requirements.txt`.

Typical setup:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the Project

Start the application with:

```bash
python main.py
```

You will then be asked whether to launch:

- the GUI
- the CLI
- or the license view

## Running Tests

Run the test suite with:

```bash
python -m pytest
```

## Notes

- The project currently mixes active code, utilities, and older experiments.
- `bug_tracker.py` documents known issues and technical debt.
- `docs/gui_backlog.md` separates GUI and UX planning from the technical bug tracker.
- `docs/design_system.md` keeps shared layout and style rules in one place.
- `docs/` also contains exported diagrams, analysis files, and release-specific documentation folders such as `docs/v0.1/` and `docs/v0.5/`.
- The external food lookup data used by the nutrition features is stored separately from the main app database.

## Contact
For questions or contributions, please reach out to the project maintainers [Vaeterchen_Host](https://github.com/Vaeterchen-Host) and [binerino](https://github.com/binerino).
Pull requests and issues are welcome!
