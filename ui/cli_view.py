"""This module contains the cli view functions for SEDA."""

import sys
from pathlib import Path
from datetime import datetime
from model.classes import User
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def show_message(message):
    """Print a message to the console."""
    print(message)

def prompt_log_id():
    """Prompt User for a log ID and return it. If input is invalid, return None."""
    try:
        log_id = int(input("Enter the log ID: "))
        return log_id
    except ValueError:
        print("Invalid input. Please enter a valid log ID." \
        "\nReturning to the previous menu.")
        return None

# User related functions

def create_user_by_input():
    """Create a new user by asking for input. Partly AI-generated."""
    while True:
        name = input("Enter your name: ")
        if name.strip(): # strip removes leading and trailing whitespaces.
            break
        print("Name cannot be empty. Please enter a valid name.")
    while True:
        birthdate = input("Enter your birthdate (YYYY-MM-DD): ")
        if (birthdate.strip() and
            "1900-01-01" <= birthdate <= (datetime.now().replace(year=datetime.now().year - 6)).strftime("%Y-%m-%d")
        ):
            break
        print("Birthdate must be in the format YYYY-MM-DD and between 1900-01-01 and 6 years ago. Please enter a valid birthdate.")
    while True:
        try:
            height_in_cm = int(input("Enter your height in cm: "))
            if height_in_cm <= 0 or height_in_cm > 250:
                raise ValueError("Height must be between 1 and 250 cm.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}")
    while True:
        gender = input("Enter your gender (m/f/d): ")
        # ai generated. strip removes leading and trailing whitespaces.
        # The intersection checks if the input is one of the valid options.
        if gender.strip() and {'m', 'f', 'd'}.intersection({gender.lower()}): 
            break
        print("Gender must be 'm', 'f', or 'd'. Please enter a valid gender.")
    while True:
        fitness_lvl = input("Enter your fitness level (beginner/intermediate/advanced): ")
        if fitness_lvl.strip() and {'beginner', 'intermediate', 'advanced'}.intersection({fitness_lvl.lower()}):
            break
        print("Fitness level must be 'beginner', 'intermediate', or 'advanced'. Please enter a valid fitness level.")
    return User(None, name, birthdate, height_in_cm, gender, fitness_lvl, [], [], [], [])

def show_user_info_from_class(user):
    """Show the user's information."""
    print("User Information:")
    print(f"Name: {user.name}")
    print(f"Birthdate: {user.birthdate}")
    print(f"Height: {user.height_in_cm} cm")
    print(f"Gender: {user.gender}")
    print(f"Fitness level: {user.fitness_lvl}")

def change_user_information(user):
    """Change the user's information by asking for input."""
    print("Change User Information. If you want to keep the current value, just press Enter.")
    name = input(f"Enter your name. Currently: ({user.name}): ") or user.name
    birthdate = input(f"Enter your birthdate (YYYY-MM-DD). Currently: ({user.birthdate}): ") or user.birthdate
    height_in_cm_input = input(f"Enter your height in cm. Currently: ({user.height_in_cm}): ") or str(user.height_in_cm)
    try:
        height_in_cm = int(height_in_cm_input)    
    except ValueError:
        print("Invalid input for height. Keeping the current value.")
        height_in_cm = user.height_in_cm
    gender = input(f"Enter your gender (m/f/d). Currently: ({user.gender}): ") or user.gender
    fitness_lvl = input(f"Enter your fitness level (beginner/intermediate/advanced). Currently: ({user.fitness_lvl}): ") or user.fitness_lvl
    return name, birthdate, height_in_cm, gender, fitness_lvl


# Water log related functions

def create_water_log_parameters_by_input():
    """Create new water log parameters by asking for input."""
    while True:
        try:
            amount_in_ml = int(input("Enter the amount of water in ml: "))
        except ValueError:
            print("Invalid input. Please enter a valid amount between 1 and 2000 ml.")
        try:
            if amount_in_ml < 1 or amount_in_ml > 2000 or not isinstance(amount_in_ml, int):
                raise ValueError("Amount must be between 1 and 2000 ml.")
            break
        except ValueError as e:
            print(e)
    while True:
        try:
            timestamp = input("Enter the timestamp (YYYY-MM-DDTHH:MM) or nothing for current time: ")
            break
        except ValueError as e:
            print(f"Invalid input: {e}")
    if not timestamp:
        timestamp = None
    return amount_in_ml, timestamp

def show_water_logs_from_db(water_logs):
    """Show all water logs."""
    if not water_logs:
        print("No water logs found.")
        return
    for log in water_logs:
        print(f"ID: {log.id}, Amount: {log.amount_in_ml} ml, Timestamp: {log.timestamp}")


# Weight log related functions

def create_weight_log_by_input():
    """Create a new weight log by asking for input."""
    while True:
        try:
            weight_in_kg = float(input("Enter your weight in kg: "))
            if weight_in_kg < 5 or weight_in_kg > 300:
                raise ValueError("Weight must be between 5 and 300 kg.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}")
    while True:
        try:
            timestamp = input("Enter the timestamp (YYYY-MM-DDTHH:MM) or nothing for current time: ")
            break
        except ValueError as e:
            print(f"Invalid input: {e}")
    if not timestamp:
        timestamp = None
    return weight_in_kg, timestamp

def show_weight_logs(weight_logs):
    """Show all weight logs."""
    if not weight_logs:
        print("No weight logs found.")
        return
    for log in weight_logs:
        print(f"ID: {log.id}, Weight: {log.weight_in_kg} kg, Timestamp: {log.timestamp}")


def prompt_main_menu():
    """Show the main menu and handle user input."""
    show_message("""
        What would you like to do?
        1. Show user information
        2. All about water logs:
        3. All about weight logs:
        4. Change user information
        5. Exit
                                """)
    return input("Enter your choice (1-5): ")

def prompt_water_log_menu():
    """Show the water log menu and handle user input."""
    show_message("""
        What would you like to do with your water logs?
        1. Add a water log
        2. Show all water logs
        3. Delete a water log
        4. Back to main menu
                                """)
    return input("Enter your choice (1-4): ")

def prompt_weight_log_menu():
    """Show the weight log menu and handle user input."""
    show_message("""
        What would you like to do with your weight logs?
        1. Add a weight log
        2. Show all weight logs
        3. Delete a weight log
        4. Back to main menu
                                """)
    return input("Enter your choice (1-4): ")