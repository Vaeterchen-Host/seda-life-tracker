# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""CLI controller functions for SEDA."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# pylint: disable=C0413, E1120, C0301

import ui.cli_view
from model.class_user import User
from model.database import Database, FoodDatabase

main_db = Database()
food_db = FoodDatabase()
initial_user = None

ui.cli_view.show_welcome()
db_connection = main_db.connect()
# sleep(2)
ui.cli_view.show_message("Connect with Database...")

if db_connection is None:
    ui.cli_view.show_message("Failed to connect to the database. Exiting.")
    sys.exit(1)
ui.cli_view.show_message("Connected with Database.")

if not main_db.get_all_users():  # pylint: disable=no-value-for-parameter
    ui.cli_view.show_message("No users found. Let's create a new user.")
    initial_user = ui.cli_view.create_user_by_input()
    try:
        main_db.add_user(
            initial_user.name,
            initial_user.birthdate,
            initial_user.height_in_cm,
            initial_user.gender,
            initial_user.fitness_lvl,
        )  # pylint: disable=no-value-for-parameter, disable=line-too-long
    except Exception as e:  # pylint: disable=broad-exception-caught
        ui.cli_view.show_message(f"An error occurred while adding the user: {e}")

else:
    ui.cli_view.show_message("Existing user found:")
    users = main_db.get_all_users()  # pylint: disable=no-value-for-parameter
    for db_user in users:
        ui.cli_view.show_message(f"""
            ID: {db_user[0]}
            Name: {db_user[1]}
            Birthdate: {db_user[2]}
            Height: {db_user[3]} cm
            Gender: {db_user[4]}
            Fitness level: {db_user[5]}
        """)


# Create an array of WaterLog instances for the user
def create_water_log_instances_for_user():
    """Create an array of WaterLog instances for the user. Partly AI-generated."""
    water_logs = []
    for log in main_db.get_all_water_logs():  # pylint: disable=no-value-for-parameter
        water_log_instance = WaterLog(
            log[0], log[1], log[2], log[3]
        )  # Assuming log[0] is id, log[1] is user_id, log[2] is amount_in_ml, log[3] is timestamp.
        water_logs.append(water_log_instance)
    return water_logs


# Create an array of WeightLog instances for the user
def create_weight_log_instances_for_user():
    """Create an array of WeightLog instances for the user. Partly AI-generated."""
    weight_logs = []
    for log in main_db.get_all_weight_logs():  # pylint: disable=no-value-for-parameter
        weight_log_instance = WeightLog(
            log[0], log[1], log[2], log[3]
        )  # Assuming log[0] is id, log[1] is user_id, log[2] is weight_in_kg, log[3] is timestamp.
        weight_logs.append(weight_log_instance)
    return weight_logs


# Create User class instance from database data
def create_user_instance_from_db():
    """Create a User class instance from database data."""
    water_logs = create_water_log_instances_for_user()
    weight_logs = create_weight_log_instances_for_user()
    function_class_user = User(
        db_user[0],  # id
        db_user[1],  # name
        db_user[2],  # birthdate
        db_user[3],  # height_in_cm
        db_user[4],  # gender
        db_user[5],  # fitness_lvl
        water_logs,  # water_logs
        weight_logs,  # weight_logs
        [],  # sleep_logs
        [],  # activity_logs
    )
    return function_class_user


# Create the user instance for the class
if not initial_user:
    class_user = create_user_instance_from_db()
else:
    class_user = initial_user

# Refresher functions
# def refresh_user_data_from_db():
#     """This function refreshes the user data from DB."""
#     global class_user # global is needed to modify the class_user variable defined outside of this function
#     class_user = create_user_instance_from_db()


def refresh_water_logs_from_db():
    """This function refreshes the water logs from DB."""
    class_user.water_logs = create_water_log_instances_for_user()


def refresh_weight_logs_from_db():
    """This function refreshes the weight logs from DB."""
    class_user.weight_logs = create_weight_log_instances_for_user()


# User related functions
def show_user_information():
    """This function shows the user's information."""
    ui.cli_view.show_user_info_from_class(class_user)


def update_biometrical_information():
    """This function changes the user's information."""
    name, birthdate, height_in_cm, gender, fitness_lvl = (
        ui.cli_view.change_user_information(class_user)
    )  # pylint: disable=E1111
    class_user.name = name
    class_user.update_biometrical_data(
        birthdate=birthdate,
        height_in_cm=height_in_cm,
        gender=gender,
        fitness_lvl=fitness_lvl,
    )
    main_db.update_user(
        class_user.id, class_user.name, birthdate, height_in_cm, gender, fitness_lvl
    )  # pylint: disable=no-value-for-parameter, disable=line-too-long
    print("\nUser information updated successfully!\n")
    show_user_information()


# waterlog functions
def add_water_log():
    """This function adds a water log to the user."""
    amount_in_ml, timestamp = ui.cli_view.create_water_log_parameters_by_input()
    class_user.add_water_log(amount_in_ml, timestamp)
    water_log_for_db = class_user.water_logs[-1]  # Get the last added water log
    main_db.add_water_log(
        class_user.id, water_log_for_db.amount_in_ml, water_log_for_db.timestamp
    )  # pylint: disable=no-value-for-parameter, disable=line-too-long
    refresh_water_logs_from_db()
    ui.cli_view.show_message("\nWater log added successfully!\n")
    class_user.show_water_logs()  # pylint: disable=E1111, disable=E1101


def show_water_logs():
    """This function shows all water logs of the user."""
    class_user.show_water_logs()  # pylint: disable=E1111, disable=E1101


def delete_water_log():
    """This function deletes a waterlog from the user_class and the DB."""
    class_user.show_water_logs()  # pylint: disable=E1111, disable=E1101
    water_log_id = ui.cli_view.prompt_log_id()
    if water_log_id is None:
        return
    if water_log_id not in [log.id for log in class_user.water_logs]:
        return ui.cli_view.show_message("Log not found. Please enter a valid log ID.")
    main_db.delete_water_log(water_log_id)  # pylint: disable=no-value-for-parameter
    refresh_water_logs_from_db()
    ui.cli_view.show_message("\nWater log deleted successfully!\n")
    class_user.show_water_logs()  # pylint: disable=E1111, disable=E


# weight log functions
def add_weight_log():
    """This function adds a weight log to the user."""
    weight_in_kg, timestamp = ui.cli_view.create_weight_log_by_input()
    class_user.add_weight_log(weight_in_kg, timestamp)  # pylint: disable=E1111
    weight_log_for_db = class_user.weight_logs[-1]  # Get the last added weight log
    main_db.add_weight_log(
        class_user.id, weight_log_for_db.weight_in_kg, weight_log_for_db.timestamp
    )  # pylint: disable=no-value-for-parameter, disable=line-too-long
    refresh_weight_logs_from_db()
    ui.cli_view.show_message("\nWeight log added successfully!\n")
    class_user.show_weight_logs()  # pylint: disable=E1111, disable=E1101


def show_weight_logs():
    """This function shows all weight logs of the user."""
    class_user.show_weight_logs()  # pylint: disable=E1111, disable=E1101


def delete_weight_log():
    """This function deletes a weightlog from the user_class and the DB."""
    class_user.show_weight_logs()  # pylint: disable=E1111, disable=E1101
    weight_log_id = ui.cli_view.prompt_log_id()
    if weight_log_id is None:
        return
    if weight_log_id not in [log.id for log in class_user.weight_logs]:
        return ui.cli_view.show_message("Log not found. Please enter a valid log ID.")
    main_db.delete_weight_log(weight_log_id)  # pylint: disable=no-value-for-parameter
    refresh_weight_logs_from_db()
    ui.cli_view.show_message("\nWeight log deleted successfully!\n")
    class_user.show_weight_logs()  # pylint: disable=E1111, disable=E1101


# --------- Main menu loop - --------

while True:
    choice = ui.cli_view.prompt_main_menu().lower()
    if choice == "1":
        ui.cli_view.show_user_info_from_class(class_user)  # pylint: disable=E1111
    elif choice == "2":
        while True:
            water_log_choice = ui.cli_view.prompt_water_log_menu()
            if water_log_choice == "1":
                add_water_log()
            elif water_log_choice == "2":
                show_water_logs()
            elif water_log_choice == "3":
                delete_water_log()
            elif water_log_choice == "4":
                ui.cli_view.show_message(
                    f"\nToday's water intake: {class_user.water_intake_today()} ml\n"
                )
            elif water_log_choice == "5":
                break
            else:
                ui.cli_view.show_message("Invalid choice. Please try again.")
    elif choice == "3":
        while True:
            weight_log_choice = ui.cli_view.prompt_weight_log_menu()
            if weight_log_choice == "1":
                add_weight_log()
            elif weight_log_choice == "2":
                show_weight_logs()
            elif weight_log_choice == "3":
                delete_weight_log()
            elif weight_log_choice == "4":
                ui.cli_view.show_message(f"\nBMI: {class_user.calculate_bmi()}\n")
            elif weight_log_choice == "5":
                break
            else:
                ui.cli_view.show_message("Invalid choice. Please try again.")
    elif choice == "4":
        update_biometrical_information()
    elif choice == "5":
        ui.cli_view.show_message("Exiting the program. Goodbye!")
        main_db.end_connection(db_connection)  # pylint: disable=no-value-for-parameter
        sys.exit(0)
    elif choice == "l":
        ui.cli_view.show_license_long()
    else:
        ui.cli_view.show_message("Invalid choice. Please try again.")
