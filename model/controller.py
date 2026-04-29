# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""CLI controller functions for SEDA."""

import sys
from dataclasses import fields
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# pylint: disable=C0413, E1120, C0301

import ui.cli_view
from model.class_user import User
from model.classes_food import BigSeven, Food, Meal, NutrientSummary
from model.classes_log import ActivityLog, MealLog, WaterLog, WeightLog
from model.database import Database, FoodDatabase


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


def create_water_log_instances_for_user(main_db: Database, user_id):
    """Create an array of WaterLog instances for the user."""
    return [
        WaterLog(
            log[0], log[1], log[2], log[3]
        )  # log[0] is id, log[1] is user_id, log[2] is amount_in_ml, log[3] is timestamp. Refactored by ai.
        for log in main_db.get_all_water_logs()  # pylint: disable=no-value-for-parameter
        if log[1] == user_id
    ]  # refactored by ai


def create_weight_log_instances_for_user(main_db: Database, user_id):
    """Create an array of WeightLog instances for the user."""
    return [
        WeightLog(
            log[0], log[1], log[2], log[3], log[4]
        )  # log[0] is id, log[1] is user_id, log[2] is weight_in_kg, log[3] is height_in_cm, log[4] is timestamp. Refactored by ai.
        for log in main_db.get_all_weight_logs()  # pylint: disable=no-value-for-parameter
        if log[1] == user_id
    ]  # refactored by ai


def create_activity_log_instances_for_user(main_db: Database, user_id):
    """Create an array of ActivityLog instances for the user."""
    return [
        ActivityLog(
            log[0], log[1], log[2], log[3], log[4], log[5], log[6]
        )  # log[0] is id, log[1] is user_id, log[2] is activity_name, log[3] is calories_burned, log[4] is activity_value, log[5] is unit_type, log[6] is timestamp. Refactored by ai.
        for log in main_db.get_all_activity_logs()  # pylint: disable=no-value-for-parameter
        if log[1] == user_id
    ]  # refactored by ai


def create_nutrient_summary_with_defaults(**overrides):
    """Create a nutrient summary with None defaults. ai-generated."""
    # fields(...) reads all dataclass attributes so we can build a complete summary shape.
    values = {field.name: None for field in fields(NutrientSummary)}
    values.update(overrides)
    return NutrientSummary(**values)


def create_food_instance_from_food_row(food_row, amount):
    """Create a Food instance from an external food DB row. ai-generated."""
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
    """Create a Food instance from a meal item DB row. ai-generated."""
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
    """Create a Meal instance with its food items from DB data. ai-generated."""
    food_items = [
        create_food_instance_from_meal_item_row(item_row)
        for item_row in main_db.get_meal_food_items(
            meal_row[0]
        )  # pylint: disable=no-value-for-parameter
    ]
    return Meal(meal_row[0], meal_row[1], food_items)


def create_meal_instances(main_db: Database):
    """Create Meal instances for all stored meal templates. ai-generated."""
    return [
        create_meal_instance_from_db(main_db, meal_row)
        for meal_row in main_db.get_all_meals()  # pylint: disable=no-value-for-parameter
    ]


def create_meal_log_instances_for_user(main_db: Database, user_id):
    """Create an array of MealLog instances for the user."""
    return [
        MealLog(
            log[0],
            log[1],
            create_meal_instance_from_db(main_db, (log[2], log[3])),
            log[4],
            log[5],
            log[6],
        )  # log[0] is meal_log_id, log[1] is user_id, log[2] is meal_id, log[3] is meal_name, log[4] is amount, log[5] is unit_type, log[6] is timestamp. Refactored by ai.
        for log in main_db.get_user_meal_logs(
            user_id
        )  # pylint: disable=no-value-for-parameter
    ]  # refactored by ai


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


def refresh_water_logs_from_db(main_db: Database, user: User):
    """Refresh the water logs from DB into the current user object."""
    user.water_log_handler.logs = create_water_log_instances_for_user(
        main_db, user.user_id
    )  # refactored by ai


def refresh_weight_logs_from_db(main_db: Database, user: User):
    """Refresh the weight logs from DB into the current user object."""
    user.weight_log_handler.logs = create_weight_log_instances_for_user(
        main_db, user.user_id
    )  # refactored by ai


def refresh_meal_logs_from_db(main_db: Database, user: User):
    """Refresh the meal logs from DB into the current user object."""
    user.meal_log_handler.logs = create_meal_log_instances_for_user(
        main_db, user.user_id
    )  # refactored by ai


def refresh_activity_logs_from_db(main_db: Database, user: User):
    """Refresh the activity logs from DB into the current user object."""
    user.activity_log_handler.logs = create_activity_log_instances_for_user(
        main_db, user.user_id
    )  # refactored by ai


def refresh_user_logs_from_db(main_db: Database, user: User):
    """Refresh all log handlers of the current user from DB."""
    refresh_water_logs_from_db(main_db, user)
    refresh_weight_logs_from_db(main_db, user)
    refresh_meal_logs_from_db(main_db, user)
    refresh_activity_logs_from_db(main_db, user)


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
    )  # refactored by ai
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


def search_foods(food_db: FoodDatabase):
    """Search foods in the external food database and display results. ai-generated."""
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
    """Choose one food from search results. ai-generated."""
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
    """Collect food items for a meal template from food search results. ai-generated."""
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
    """Create a meal template from searched foods. ai-generated."""
    meal_name = ui.cli_view.prompt_meal_name()
    if not meal_name:
        ui.cli_view.show_message("Meal creation aborted.")
        return None

    meal_id = main_db.add_meal(meal_name)  # pylint: disable=no-value-for-parameter
    meal = Meal(meal_id, meal_name, [])  # ai-generated

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


def create_single_food_meal(main_db: Database, food_row):
    """Create a one-food meal object for direct logging. ai-generated."""
    meal_name = food_row["name_de"] or food_row["name_en"]
    meal_id = main_db.add_meal(meal_name)  # pylint: disable=no-value-for-parameter
    # Food DB values are stored per 100 units, so the helper meal uses 100 g/ml as its base.
    food_item = create_food_instance_from_food_row(food_row, 100)
    main_db.add_meal_food_item(
        meal_id, food_item.id, food_item.amount, food_item.unit_type
    )  # pylint: disable=no-value-for-parameter
    return Meal(meal_id, meal_name, [food_item])


def update_meal_template(main_db: Database, food_db: FoodDatabase):
    """Update a meal template name and optionally rebuild its foods. ai-generated."""
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
    """Show all meal templates. ai-generated."""
    meals = create_meal_instances(main_db)
    ui.cli_view.show_meal_templates(meals)


def delete_meal_template(main_db: Database):
    """Delete one meal template. ai-generated."""
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


def add_meal_log(main_db: Database, user: User):
    """Log a consumed meal for the current user. ai-generated."""
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
    )  # ai-generated
    db_id = main_db.add_meal_log(
        user.user_id, selected_meal.id, amount, unit_type, new_log.timestamp
    )  # pylint: disable=no-value-for-parameter
    new_log.set_database_id(db_id)
    ui.cli_view.show_message("\nMeal log added successfully.\n")


def add_single_food_log(main_db: Database, food_db: FoodDatabase, user: User):
    """Log one searched food directly without manual meal-template creation. ai-generated."""
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
    )  # ai-generated
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
    """Update one meal log in object state and DB. ai-generated."""
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
    """Show all meal logs of the user. ai-generated."""
    ui.cli_view.show_meal_logs(user.meal_log_handler.logs)


def delete_meal_log(main_db: Database, user: User):
    """Delete one meal log from DB and object state. ai-generated."""
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


def get_today_water_status(user: User):
    """Return today's water status as plain data. ai-generated."""
    # Returning plain data keeps the controller easy to call from CLI now and Flet later.
    return {
        "intake": user.water_log_handler.water_intake_today(),
        "target": user.daily_water_target,
        "difference": user.today_water_balance,
        "progress": user.today_water_progress,
    }


def show_today_water_status(user: User):
    """Show today's water status. ai-generated."""
    ui.cli_view.show_water_status(get_today_water_status(user))


def get_today_calorie_status(user: User):
    """Return today's calorie status as plain data. ai-generated."""
    intake = user.today_calorie_intake
    burned = user.today_calories_burned
    net = user.today_net_calories
    target = user.daily_calorie_target
    difference = None if target is None else round(target - net, 2)
    return {
        "intake": intake,
        "burned": burned,
        "net": net,
        "target": target,
        "difference": difference,
    }


def show_today_calorie_status(user: User):
    """Show the current calorie status of today. ai-generated."""
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


def add_activity_log(main_db: Database, user: User):
    """Add an activity log to the user and persist it. ai-generated."""
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
    )  # ai-generated
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
    """Show all activity logs of the user. ai-generated."""
    ui.cli_view.show_activity_logs(user.activity_log_handler.logs)


def update_activity_log(main_db: Database, user: User):
    """Update one activity log in object state and DB. ai-generated."""
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
    """Delete one activity log from DB and object state. ai-generated."""
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


def delete_current_user(main_db: Database, user: User):
    """Delete the current user and return the next active user. ai-generated."""
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
    """Run the meal and calorie CLI menu. ai-generated."""
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
    """Run the activity log CLI menu. ai-generated."""
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


def main():
    """This is the main CLI entry point."""
    main_db = connect_main_db()
    food_db = connect_food_db()
    current_user = get_or_create_user(main_db)
    refresh_user_logs_from_db(main_db, current_user)
    cli_menu(main_db, food_db, current_user)
