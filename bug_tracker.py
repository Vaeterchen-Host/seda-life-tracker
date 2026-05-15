# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Known bugs and technical debt for SEDA."""

# pylint: skip-file

BUGS = [
    {
        "id": "BUG-001",
        "title": "Timestamp input in CLI is awkward",
        "status": "open",
        "priority": "medium",
        "area": "ui/cli_view.py",
        "notes": "User currently has to enter ISO format manually.",
    },
    {
        "id": "BUG-002",
        "title": "Height input validation is inconsistent",
        "status": "open",
        "priority": "medium",
        "area": "ui/cli_view.py",
        "notes": "Validation and error messages around height input still need cleanup.",
    },
    {
        "id": "BUG-003",
        "title": "controller.main mixes setup, DB loading and menu control",
        "status": "open",
        "priority": "low",
        "area": "controllers/cli_controller.py",
        "notes": "Pylint reports too many statements, branches and local variables in main(). Not urgent, but worth refactoring later.",
    },
    {
        "id": "BUG-004",
        "title": "create_user_instance_from_db depends on loop variable db_user",
        "status": "open",
        "priority": "medium",
        "area": "application/builders.py",
        "notes": "The function reads db_user from outer scope. This is fragile and depends on previous control flow."
        "Currently i don't care because of the single-user setup, but this will need to be addressed for multi-user support.",
    },
    {
        "id": "BUG-005",
        "title": "Water and weight logs are loaded without filtering by user",
        "status": "open",
        "priority": "low",
        "area": "application/builders.py",
        "notes": "create_water_log_instances_for_user() and create_weight_log_instances_for_user() currently load every log from the database."
        " This is not a problem with the current single-user setup, but will need to be addressed for multi-user support.",
    },
    {
        "id": "BUG-006",
        "title": "Controller and view naming is still inconsistent",
        "status": "open",
        "priority": "medium",
        "area": "controllers/cli_controller.py / ui/cli_view.py",
        "notes": "There are several similar names such as show_user_info_from_class, create_water_log_parameters_by_input and older variants. This makes wiring easy to break.",
    },
    {
        "id": "BUG-007",
        "title": "BMI calculator has not implemented the age, yet.",
        "status": "open",
        "priority": "low",
        "area": "model/classes.py",
        "notes": "User.calculate_bmi() already exists.",
    },
    {
        "id": "BUG-008",
        "title": "Daily water intake calculator missing",
        "status": "closed",
        "priority": "high",
        "area": "future feature",
        "notes": "This is more of a future feature than a bug.",
    },
    {
        "id": "BUG-009",
        "title": "utils folder is used as a mixed staging area",
        "status": "open",
        "priority": "low",
        "area": "utils/",
        "notes": "The folder should ideally contain only helper functions, or be split into clearer responsibility-based folders later.",
    },
    {
        "id": "BUG-010",
        "title": "Legacy code can be confused with active UI code",
        "status": "open",
        "priority": "low",
        "area": "legacy/ / ui/",
        "notes": "The purpose of legacy code should stay clearly separated from actively maintained UI code.",
    },
    {
        "id": "BUG-011",
        "title": "ui_discardable.py is not clearly marked as experimental",
        "status": "open",
        "priority": "low",
        "area": "ui/ui_discardable.py",
        "notes": "The file should either be removed later or marked more clearly as experimental or disposable UI code.",
    },
    {
        "id": "BUG-012",
        "title": "CLI should display long license text page by page",
        "status": "closed",
        "priority": "low",
        "area": "ui/cli_view.py / controllers/cli_controller.py",
        "notes": "If the GPL text is shown in the CLI, it should be paginated, for example in blocks of 25 to 30 lines with Enter to continue, instead of printing one very long block.",
    },
    {
        "id": "BUG-013",
        "title": "Unit of measurement for food and beverages",
        "status": "open",
        "priority": "medium",
        "area": "classes.py",
        "notes": "for logical reasons, we should define the measurement of 'amount_in_gram' to 'amount_in_gram_or_mililiters', as we are also going to track beverages such as coca cola etc. ",
    },
    {
        "id": "BUG-014",
        "title": "Temporary food database demo function should be removed or replaced",
        "status": "open",
        "priority": "low",
        "area": "ui/cli_view.py",
        "notes": "The temporary demonstration-only function should not remain in the final version and needs to be deleted or replaced later.",
    },
    {
        "id": "BUG-015",
        "title": "MealLog model and meal_logs table use different data shapes",
        "status": "open",
        "priority": "medium",
        "area": "model/classes.py / model/database.py",
        "notes": "MealLog currently expects amount_in_gram, but the meal_logs table and add_meal_log() only store user_id, meal_id and timestamp. This needs to be aligned before meal log handling is extended further.",
    },
    {
        "id": "BUG-016",
        "title": "metabolic rate is not being calculated by the most recent weight log",
        "status": "open",
        "priority": "high",
        "area": "model/classes.py / model/database.py",
        "notes": "when enterint a new weight log with a past date, the metabolic rate calculates its value from this last log, although it is not the most current weight",
    },    # Partly AI-refactored: GUI and UX planning items now live in docs/gui_backlog.md.
]
