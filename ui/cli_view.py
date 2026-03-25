"""This module contains the cli view functions for SEDA."""

import sys
from pathlib import Path

from model.classes import User
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def show_message(message):
    """Print a message to the console."""
    print(message)

# User related functions

def create_user_by_input():
    """Create a new user by asking for input."""
    name = input("Enter your name: ")
    birthdate = input("Enter your birthdate (YYYY-MM-DD): ")
    height_in_cm = int(input("Enter your height in cm: "))
    gender = input("Enter your gender (m/f/d): ")
    fitness_lvl = input("Enter your fitness level (beginner/intermediate/advanced): ")
    return User(None, name, birthdate, height_in_cm, gender, fitness_lvl, [], [], [], [])

def show_user_info(user):
    """Show the user's information."""
    print("User Information:")
    print(f"Name: {user.name}")
    print(f"Birthdate: {user.birthdate}")
    print(f"Height: {user.height_in_cm} cm")
    print(f"Gender: {user.gender}")
    print(f"Fitness level: {user.fitness_lvl}")

# Water log related functions

def create_water_log_by_input():
    """Create a new water log by asking for input."""
    amount_in_ml = int(input("Enter the amount of water in ml: "))
    timestamp = input("Enter the timestamp (YYYY-MM-DDTHH:MM) or nothing: ")
    if not timestamp:
        timestamp = None
    return amount_in_ml, timestamp

def show_water_logs(water_logs):
    """Show all water logs."""
    if not water_logs:
        print("No water logs found.")
        return
    for log in water_logs:
        print(f"ID: {log.id}, Amount: {log.amount_in_ml} ml, Timestamp: {log.timestamp}")

# Weight log related functions

def create_weight_log_by_input():
    """Create a new weight log by asking for input."""
    weight_in_kg = float(input("Enter your weight in kg: "))
    timestamp = input("Enter the timestamp (YYYY-MM-DDTHH:MM) or nothing: ")
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
        2. Add a water log
        3. Show water logs
        4. Delete a water log
        5. Add a weight log
        6. Show weight logs
        7. Delete a weight log
        8. Change user information
        9. Exit
                                """)
    return input("Enter your choice (1-9): ")