# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""CLI controller functions for SEDA."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# pylint: disable=E1120, C0301

import ui.cli_view
from application.builders import (
    create_food_instance_from_food_row,
    create_meal_instances,
    create_user_instance_from_db,
)
from application.meal_service import create_single_food_meal
from application.status_service import get_today_calorie_status, get_today_water_status
from application.user_service import refresh_user_logs_from_db
from model.class_user import User
from model.classes_food import Meal
from model.database import Database, FoodDatabase


# ---------------------------
# Setup and database access
# These functions start the databases and check whether a connection works.
# ---------------------------
def connect_main_db():
    """Create the main database object and check the connection once."""
    main_db = Database()
    ui.cli_view.show_message("Connect with Database...")
    main_db_connection = main_db.connect()

    if main_db_connection is None:
        ui.cli_view.show_message("Failed to connect to the database. Exiting.")
        sys.exit(1)

    main_db.end_connection(main_db_connection)
    ui.cli_view.show_message("Connected with Database.")
    return main_db


def connect_food_db():
    """Create the food database object and check the connection once."""
    food_db = FoodDatabase()
    ui.cli_view.show_message("Connect with FoodDatabase...")
    food_db_connection = food_db.connect()

    if food_db_connection is None:
        ui.cli_view.show_message("Failed to connect to the FoodDatabase. Exiting.")
        sys.exit(1)

    food_db.end_connection(food_db_connection)
    ui.cli_view.show_message("Connected with FoodDatabase.")
    return food_db


def get_or_create_user(main_db: Database):
    """Create a user by existing data or by input."""
    users = main_db.get_all_users()  # pylint: disable=no-value-for-parameter

    if not users:
        ui.cli_view.show_message("No users found. Let's create a new user.")
        name, birthdate, height_in_cm, gender, fitness_lvl = (
            ui.cli_view.create_user_by_input()
        )
        user_id = main_db.add_user(
            name,
            birthdate,
            height_in_cm,
            gender,
            fitness_lvl,
        )  # pylint: disable=no-value-for-parameter
        return User(
            user_id,
            name,
            birthdate,
            height_in_cm,
            gender,
            fitness_lvl,
            [],
            [],
            [],
            [],
        )

    ui.cli_view.show_message("Existing user found:")
    for db_user in users:
        ui.cli_view.show_message(f"""
                ID: {db_user[0]}
                Name: {db_user[1]}
                Birthdate: {db_user[2]}
                Height: {db_user[3]} cm
                Gender: {db_user[4]}
                Fitness level: {db_user[5]}
            """)

    return create_user_instance_from_db(main_db, users[0])


# ---------------------------
# User profile actions
# These functions handle user data like showing or changing biometrical information.
# ---------------------------
def show_user_information(user: User):
    """Show the user's information."""
    ui.cli_view.show_user_info_from_class(user)


def update_biometrical_information(main_db: Database, user: User):
    """Change the user's biometrical information."""
    name, birthdate, height_in_cm, gender, fitness_lvl = (
        ui.cli_view.change_user_information(user)
    )  # pylint: disable=E1111

    user.name = name
    user.update_biometrical_data(
        birthdate=birthdate,
        height_in_cm=height_in_cm,
        gender=gender,
        fitness_lvl=fitness_lvl,
    )
    main_db.update_user(
        user.user_id,
        user.name,
        user.birthdate,
        user.height_in_cm,
        user.gender,
        user.fitness_lvl,
    )  # pylint: disable=no-value-for-parameter
    ui.cli_view.show_message("\nUser information updated successfully!\n")
    show_user_information(user)


# ---------------------------
# Water log actions
# CRUD for water logs plus today's water-related output.
# ---------------------------
def add_water_log(main_db: Database, user: User):
    """Add a water log to the user and persist it."""
    amount_in_ml, timestamp = ui.cli_view.create_water_log_parameters_by_input()
    new_log = user.water_log_handler.create_log(None, amount_in_ml, timestamp)
    db_id = main_db.add_water_log(
        user.user_id, new_log.amount_in_ml, new_log.timestamp
    )  # pylint: disable=no-value-for-parameter
    new_log.set_database_id(db_id)
    ui.cli_view.show_message("\nWater log added successfully!\n")


def show_water_logs(user: User):
    """Show all water logs of the user."""
    ui.cli_view.show_water_logs_from_db(user.water_log_handler.logs)


def delete_water_log(main_db: Database, user: User):
    """Delete a water log from the user object and the DB."""
    show_water_logs(user)
    water_log_id = ui.cli_view.prompt_log_id()
    if water_log_id is None:
        return
    if water_log_id not in [log.id for log in user.water_log_handler.logs]:
        ui.cli_view.show_message("Log not found. Please enter a valid log ID.")
        return

    deleted_rows = main_db.delete_water_log(
        water_log_id
    )  # pylint: disable=no-value-for-parameter
    if not deleted_rows:
        ui.cli_view.show_message("Water log could not be deleted from the database.")
        return

    user.water_log_handler.delete_log(water_log_id)
    ui.cli_view.show_message("\nWater log deleted successfully!\n")
    show_water_logs(user)


def add_weight_log(main_db: Database, user: User):
    """Add a weight log to the user and persist it."""
    weight_in_kg, timestamp = ui.cli_view.create_weight_log_by_input()
    new_log = user.weight_log_handler.create_log(
        None,
        weight_in_kg,
        user.height_in_cm,
        timestamp,
    )
    db_id = main_db.add_weight_log(
        user.user_id,
        new_log.weight_in_kg,
        new_log.height_in_cm,
        new_log.timestamp,
    )  # pylint: disable=no-value-for-parameter
    new_log.set_database_id(db_id)
    ui.cli_view.show_message("\nWeight log added successfully!\n")


def show_weight_logs(user: User):
    """Show all weight logs of the user."""
    ui.cli_view.show_weight_logs(user.weight_log_handler.logs)


def delete_weight_log(main_db: Database, user: User):
    """Delete a weight log from the user object and the DB."""
    show_weight_logs(user)
    weight_log_id = ui.cli_view.prompt_log_id()
    if weight_log_id is None:
        return
    if weight_log_id not in [log.id for log in user.weight_log_handler.logs]:
        ui.cli_view.show_message("Log not found. Please enter a valid log ID.")
        return

    deleted_rows = main_db.delete_weight_log(
        weight_log_id
    )  # pylint: disable=no-value-for-parameter
    if not deleted_rows:
        ui.cli_view.show_message("Weight log could not be deleted from the database.")
        return

    user.weight_log_handler.delete_log(weight_log_id)
    ui.cli_view.show_message("\nWeight log deleted successfully!\n")
    show_weight_logs(user)


def show_today_water_intake(user: User):
    """Show the user's current water intake for today."""
    ui.cli_view.show_message(
        f"\nToday's water intake: {user.water_log_handler.water_intake_today()} ml\n"
    )


def show_last_bmi(user: User):
    """Show the BMI of the latest weight log."""
    if user.last_bmi is None:
        ui.cli_view.show_message("\nNo BMI available yet.\n")
        return
    ui.cli_view.show_message(f"\nBMI: {user.last_bmi}\n")


# ---------------------------
# Food search and meal-building helpers
# These functions search foods and assemble Meal objects from chosen food items.
# ---------------------------
def search_foods(food_db: FoodDatabase):
    """Search foods in the external food database and display results. AI-generated."""
    search_term = ui.cli_view.prompt_food_search_term()
    if not search_term:
        ui.cli_view.show_message("Search aborted.")
        return []
    food_rows = food_db.search_foods(search_term)
    if not food_rows:
        ui.cli_view.show_message("No foods found.")
        return []
    ui.cli_view.show_food_search_results(food_rows)
    return food_rows


def choose_food_from_search_results(food_rows):
    """Choose one food from search results. AI-generated."""
    if not food_rows:
        return None
    selected_food_id = ui.cli_view.prompt_food_id()
    if selected_food_id is None:
        return None
    for food_row in food_rows:
        if food_row["food_id"] == selected_food_id:
            return food_row
    ui.cli_view.show_message("Food not found in the current result list.")
    return None


def collect_food_items_for_meal(food_db: FoodDatabase):
    """Collect food items for a meal template from food search results. AI-generated."""
    food_items = []
    while True:
        food_rows = search_foods(food_db)
        if not food_rows:
            break
        selected_food_row = choose_food_from_search_results(food_rows)
        if selected_food_row is None:
            ui.cli_view.show_message("Please choose a valid food from the shown list.")
            continue

        amount = ui.cli_view.prompt_food_amount(selected_food_row["unit_type"])
        if amount is None:
            continue

        # The chosen DB row is translated into one Food object that can be reused by CLI and later UI.
        food_items.append(create_food_instance_from_food_row(selected_food_row, amount))

        if not ui.cli_view.prompt_yes_no("Add another food to this meal? (y/n): "):
            break
    return food_items


def create_meal_template(main_db: Database, food_db: FoodDatabase):
    """Create a meal template from searched foods. AI-generated."""
    meal_name = ui.cli_view.prompt_meal_name()
    if not meal_name:
        ui.cli_view.show_message("Meal creation aborted.")
        return None

    meal_id = main_db.add_meal(meal_name)  # pylint: disable=no-value-for-parameter
    meal = Meal(meal_id, meal_name, [])

    for food_item in collect_food_items_for_meal(food_db):
        meal.add_food_item(food_item)
        main_db.add_meal_food_item(
            meal.id, food_item.id, food_item.amount, food_item.unit_type
        )  # pylint: disable=no-value-for-parameter

    if not meal.food_items:
        main_db.delete_meal(meal.id)  # pylint: disable=no-value-for-parameter
        ui.cli_view.show_message("\nMeal creation aborted. No foods were added.\n")
        return None

    ui.cli_view.show_message(f"\nMeal template '{meal.name}' added successfully.\n")
    return meal


# ---------------------------
# Meal template actions
# Create, update, show and delete reusable meal templates.
# ---------------------------
def update_meal_template(main_db: Database, food_db: FoodDatabase):
    """Update a meal template name and optionally rebuild its foods. AI-generated."""
    meals = create_meal_instances(main_db)
    if not meals:
        ui.cli_view.show_message("No meal templates found.")
        return
    ui.cli_view.show_meal_templates(meals)
    meal_id = ui.cli_view.prompt_meal_id()
    if meal_id is None:
        return
    selected_meal = next((meal for meal in meals if meal.id == meal_id), None)
    if selected_meal is None:
        ui.cli_view.show_message("Meal template not found.")
        return

    new_name = (
        ui.cli_view.prompt_optional_text(
            f"Enter the new meal template name or nothing to keep '{selected_meal.name}': "
        )
        or selected_meal.name
    )
    main_db.update_meal(meal_id, new_name)  # pylint: disable=no-value-for-parameter

    if ui.cli_view.prompt_yes_no(
        "Do you want to rebuild the foods of this meal? (y/n): "
    ):
        # Rebuilding is simpler and safer here than editing individual meal items one by one.
        new_food_items = collect_food_items_for_meal(food_db)
        if not new_food_items:
            ui.cli_view.show_message(
                "No new foods were selected. Keeping the previous meal composition."
            )
        else:
            main_db.delete_meal_food_items(
                meal_id
            )  # pylint: disable=no-value-for-parameter
            for food_item in new_food_items:
                main_db.add_meal_food_item(
                    meal_id,
                    food_item.id,
                    food_item.amount,
                    food_item.unit_type,
                )  # pylint: disable=no-value-for-parameter

    ui.cli_view.show_message("\nMeal template updated successfully.\n")


def show_meal_templates(main_db: Database):
    """Show all meal templates. AI-generated."""
    meals = create_meal_instances(main_db)
    ui.cli_view.show_meal_templates(meals)


def delete_meal_template(main_db: Database):
    """Delete one meal template. AI-generated."""
    meal_id = ui.cli_view.prompt_meal_id()
    if meal_id is None:
        return
    deleted_rows = main_db.delete_meal(
        meal_id
    )  # pylint: disable=no-value-for-parameter
    if not deleted_rows:
        ui.cli_view.show_message("Meal template not found.")
        return
    ui.cli_view.show_message("\nMeal template deleted successfully.\n")


# ---------------------------
# Meal log actions
# Log eaten meals or single foods and keep the meal log in sync with the database.
# ---------------------------
def add_meal_log(main_db: Database, user: User):
    """Log a consumed meal for the current user. AI-generated."""
    meals = create_meal_instances(main_db)
    if not meals:
        ui.cli_view.show_message("No meal templates found.")
        return

    ui.cli_view.show_meal_templates(meals)
    meal_id = ui.cli_view.prompt_meal_id()
    if meal_id is None:
        return
    selected_meal = next((meal for meal in meals if meal.id == meal_id), None)
    if selected_meal is None:
        ui.cli_view.show_message("Meal template not found.")
        return

    amount, unit_type, timestamp = ui.cli_view.prompt_meal_log_parameters()
    if amount is None:
        return

    new_log = user.meal_log_handler.create_log(
        None, selected_meal, amount, unit_type, timestamp
    )
    db_id = main_db.add_meal_log(
        user.user_id, selected_meal.id, amount, unit_type, new_log.timestamp
    )  # pylint: disable=no-value-for-parameter
    new_log.set_database_id(db_id)
    ui.cli_view.show_message("\nMeal log added successfully.\n")


def add_single_food_log(main_db: Database, food_db: FoodDatabase, user: User):
    """Log one searched food directly without manual meal-template creation. AI-generated."""
    food_rows = search_foods(food_db)
    selected_food_row = choose_food_from_search_results(food_rows)
    if selected_food_row is None:
        return

    amount, timestamp = ui.cli_view.prompt_single_food_log_parameters(
        selected_food_row["unit_type"]
    )
    if amount is None:
        return

    single_food_meal = create_single_food_meal(main_db, selected_food_row)
    new_log = user.meal_log_handler.create_log(
        None,
        single_food_meal,
        amount,
        selected_food_row["unit_type"],
        timestamp,
    )
    db_id = main_db.add_meal_log(
        user.user_id,
        single_food_meal.id,
        amount,
        selected_food_row["unit_type"],
        new_log.timestamp,
    )  # pylint: disable=no-value-for-parameter
    new_log.set_database_id(db_id)
    ui.cli_view.show_message("\nSingle food log added successfully.\n")


def update_meal_log(main_db: Database, user: User):
    """Update one meal log in object state and DB. AI-generated."""
    meals = create_meal_instances(main_db)
    if not meals:
        ui.cli_view.show_message("No meal templates found.")
        return
    show_meal_logs(user)
    meal_log_id = ui.cli_view.prompt_log_id()
    if meal_log_id is None:
        return
    selected_log = next(
        (log for log in user.meal_log_handler.logs if log.id == meal_log_id), None
    )
    if selected_log is None:
        ui.cli_view.show_message("Log not found. Please enter a valid log ID.")
        return

    ui.cli_view.show_meal_templates(meals)
    new_meal_id = ui.cli_view.prompt_optional_int(
        f"Enter a new meal ID or nothing to keep '{selected_log.meal.name}': "
    )
    selected_meal = (
        next((meal for meal in meals if meal.id == new_meal_id), None)
        if new_meal_id is not None
        else selected_log.meal
    )
    if selected_meal is None:
        ui.cli_view.show_message(
            "Meal template not found. Returning to the previous menu."
        )
        return

    # Empty input means "keep current value", so updates stay convenient in CLI and reusable for UI.
    new_amount = ui.cli_view.prompt_optional_float(
        f"Enter a new amount or nothing to keep {selected_log.amount}: "
    )
    if new_amount is None:
        new_amount = selected_log.amount
    new_unit_type = (
        ui.cli_view.prompt_optional_text(
            f"Enter a new unit type or nothing to keep '{selected_log.unit_type}': "
        )
        or selected_log.unit_type
    )
    new_timestamp = ui.cli_view.prompt_optional_timestamp() or selected_log.timestamp

    main_db.update_meal_log(
        meal_log_id,
        selected_meal.id,
        new_amount,
        new_unit_type,
        new_timestamp,
    )  # pylint: disable=no-value-for-parameter
    user.meal_log_handler.update_log(
        meal_log_id,
        new_meal=selected_meal,
        new_amount=new_amount,
        new_unit_type=new_unit_type,
        new_timestamp=new_timestamp,
    )
    ui.cli_view.show_message("\nMeal log updated successfully.\n")


def show_meal_logs(user: User):
    """Show all meal logs of the user. AI-generated."""
    ui.cli_view.show_meal_logs(user.meal_log_handler.logs)


def delete_meal_log(main_db: Database, user: User):
    """Delete one meal log from DB and object state. AI-generated."""
    show_meal_logs(user)
    meal_log_id = ui.cli_view.prompt_log_id()
    if meal_log_id is None:
        return
    if meal_log_id not in [log.id for log in user.meal_log_handler.logs]:
        ui.cli_view.show_message("Log not found. Please enter a valid log ID.")
        return

    deleted_rows = main_db.delete_meal_log(
        meal_log_id
    )  # pylint: disable=no-value-for-parameter
    if not deleted_rows:
        ui.cli_view.show_message("Meal log could not be deleted from the database.")
        return

    user.meal_log_handler.delete_log(meal_log_id)
    ui.cli_view.show_message("\nMeal log deleted successfully.\n")


# ---------------------------
# Daily status helpers
# These connect shared status data to CLI output.
# ---------------------------
def show_today_water_status(user: User):
    """Show today's water status. AI-generated."""
    ui.cli_view.show_water_status(get_today_water_status(user))


def show_today_calorie_status(user: User):
    """Show the current calorie status of today. AI-generated."""
    status = get_today_calorie_status(user)
    intake = status["intake"]
    burned = status["burned"]
    net = status["net"]
    target = status["target"]
    if target is None:
        ui.cli_view.show_message(
            f"\nCalories eaten today: {intake} kcal\nCalories burned today: {burned} kcal\nNet calories today: {net} kcal\nNo calorie target available yet. Please add a weight log.\n"
        )
        return
    ui.cli_view.show_message(
        f"\nCalories eaten today: {intake} kcal\nCalories burned today: {burned} kcal\nNet calories today: {net} kcal\nTarget today: {target} kcal\nDifference: {status['difference']} kcal\n"
    )


# ---------------------------
# Activity log actions
# CRUD for burned-calorie entries.
# ---------------------------
def add_activity_log(main_db: Database, user: User):
    """Add an activity log to the user and persist it. AI-generated."""
    activity_name, calories_burned, activity_value, timestamp = (
        ui.cli_view.prompt_activity_log_parameters()
    )
    if activity_name is None:
        return
    new_log = user.activity_log_handler.create_log(
        None,
        activity_name,
        calories_burned,
        activity_value,
        "minutes",
        timestamp,
    )
    db_id = main_db.add_activity_log(
        user.user_id,
        new_log.activity_name,
        new_log.calories_burned,
        new_log.activity_value,
        new_log.unit_type,
        new_log.timestamp,
    )  # pylint: disable=no-value-for-parameter
    new_log.set_database_id(db_id)
    ui.cli_view.show_message("\nActivity log added successfully.\n")


def show_activity_logs(user: User):
    """Show all activity logs of the user. AI-generated."""
    ui.cli_view.show_activity_logs(user.activity_log_handler.logs)


def update_activity_log(main_db: Database, user: User):
    """Update one activity log in object state and DB. AI-generated."""
    show_activity_logs(user)
    activity_log_id = ui.cli_view.prompt_log_id()
    if activity_log_id is None:
        return
    selected_log = next(
        (log for log in user.activity_log_handler.logs if log.id == activity_log_id),
        None,
    )
    if selected_log is None:
        ui.cli_view.show_message("Log not found. Please enter a valid log ID.")
        return

    new_activity_name = (
        ui.cli_view.prompt_optional_text(
            f"Enter a new activity name or nothing to keep '{selected_log.activity_name}': "
        )
        or selected_log.activity_name
    )
    new_calories_burned = ui.cli_view.prompt_optional_float(
        f"Enter new burned calories or nothing to keep {selected_log.calories_burned}: "
    )
    if new_calories_burned is None:
        new_calories_burned = selected_log.calories_burned
    new_activity_value = ui.cli_view.prompt_optional_float(
        f"Enter a new duration in minutes or nothing to keep {selected_log.activity_value}: "
    )
    if new_activity_value is None:
        new_activity_value = selected_log.activity_value
    new_timestamp = ui.cli_view.prompt_optional_timestamp() or selected_log.timestamp

    main_db.update_activity_log(
        activity_log_id,
        new_activity_name,
        new_calories_burned,
        new_activity_value,
        selected_log.unit_type,
        new_timestamp,
    )  # pylint: disable=no-value-for-parameter
    user.activity_log_handler.update_log(
        activity_log_id,
        new_activity_name=new_activity_name,
        new_calories_burned=new_calories_burned,
        new_activity_value=new_activity_value,
        new_timestamp=new_timestamp,
    )
    ui.cli_view.show_message("\nActivity log updated successfully.\n")


def delete_activity_log(main_db: Database, user: User):
    """Delete one activity log from DB and object state. AI-generated."""
    show_activity_logs(user)
    activity_log_id = ui.cli_view.prompt_log_id()
    if activity_log_id is None:
        return
    if activity_log_id not in [log.id for log in user.activity_log_handler.logs]:
        ui.cli_view.show_message("Log not found. Please enter a valid log ID.")
        return

    deleted_rows = main_db.delete_activity_log(
        activity_log_id
    )  # pylint: disable=no-value-for-parameter
    if not deleted_rows:
        ui.cli_view.show_message("Activity log could not be deleted from the database.")
        return

    user.activity_log_handler.delete_log(activity_log_id)
    ui.cli_view.show_message("\nActivity log deleted successfully.\n")


# ---------------------------
# Account action
# This removes the current user and then loads or creates the next active user.
# ---------------------------
def delete_current_user(main_db: Database, user: User):
    """Delete the current user and return the next active user. AI-generated."""
    if not ui.cli_view.prompt_yes_no(
        "Do you really want to delete the current user account? (y/n): "
    ):
        ui.cli_view.show_message("User deletion aborted.")
        return user

    deleted_rows = main_db.delete_user_by_id(
        user.user_id
    )  # pylint: disable=no-value-for-parameter
    if not deleted_rows:
        ui.cli_view.show_message("User could not be deleted from the database.")
        return user

    ui.cli_view.show_message("\nUser deleted successfully.\n")
    new_user = get_or_create_user(main_db)
    refresh_user_logs_from_db(main_db, new_user)
    return new_user


# ---------------------------
# CLI menus
# These functions connect the view input to the controller actions above.
# ---------------------------
def run_water_log_menu(main_db: Database, user: User):
    """Run the water log CLI menu."""
    while True:
        water_log_choice = ui.cli_view.prompt_water_log_menu()
        if water_log_choice == "1":
            add_water_log(main_db, user)
        elif water_log_choice == "2":
            show_water_logs(user)
        elif water_log_choice == "3":
            delete_water_log(main_db, user)
        elif water_log_choice == "4":
            show_today_water_intake(user)
        elif water_log_choice == "5":
            show_today_water_status(user)
        elif water_log_choice == "6":
            break
        else:
            ui.cli_view.show_message("Invalid choice. Please try again.")


def run_weight_log_menu(main_db: Database, user: User):
    """Run the weight log CLI menu."""
    while True:
        weight_log_choice = ui.cli_view.prompt_weight_log_menu()
        if weight_log_choice == "1":
            add_weight_log(main_db, user)
        elif weight_log_choice == "2":
            show_weight_logs(user)
        elif weight_log_choice == "3":
            delete_weight_log(main_db, user)
        elif weight_log_choice == "4":
            show_last_bmi(user)
        elif weight_log_choice == "5":
            break
        else:
            ui.cli_view.show_message("Invalid choice. Please try again.")


def run_meal_menu(main_db: Database, food_db: FoodDatabase, user: User):
    """Run the meal and calorie CLI menu. AI-generated."""
    while True:
        meal_choice = ui.cli_view.prompt_meal_menu()
        if meal_choice == "1":
            search_foods(food_db)
        elif meal_choice == "2":
            create_meal_template(main_db, food_db)
        elif meal_choice == "3":
            show_meal_templates(main_db)
        elif meal_choice == "4":
            update_meal_template(main_db, food_db)
        elif meal_choice == "5":
            delete_meal_template(main_db)
        elif meal_choice == "6":
            add_single_food_log(main_db, food_db, user)
        elif meal_choice == "7":
            add_meal_log(main_db, user)
        elif meal_choice == "8":
            show_meal_logs(user)
        elif meal_choice == "9":
            update_meal_log(main_db, user)
        elif meal_choice == "10":
            delete_meal_log(main_db, user)
        elif meal_choice == "11":
            show_today_calorie_status(user)
        elif meal_choice == "12":
            break
        else:
            ui.cli_view.show_message("Invalid choice. Please try again.")


def run_activity_log_menu(main_db: Database, user: User):
    """Run the activity log CLI menu. AI-generated."""
    while True:
        activity_choice = ui.cli_view.prompt_activity_menu()
        if activity_choice == "1":
            add_activity_log(main_db, user)
        elif activity_choice == "2":
            show_activity_logs(user)
        elif activity_choice == "3":
            update_activity_log(main_db, user)
        elif activity_choice == "4":
            delete_activity_log(main_db, user)
        elif activity_choice == "5":
            break
        else:
            ui.cli_view.show_message("Invalid choice. Please try again.")


def cli_menu(main_db: Database, food_db: FoodDatabase, user: User):
    """Run the main CLI menu loop."""
    while True:
        choice = ui.cli_view.prompt_main_menu().lower()
        if choice == "1":
            show_user_information(user)
        elif choice == "2":
            run_water_log_menu(main_db, user)
        elif choice == "3":
            run_weight_log_menu(main_db, user)
        elif choice == "4":
            run_meal_menu(main_db, food_db, user)
        elif choice == "5":
            run_activity_log_menu(main_db, user)
        elif choice == "6":
            update_biometrical_information(main_db, user)
        elif choice == "7":
            show_today_calorie_status(user)
        elif choice == "8":
            user = delete_current_user(main_db, user)
        elif choice == "9":
            ui.cli_view.show_message("Exiting the program. Goodbye!")
            sys.exit(0)
        elif choice == "l":
            ui.cli_view.show_license_long()
        else:
            ui.cli_view.show_message("Invalid choice. Please try again.")


# ---------------------------
# Program entry point
# This is the small bootstrap that starts CLI mode.
# ---------------------------
def main():
    """This is the main CLI entry point."""
    main_db = connect_main_db()
    food_db = connect_food_db()
    current_user = get_or_create_user(main_db)
    refresh_user_logs_from_db(main_db, current_user)
    cli_menu(main_db, food_db, current_user)
