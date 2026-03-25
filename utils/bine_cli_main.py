"""This module contains the cli controller functions for SEDA."""
# still needs some fixing on other files to work properly, but the general structure is there.

import sys
from pathlib import Path
from time import sleep
from datetime import datetime

# Path-correction
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.classes import User, WaterLog, WeightLog
from model.database import Database
import ui.cli_view

# function to convert DB user row to User object (added by Bine) 
def get_current_user_object(db_user_row):
    """function to convert DB user row to User object."""
    if not db_user_row:
        return None
    
    return User(
        user_id=db_user_row[0],
        name=db_user_row[1],
        birthdate=db_user_row[2],
        height_in_cm=db_user_row[3],
        gender=db_user_row[4],
        fitness_lvl=db_user_row[5],
        water=[], weight=[], food=[], meal=[] # starts off empty and will be filled as needed
    )


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

# --- USER INITIALIZATION ---
all_users_raw = db.get_all_users() # pylint: disable=no-value-for-parameter
#all_users_raw = represents a list of tuples representing the users in the database. Each tuple contains the raw data for a user, such as (user_id, name, birthdate, etc)

if not all_users_raw:
    ui.cli_view.show_message("No users found. Let's create a new user.")
    temp_user = ui.cli_view.create_user_by_input()
    db.add_user(temp_user.name, temp_user.birthdate, temp_user.height_in_cm, temp_user.gender, temp_user.fitness_lvl) # pylint: disable=no-value-for-parameter, disable=line-too-long
    all_users_raw = db.get_all_users() # Refresh the user list after adding the new user

current_user = get_current_user_object(all_users_raw[0]) # Assuming we take the first user for now; can be expanded to allow user selection

ui.cli_view.show_message(f"Logged in as: {current_user.name} (ID: {current_user.user_id})")


while True:
    choice = ui.cli_view.prompt_main_menu()

    if choice == "1":
        ui.cli_view.show_user_info(current_user) #retrieving data from the current user object
                                     
    elif choice == "2":
        # Add a water log -- amended by Bine
        amount_in_ml, timestamp = ui.cli_view.create_water_log_by_input()
        water_log_1 = current_user.add_water_log(amount_in_ml, timestamp)
        db_id = db.add_water_log(current_user.user_id, water_log_1.amount_in_ml, water_log_1.timestamp)
        water_log_1.id = db_id
        ui.cli_view.show_message("Water log added successfully.")
    elif choice == "3":
        # Show water logs -- amended by Bine
        current_user.show_water_logs()
        water_logs = db.get_all_water_logs() # pylint: disable=no-value-for-parameter
        ui.cli_view.show_water_logs(water_logs)
    elif choice == "4": # -- added by Bine
        # Add a weight log
        weight_in_kg, timestamp = ui.cli_view.create_weight_log_by_input() #zum Abfragen der Daten über die CLI View
        weight_log_1 = current_user.add_weight_log(weight_in_kg, timestamp)
        db_id = db.add_weight_log(current_user.user_id, weight_log_1.weight_in_kg, weight_log_1.timestamp)
        weight_log_1.id = db_id # Update the log with the DB-assigned ID
        ui.cli_view.show_message("Weight log added successfully.")
    elif choice == "5": # -- added by Bine
        # Show weight logs
        raw_logs = db.get_all_weight_logs() # pylint: disable=no-value-for-parameter
        user_logs_raw = [log for log in raw_logs if log[1] == current_user.user_id] # Filter logs for the current user
        weight_log_objects = [WeightLog(id=log[0], weight_in_kg=log[3], timestamp=log[4]) for log in user_logs_raw] # Convert raw logs to WeightLog objects
        ui.cli_view.show_weight_logs(weight_log_objects)
    elif choice == "6":
        # Exit the program
        ui.cli_view.show_message("Exiting SEDA. Goodbye!")
        break
    elif choice == "7": # -- added by Bine
        # Delete a weight log
        raw_logs = db.get_all_weight_logs() # pylint: disable=no-value-for-parameter
        user_logs_raw = [log for log in raw_logs if log[1] == current_user.user_id] # Filter logs for the current user
        weight_log_objects = [WeightLog(id=log[0], weight_in_kg=log[3], timestamp=log[4]) for log in user_logs_raw] # Convert raw logs to WeightLog objects
        ui.cli_view.show_weight_logs(weight_log_objects)
        if weight_log_objects:
            log_id_to_delete = int(input("Enter the ID of the weight log you want to delete: "))
            db.delete_weight_log(log_id_to_delete) # pylint: disable=no-value-for-parameter
            current_user.delete_weight_log(log_id_to_delete) # deleting from the local object as well
            ui.cli_view.show_message("Weight log deleted successfully.")
        else:
            ui.cli_view.show_message("Nothing to delete.")
    elif choice == "8": # -- added by Bine
        # Change user information
        ui.cli_view.show_message("Let's update your user information.")
        updated_data = ui.cli_view.create_user_by_input() # temporary variable to hold the updated data
        current_user.update_biometrical_data(
            birthdate=updated_data.birthdate,
            height_in_cm=updated_data.height_in_cm,
            gender=updated_data.gender,
            fitness_lvl=updated_data.fitness_lvl
        )
        current_user.name = updated_data.name 
        pass # Here we would also need to update the database with the new user information, which would require a new method in the Database class (not implemented here yet)
    elif choice == "9":
        # Exit the program
        ui.cli_view.show_message("Exiting SEDA. Goodbye!")
        break
    else:
        ui.cli_view.show_message("Invalid choice. Please enter a number between 1 and 6.")
