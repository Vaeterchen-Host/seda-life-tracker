# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Shared meal helpers for CLI and GUI."""

from model.classes_food import Meal
from model.database import Database

from application.builders import create_food_instance_from_food_row


# ---------------------------
# Meal helpers
# Small shared helpers around meal-template construction.
# ---------------------------
def create_single_food_meal(main_db: Database, food_row):
    """Create a one-food meal object for direct logging. AI-generated."""
    meal_name = food_row["name_de"] or food_row["name_en"]
    meal_id = main_db.add_meal(meal_name)  # pylint: disable=no-value-for-parameter
    # Food DB values are stored per 100 units, so the helper meal uses 100 g/ml as its base.
    food_item = create_food_instance_from_food_row(food_row, 100)
    main_db.add_meal_food_item(
        meal_id, food_item.id, food_item.amount, food_item.unit_type
    )  # pylint: disable=no-value-for-parameter
    return Meal(meal_id, meal_name, [food_item])
