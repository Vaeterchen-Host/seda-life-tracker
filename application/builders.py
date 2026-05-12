# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Shared object builders for turning database rows into domain objects."""

from dataclasses import fields

from model.class_user import User
from model.classes_food import BigSeven, Food, Meal, NutrientSummary
from model.classes_log import ActivityLog, MealLog, WaterLog, WeightLog
from model.database import Database


# ---------------------------
# Build model objects from database rows
# These helpers translate plain DB rows into Python objects like User, Meal or Log items.
# ---------------------------
def create_water_log_instances_for_user(main_db: Database, user_id):
    """Create an array of WaterLog instances for the user. Partly AI-generated."""
    return [
        WaterLog(
            log[0], log[1], log[2], log[3]
        )  # log[0] is id, log[1] is user_id, log[2] is amount_in_ml, log[3] is timestamp.
        for log in main_db.get_all_water_logs()  # pylint: disable=no-value-for-parameter
        if log[1] == user_id
    ]


def create_weight_log_instances_for_user(main_db: Database, user_id):
    """Create an array of WeightLog instances for the user. Partly AI-generated."""
    return [
        WeightLog(
            log[0], log[1], log[2], log[3], log[4]
        )  # log[0] is id, log[1] is user_id, log[2] is weight_in_kg, log[3] is height_in_cm, log[4] is timestamp.
        for log in main_db.get_all_weight_logs()  # pylint: disable=no-value-for-parameter
        if log[1] == user_id
    ]


def create_activity_log_instances_for_user(main_db: Database, user_id):
    """Create an array of ActivityLog instances for the user. Partly AI-generated."""
    return [
        ActivityLog(
            log[0], log[1], log[2], log[3], log[4], log[5], log[6]
        )  # log[0] is id, log[1] is user_id, log[2] is activity_name, log[3] is calories_burned, log[4] is activity_value, log[5] is unit_type, log[6] is timestamp.
        for log in main_db.get_all_activity_logs()  # pylint: disable=no-value-for-parameter
        if log[1] == user_id
    ]


def create_nutrient_summary_with_defaults(**overrides):
    """Create a nutrient summary with None defaults. AI-generated."""
    # fields(...) reads all dataclass attributes so we can build a complete summary shape.
    values = {field.name: None for field in fields(NutrientSummary)}
    values.update(overrides)
    return NutrientSummary(**values)


def create_food_instance_from_food_row(food_row, amount):
    """Create a Food instance from an external food DB row. AI-generated."""
    # The external food DB already stores the nutrient columns, so we map them into our objects here.
    big_seven = BigSeven(
        **{field.name: food_row[field.name] for field in fields(BigSeven)}
    )
    nutrient_summary = NutrientSummary(
        **{field.name: food_row[field.name] for field in fields(NutrientSummary)}
    )
    return Food(
        food_row["food_id"],
        food_row["name_de"] or food_row["name_en"],
        amount,
        food_row["unit_type"],
        food_row["kcal"],
        big_seven,
        nutrient_summary,
    )


def create_food_instance_from_meal_item_row(meal_item_row):
    """Create a Food instance from a meal item DB row. AI-generated."""
    big_seven = BigSeven(
        fat=meal_item_row[6],
        saturated_fat=meal_item_row[7],
        carbohydrate=meal_item_row[8],
        fibre=meal_item_row[9],
        sugar=meal_item_row[10],
        protein=meal_item_row[11],
        salt=meal_item_row[12],
    )
    nutrient_summary = create_nutrient_summary_with_defaults(sodium=meal_item_row[13])
    return Food(
        meal_item_row[1],
        meal_item_row[2],
        meal_item_row[3],
        meal_item_row[4],
        meal_item_row[5],
        big_seven,
        nutrient_summary,
    )


def create_meal_instance_from_db(main_db: Database, meal_row):
    """Create a Meal instance with its food items from DB data. AI-generated."""
    food_items = [
        create_food_instance_from_meal_item_row(item_row)
        for item_row in main_db.get_meal_food_items(
            meal_row[0]
        )  # pylint: disable=no-value-for-parameter
    ]
    return Meal(meal_row[0], meal_row[1], food_items)


def create_meal_instances(main_db: Database):
    """Create Meal instances for all stored meal templates. AI-generated."""
    return [
        create_meal_instance_from_db(main_db, meal_row)
        for meal_row in main_db.get_all_meals()  # pylint: disable=no-value-for-parameter
    ]


def create_meal_log_instances_for_user(main_db: Database, user_id):
    """Create an array of MealLog instances for the user. Partly AI-generated."""
    return [
        MealLog(
            log[0],
            log[1],
            create_meal_instance_from_db(main_db, (log[2], log[3])),
            log[4],
            log[5],
            log[6],
        )  # log[0] is meal_log_id, log[1] is user_id, log[2] is meal_id, log[3] is meal_name, log[4] is amount, log[5] is unit_type, log[6] is timestamp.
        for log in main_db.get_user_meal_logs(
            user_id
        )  # pylint: disable=no-value-for-parameter
    ]


def create_user_instance_from_db(main_db: Database, db_user):
    """Create a User class instance from database data."""
    return User(
        db_user[0],  # id
        db_user[1],  # name
        db_user[2],  # birthdate
        db_user[3],  # height_in_cm
        db_user[4],  # gender
        db_user[5],  # fitness_lvl
        create_water_log_instances_for_user(main_db, db_user[0]),  # water_logs
        create_weight_log_instances_for_user(main_db, db_user[0]),  # weight_logs
        create_meal_log_instances_for_user(main_db, db_user[0]),  # meal_logs
        create_activity_log_instances_for_user(main_db, db_user[0]),  # activity_logs
    )
