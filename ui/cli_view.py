# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""CLI view functions for SEDA."""


import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# pylint: disable=C0413, E1120, C0301
from datetime import datetime
from config import DEVS, LICENSE_PATH
from model.classes import User
from model.database import FoodDatabase
from utils.paginator import paginator

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Type example german food query.
# Just for testing. Must be deleted.
FOOD = "Rinderfilet"


def show_message(message):
    """Print a message to the console."""
    print(message)


def prompt_log_id():
    """Prompt User for a log ID and return it. If input is invalid, return None."""
    try:
        log_id = int(input("Enter the log ID: "))
        return log_id
    except ValueError:
        print(
            "Invalid input. Please enter a valid log ID."
            "\nReturning to the previous menu."
        )
        return None


def show_welcome():
    """Show a short license notice."""
    show_message(
        f"""
        Welcome to SEDA - Your personal fitness assistant!

                seda  Copyright (C) 2026  {DEVS}
        This program comes with ABSOLUTELY NO WARRANTY.
        This is free software, and you are welcome to redistribute it
        under certain conditions.
        Type "l" for details.\n
                 """
    )


def show_license_long():
    """Show the project license text. AI-generated content."""
    if not LICENSE_PATH.exists():
        print("LICENSE.md not found.")
        return

    paginator(LICENSE_PATH.read_text(encoding="utf-8"))  # pylint: disable=E1121


# User related functions


def create_user_by_input():
    """Create a new user by asking for input. Partly AI-generated."""
    while True:
        name = input("Enter your name: ")
        if name.strip():  # strip removes leading and trailing whitespaces.
            break
        print("Name cannot be empty. Please enter a valid name.")
    while True:
        birthdate = input("Enter your birthdate (YYYY-MM-DD): ")
        if birthdate.strip() and "1900-01-01" <= birthdate <= (
            datetime.now().replace(year=datetime.now().year - 6)
        ).strftime("%Y-%m-%d"):
            break
        print(
            "Birthdate must be in the format YYYY-MM-DD and between 1900-01-01 and 6 years ago. Please enter a valid birthdate."
        )
    while True:
        try:
            height_in_cm = int(input("Enter your height in cm: "))
            if height_in_cm <= 50 or height_in_cm > 250:
                raise ValueError("Height must be between 50 and 250 cm.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}" + "\nPlease enter a valid height in cm.")
    while True:
        gender = input("Enter your gender (m/f/d): ")
        # ai generated. strip removes leading and trailing whitespaces.
        # The intersection checks if the input is one of the valid options.
        if gender.strip() and {"m", "f", "d"}.intersection({gender.lower()}):
            break
        print("Gender must be 'm', 'f', or 'd'. Please enter a valid gender.")
    while True:
        fitness_lvl = input(
            "Enter your fitness level (beginner/intermediate/advanced): "
        )
        if fitness_lvl.strip() and {
            "beginner",
            "intermediate",
            "advanced",
        }.intersection({fitness_lvl.lower()}):
            break
        print(
            "Fitness level must be 'beginner', 'intermediate', or 'advanced'. Please enter a valid fitness level."
        )
    return User(
        None, name, birthdate, height_in_cm, gender, fitness_lvl, [], [], [], [], []
    )


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
    print(
        "Change User Information. If you want to keep the current value, just press Enter."
    )
    name = input(f"Enter your name. Currently: ({user.name}): ") or user.name
    if not name.strip():
        print("Invalid input for name. Keeping the current value.")
        name = user.name
    try:
        birthdate = (
            input(f"Enter your birthdate (YYYY-MM-DD). Currently: ({user.birthdate}): ")
            or user.birthdate
        )
        datetime.strptime(birthdate, "%Y-%m-%d")  # Validate the date format
    except ValueError:
        print("Invalid input for birthdate. Keeping the current value.")
        birthdate = user.birthdate
    height_in_cm_input = input(
        f"Enter your height in cm. Currently: ({user.height_in_cm}): "
    ) or str(user.height_in_cm)
    try:
        height_in_cm = int(height_in_cm_input)
        if height_in_cm <= 50 or height_in_cm > 250:
            raise ValueError("Height must be between 50 and 250 cm.")
    except ValueError:
        print("Invalid input for height. Keeping the current value.")
        height_in_cm = user.height_in_cm
    gender = (
        input(f"Enter your gender (m/f/d). Currently: ({user.gender}): ") or user.gender
    )
    if not {"m", "f", "d"}.intersection({gender.lower()}):
        print("Invalid input for gender. Keeping the current value.")
        gender = user.gender

    fitness_lvl = (
        input(
            f"Enter your fitness level (beginner/intermediate/advanced). Currently: ({user.fitness_lvl}): "
        )
        or user.fitness_lvl
    )
    if not {"beginner", "intermediate", "advanced"}.intersection({fitness_lvl.lower()}):
        print("Invalid input for fitness level. Keeping the current value.")
        fitness_lvl = user.fitness_lvl
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
            if (
                amount_in_ml < 1
                or amount_in_ml > 2000
                or not isinstance(amount_in_ml, int)
            ):
                raise ValueError("Amount must be between 1 and 2000 ml.")
            break
        except ValueError as e:
            print(
                f"Invalid input: {e}"
                + "\nPlease enter a valid amount between 1 and 2000 ml."
            )
    while True:
        try:
            timestamp = input(
                "Enter the timestamp (YYYY-MM-DDTHH:MM) or nothing for current time: "
            )
            break
        except ValueError as e:
            print(
                f"Invalid input: {e}"
                + "\nPlease enter a valid timestamp in the format YYYY-MM-DDTHH:MM"
                " or leave it empty for the current time."
            )
    if not timestamp:
        timestamp = None
    return amount_in_ml, timestamp


def show_water_logs_from_db(water_logs):
    """Show all water logs."""
    if not water_logs:
        print("No water logs found.")
        return
    for log in water_logs:
        print(
            f"ID: {log.id}, Amount: {log.amount_in_ml} ml, Timestamp: {log.timestamp}"
        )


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
            timestamp = input(
                "Enter the timestamp (YYYY-MM-DDTHH:MM) or nothing for current time: "
            )
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
        print(
            f"ID: {log.id}, Weight: {log.weight_in_kg} kg, Timestamp: {log.timestamp}"
        )


def prompt_main_menu():
    """Show the main menu and handle user input."""
    show_message(
        """
        What would you like to do?
        1. Show user information
        2. All about water logs:
        3. All about weight log:
        4. Change user information
        5. Exit
        
        l. Show License
                                """
    )
    return input("Enter your choice (1-5/l): ")


def prompt_water_log_menu():
    """Show the water log menu and handle user input."""
    show_message(
        """
        What would you like to do with your water logs?
        1. Add a water log
        2. Show all water logs
        3. Delete a water log
        4. Show today's water intake
        5. Back to main menu
                                """
    )
    return input("Enter your choice (1-5): ")


def prompt_weight_log_menu():
    """Show the weight log menu and handle user input."""
    show_message(
        """
        What would you like to do with your weight logs?
        1. Add a weight log
        2. Show all weight logs
        3. Delete a weight log
        4. Calculate BMI.
        5. Back to main menu
                                """
    )
    return input("Enter your choice (1-5): ")


# Food-DB related functions
def example_query(food_name="Hafer"):
    """Example function. For testing and demonstration purposes.
    It queries the food database for a given food name.
    It must be deleted or replaced in the final version
    This function is ai-generated."""
    db = FoodDatabase()

    query = f"""
    SELECT *
    FROM foods
    WHERE name_de LIKE '%{food_name}%'
    LIMIT 1;
    """

    result = db.custom_sql_query(query)

    if not result:
        print("Nothing found. Maybe your food is too exotic.")
        return

    row = result[0]

    # fetch column names
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(foods);")
    columns = [col[1] for col in cursor.fetchall()]
    conn.close()

    data = dict(zip(columns, row))

    # --- Output ---
    print("\n" + "=" * 60)
    print(f"English: {data['name_en']}")
    print(f"German: {data['name_de']}")
    print(f"food_id: {data['food_id']}")
    print(f"BLS Code: {data['bls_code']}")
    print("=" * 60)

    # --- Macronutrients (per 100g) ---
    print("\n--- Macronutrients (per 100g) ---")
    print(f"Calories:              {data['kcal']} kcal")
    print(f"Protein:               {data['protein']} g")
    print(f"Fat:                   {data['fat']} g")
    print(f"  Saturated:           {data['saturated_fat']} g")
    print(f"  Monounsaturated:     {data['monounsaturated_fat']} g")
    print(f"  Polyunsaturated:     {data['polyunsaturated_fat']} g")
    print(f"Carbohydrates:         {data['carbohydrate']} g")
    print(f"  Sugar:               {data['sugar']} g")
    print(f"Fibre:                 {data['fibre']} g")

    # --- Minerals ---
    print("\n--- Minerals ---")
    print(f"Salt:                  {data['salt']} g")
    print(f"Sodium:                {data['sodium']} mg")
    print(f"Potassium:             {data['potassium']} mg")
    print(f"Calcium:               {data['calcium']} mg")
    print(f"Magnesium:             {data['magnesium']} mg")
    print(f"Iron:                  {data['iron']} mg")
    print(f"Zinc:                  {data['zinc']} mg")
    print(f"Iodine:                {data['iodine']} µg")

    # --- Vitamins ---
    print("\n--- Vitamins ---")
    print(f"Vitamin A:             {data['vitamin_a']} µg")
    print(f"Vitamin D:             {data['vitamin_d']} µg")
    print(f"Vitamin E:             {data['vitamin_e']} mg")
    print(f"Vitamin K:             {data['vitamin_k']} µg")
    print(f"Vitamin B1:            {data['vitamin_b1']} mg")
    print(f"Vitamin B2:            {data['vitamin_b2']} mg")
    print(f"Niacin:                {data['niacin']} mg")
    print(f"Vitamin B6:            {data['vitamin_b6']} µg")
    print(f"Folate:                {data['folate']} µg")
    print(f"Vitamin B12:           {data['vitamin_b12']} µg")
    print(f"Vitamin C:             {data['vitamin_c']} mg")

    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    example_query(FOOD)
