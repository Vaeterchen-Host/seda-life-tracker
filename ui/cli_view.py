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
from model.database import FoodDatabase
from utils.paginator import paginator

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Type example german food query.
# Just for testing. Must be deleted.
FOOD = "Olivenöl"

FOOD_DISPLAY_SECTIONS = [  # ai-generated
    (
        "Energy and Basic Values (per 100g/ml)",
        [
            ("Calories:", "kcal", "kcal"),
            ("Water:", "water", "g"),
            ("Alcohol:", "alcohol", "g"),
            ("Salt:", "salt", "g"),
        ],
    ),
    (
        "Macronutrients (per 100g/ml)",
        [
            ("Protein:", "protein", "g"),
            ("Fat:", "fat", "g"),
            ("Saturated fat:", "saturated_fat", "g"),
            ("Monounsaturated:", "monounsaturated_fat", "g"),
            ("Polyunsaturated:", "polyunsaturated_fat", "g"),
            ("Omega-3:", "omega_3", "g"),
            ("Omega-6:", "omega_6", "g"),
            ("Carbohydrates:", "carbohydrate", "g"),
            ("Sugar:", "sugar", "g"),
            ("Starch:", "starch", "g"),
            ("Fibre:", "fibre", "g"),
        ],
    ),
    (
        "Other Nutrients",
        [
            ("Cholesterol:", "cholesterol", "mg"),
        ],
    ),
    (
        "Minerals",
        [
            ("Sodium:", "sodium", "mg"),
            ("Potassium:", "potassium", "mg"),
            ("Calcium:", "calcium", "mg"),
            ("Magnesium:", "magnesium", "mg"),
            ("Phosphorus:", "phosphorus", "mg"),
            ("Iron:", "iron", "mg"),
            ("Zinc:", "zinc", "mg"),
            ("Iodine:", "iodine", "µg"),
            ("Copper:", "copper", "µg"),
            ("Manganese:", "manganese", "µg"),
            ("Fluoride:", "fluoride", "µg"),
            ("Chromium:", "chromium", "µg"),
            ("Molybdenum:", "molybdenum", "µg"),
        ],
    ),
    (
        "Vitamins",
        [
            ("Vitamin A (RE):", "vitamin_a_re", "µg"),
            ("Vitamin A (RAE):", "vitamin_a_rae", "µg"),
            ("Retinol:", "retinol", "µg"),
            ("Beta-carotene:", "beta_carotene", "µg"),
            ("Vitamin D:", "vitamin_d", "µg"),
            ("Vitamin D2:", "vitamin_d2", "µg"),
            ("Vitamin D3:", "vitamin_d3", "µg"),
            ("Vitamin E:", "vitamin_e", "mg"),
            ("Alpha-tocopherol:", "alpha_tocopherol", "mg"),
            ("Vitamin K:", "vitamin_k", "µg"),
            ("Vitamin K1:", "vitamin_k1", "µg"),
            ("Vitamin K2:", "vitamin_k2", "µg"),
            ("Vitamin B1:", "vitamin_b1", "mg"),
            ("Vitamin B2:", "vitamin_b2", "mg"),
            ("Niacin:", "niacin", "mg"),
            ("Niacin equivalent:", "niacin_equivalent", "mg"),
            ("Pantothenic acid:", "pantothenic_acid", "mg"),
            ("Vitamin B6:", "vitamin_b6", "µg"),
            ("Biotin:", "biotin", "µg"),
            ("Folate equivalent:", "folate_equivalent", "µg"),
            ("Folate:", "folate", "µg"),
            ("Folic acid:", "folic_acid", "µg"),
            ("Vitamin B12:", "vitamin_b12", "µg"),
            ("Vitamin C:", "vitamin_c", "mg"),
        ],
    ),
]


def show_message(message):
    """Print a message to the console."""
    print(message)


def print_food_section(title, items, data):
    """Print a formatted nutrient section."""
    print(f"\n--- {title} ---")
    for label, key, unit in items:
        print(f"{label:<24} {data[key]} {unit}")


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
    show_message(f"""
        Welcome to SEDA - Your personal fitness assistant!

                seda  Copyright (C) 2026  {DEVS}
        This program comes with ABSOLUTELY NO WARRANTY.
        This is free software, and you are welcome to redistribute it
        under certain conditions.
        Type "l" for details.\n
                 """)


def show_license_long():
    """Show the project license text. AI-generated content."""
    if not LICENSE_PATH.exists():
        print("LICENSE.md not found.")
        return

    paginator(LICENSE_PATH.read_text(encoding="utf-8"))  # pylint: disable=E1121


# User related functions


def create_user_by_input():
    """Create new user data by asking for input. Partly AI-generated."""
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
    return name, birthdate, height_in_cm, gender, fitness_lvl


def show_user_info_from_class(user):
    """Show the user's information."""
    print("User Information:")
    print(f"Name: {user.name}")
    print(f"Birthdate: {user.birthdate}")
    print(f"Height: {user.height_in_cm} cm")
    print(f"Gender: {user.gender}")
    print(f"Fitness level: {user.fitness_lvl}")


def change_user_information(user):
    """Return input for updating user information."""
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
    show_message("""
        What would you like to do?
        1. Show user information
        2. All about water logs:
        3. All about weight log:
        4. All about meals:
        5. All about activity logs:
        6. Change user information
        7. Show today's calorie status
        8. Delete current user account
        9. Exit
        
        l. Show License
                                """)
    return input("Enter your choice (1-9/l): ")


def prompt_water_log_menu():
    """Show the water log menu and handle user input."""
    show_message("""
        What would you like to do with your water logs?
        1. Add a water log
        2. Show all water logs
        3. Delete a water log
        4. Show today's water intake
        5. Show today's water status
        6. Back to main menu
                                """)
    return input("Enter your choice (1-6): ")


def prompt_weight_log_menu():
    """Show the weight log menu and handle user input."""
    show_message("""
        What would you like to do with your weight logs?
        1. Add a weight log
        2. Show all weight logs
        3. Delete a weight log
        4. Calculate BMI.
        5. Back to main menu
                                """)
    return input("Enter your choice (1-5): ")


def prompt_meal_menu():
    """Show the meal and calorie menu and handle user input. ai-generated."""
    show_message("""
        What would you like to do with meals?
        1. Search foods
        2. Create a meal template
        3. Show meal templates
        4. Update a meal template
        5. Delete a meal template
        6. Consume a single food
        7. Log a consumed meal
        8. Show meal logs
        9. Update a meal log
        10. Delete a meal log
        11. Show today's calorie status
        12. Back to main menu
                                """)
    return input("Enter your choice (1-12): ")


def prompt_activity_menu():
    """Show the activity log menu and handle user input. ai-generated."""
    show_message("""
        What would you like to do with your activity logs?
        1. Add an activity log
        2. Show activity logs
        3. Update an activity log
        4. Delete an activity log
        5. Back to main menu
                                """)
    return input("Enter your choice (1-5): ")


def prompt_meal_name():
    """Prompt the user for a meal template name. ai-generated."""
    meal_name = input("Enter the meal template name: ").strip()
    return meal_name or None


def prompt_food_search_term():
    """Prompt the user for a food search term. ai-generated."""
    search_term = input("Enter a German or English food name to search: ").strip()
    return search_term or None


def prompt_food_id():
    """Prompt the user for a food id. ai-generated."""
    try:
        return int(input("Enter the food_id you want to use: "))
    except ValueError:
        print("Invalid input. Returning to the previous menu.")
        return None


def prompt_food_amount(unit_type):
    """Prompt the user for a food amount. ai-generated."""
    try:
        amount = float(input(f"Enter the amount in {unit_type}: "))
        if amount <= 0:
            raise ValueError
        return amount
    except ValueError:
        print("Invalid input. Please enter a valid positive amount.")
        return None


def prompt_meal_id():
    """Prompt the user for a meal id. ai-generated."""
    try:
        return int(input("Enter the meal ID: "))
    except ValueError:
        print("Invalid input. Returning to the previous menu.")
        return None


def prompt_meal_log_parameters():
    """Prompt the user for meal log values. ai-generated."""
    try:
        amount = float(input("Enter the consumed amount (g/ml): "))
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Invalid amount. Returning to the previous menu.")
        return None, None, None

    unit_type = input("Enter the unit type (g/ml): ").strip().lower() or "g"
    if unit_type not in {"g", "ml"}:
        print("Invalid unit type. Returning to the previous menu.")
        return None, None, None

    timestamp = input(
        "Enter the timestamp (YYYY-MM-DDTHH:MM) or nothing for current time: "
    )
    if not timestamp:
        timestamp = None
    return amount, unit_type, timestamp


def prompt_single_food_log_parameters(unit_type):
    """Prompt the user for direct single-food logging values. ai-generated."""
    amount = prompt_food_amount(unit_type)
    if amount is None:
        return None, None
    timestamp = input(
        "Enter the timestamp (YYYY-MM-DDTHH:MM) or nothing for current time: "
    )
    if not timestamp:
        timestamp = None
    return amount, timestamp


def prompt_activity_log_parameters():
    """Prompt the user for activity log values. ai-generated."""
    activity_name = input("Enter the activity name: ").strip()
    if not activity_name:
        print("Invalid activity name. Returning to the previous menu.")
        return None, None, None, None

    try:
        calories_burned = float(input("Enter the burned calories in kcal: "))
        if calories_burned < 0:
            raise ValueError
    except ValueError:
        print("Invalid burned calories. Returning to the previous menu.")
        return None, None, None, None

    activity_value_input = input(
        "Enter the activity duration in minutes or nothing to skip: "
    ).strip()
    if activity_value_input:
        try:
            activity_value = float(activity_value_input)
            if activity_value < 0:
                raise ValueError
        except ValueError:
            print("Invalid activity duration. Returning to the previous menu.")
            return None, None, None, None
    else:
        activity_value = None

    timestamp = input(
        "Enter the timestamp (YYYY-MM-DDTHH:MM) or nothing for current time: "
    )
    if not timestamp:
        timestamp = None
    return activity_name, calories_burned, activity_value, timestamp


def prompt_yes_no(message):
    """Prompt the user for a yes/no decision. ai-generated."""
    return input(message).strip().lower() == "y"


def prompt_optional_text(message):
    """Prompt the user for an optional text value. ai-generated."""
    return input(message).strip() or None


def prompt_optional_float(message):
    """Prompt the user for an optional float value. ai-generated."""
    value = input(message).strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        print("Invalid input. Returning to the previous menu.")
        return None


def prompt_optional_int(message):
    """Prompt the user for an optional integer value. ai-generated."""
    value = input(message).strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        print("Invalid input. Returning to the previous menu.")
        return None


def prompt_optional_timestamp():
    """Prompt the user for an optional timestamp. ai-generated."""
    return (
        input(
            "Enter the timestamp (YYYY-MM-DDTHH:MM) or nothing to keep the current one: "
        ).strip()
        or None
    )


def show_food_search_results(food_rows):
    """Show food search results. ai-generated."""
    show_message("\nFood search results:")
    for food_row in food_rows:
        print(
            f"food_id: {food_row['food_id']} | "
            f"Name: {food_row['name_de'] or food_row['name_en']} | "
            f"Unit: {food_row['unit_type']} | "
            f"Calories/100 units: {food_row['kcal']}"
        )


def show_meal_templates(meals):
    """Show all meal templates. ai-generated."""
    if not meals:
        print("No meal templates found.")
        return
    for meal in meals:
        print(f"\nMeal ID: {meal.id} | Name: {meal.name} | Calories: {meal.calories}")
        for food_item in meal.food_items:
            print(
                f"  - {food_item.name}: {food_item.amount} {food_item.unit_type} "
                f"({food_item.calories_per_100_units} kcal/100 units)"
            )


def show_meal_logs(meal_logs):
    """Show all meal logs. ai-generated."""
    if not meal_logs:
        print("No meal logs found.")
        return
    for log in meal_logs:
        print(
            f"ID: {log.id}, Meal: {log.meal.name}, Amount: {log.amount} {log.unit_type}, "
            f"Calories: {log.calories}, Timestamp: {log.timestamp}"
        )
        print(
            "  Big 7: "
            f"Fat {log.big_seven.fat} g, "
            f"Saturated fat {log.big_seven.saturated_fat} g, "
            f"Carbohydrate {log.big_seven.carbohydrate} g, "
            f"Sugar {log.big_seven.sugar} g, "
            f"Fibre {log.big_seven.fibre} g, "
            f"Protein {log.big_seven.protein} g, "
            f"Salt {log.big_seven.salt} g"
        )
        # vars(...) exposes the dataclass fields as a dict so we can print only non-empty values.
        additional_nutrients = [
            f"{field_name}: {value}"
            for field_name, value in vars(log.nutrient_summary).items()
            if value not in (None, 0)
        ]
        if additional_nutrients:
            print("  Additional nutrients: " + ", ".join(additional_nutrients))


def show_activity_logs(activity_logs):
    """Show all activity logs. ai-generated."""
    if not activity_logs:
        print("No activity logs found.")
        return
    for log in activity_logs:
        print(
            f"ID: {log.id}, Activity: {log.activity_name}, "
            f"Burned calories: {log.calories_burned} kcal, "
            f"Duration: {log.activity_value} minutes, Timestamp: {log.timestamp}"
        )


def show_water_status(status):
    """Show today's water status. ai-generated."""
    print(
        f"\nWater today: {status['intake']} ml\n"
        f"Water target: {status['target']} ml\n"
        f"Difference: {status['difference']} ml\n"
        f"Progress: {status['progress']} %\n"
    )


# Food-DB related functions
def example_query(food_name="Hafer"):
    """Example function. For testing and demonstration purposes.
    It queries the food database for a given food name.
    It must be deleted or replaced in the final version"""
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
    print(f"Unit type: {data['unit_type']}")
    print("=" * 60)

    for title, items in FOOD_DISPLAY_SECTIONS:
        print_food_section(title, items, data)

    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    example_query(FOOD)
