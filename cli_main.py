"""This module contains the cli controller functions for SEDA."""

from email import message

from model.classes import User, WaterLog, WeightLog
from model.database import Database
import ui.cli_view

import sys
from pathlib import Path
from time import sleep
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))




db = Database()

ui.cli_view.show_message("""
    Welcome to SEDA - Your personal fitness assistant!
    Please follow the prompts.
                            """)
db_connection = db.connect()
sleep(2)
ui.cli_view.show_message("Connect with Database...")

if db_connection is None:
    ui.cli_view.show_message("Failed to connect to the database. Exiting.")
    sys.exit(1)
ui.cli_view.show_message("Connected with Database.")

if not db.get_all_users(): # pylint: disable=no-value-for-parameter
    ui.cli_view.show_message("No users found. Let's create a new user.")
    user = ui.cli_view.create_user_by_input()
    try:
        db.add_user(user.name, user.birthdate, user.height_in_cm, user.gender, user.fitness_lvl) # pylint: disable=no-value-for-parameter, disable=line-too-long
    except Exception as e:
        ui.cli_view.show_message(f"An error occurred while adding the user: {e}")

else:
    ui.cli_view.show_message("Existing user found:")
    users = db.get_all_users() # pylint: disable=no-value-for-parameter
    for user in users:
        ui.cli_view.show_message(f"""
            ID: {user[0]}
            Name: {user[1]}
            Birthdate: {user[2]}
            Height: {user[3]} cm
            Gender: {user[4]}
            Fitness level: {user[5]}
        """)



while True:
    choice = ui.cli_view.prompt_main_menu()
    if choice == "1":
        for user in users:
            ui.cli_view.show_message(f"""
            User Information:
            ID: {user[0]}
            Name: {user[1]}
            Birthdate: {user[2]}
            Height: {user[3]} cm
            Gender: {user[4]}
            Fitness level: {user[5]}
        """)
    elif choice == "2":
        # Add a water log
        amount_in_ml, timestamp = ui.cli_view.create_water_log_by_input()
        water_log_1 = user.add_water_log(amount_in_ml, timestamp)
        db.add_water_log(user[0], water_log_1.amount_in_ml, water_log_1.timestamp) # pylint: disable=no-value-for-parameter, disable=line-too-long
    elif choice == "3":
        # Show water logs
        user.show_water_logs()
        water_logs = db.get_all_water_logs() # pylint: disable=no-value-for-parameter
        ui.cli_view.show_water_logs(water_logs)
        pass
    elif choice == "4":
        # Add a weight log
        pass
    elif choice == "5":
        # Show weight logs
        pass
    elif choice == "6":
        # Exit the program
        ui.cli_view.show_message("Exiting SEDA. Goodbye!")
        break
    elif choice == "7":
        # Delete a weight log
        pass
    elif choice == "8":
        # Change user information
        pass
    elif choice == "9":
        # Exit the program
        ui.cli_view.show_message("Exiting SEDA. Goodbye!")
        break
    else:
        ui.cli_view.show_message("Invalid choice. Please enter a number between 1 and 6.")
