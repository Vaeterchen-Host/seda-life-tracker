# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Tests for the SEDA database layer."""

import uuid
from pathlib import Path

import pytest

from model.database import Database
from model.classes import User

# pylint: skip-file

# AI-generated content start: fixtures for isolated test setup.
TEST_DB_DIR = Path(__file__).resolve().parents[1] / "test_db"


@pytest.fixture
def db():
    """Create a fresh test database for each test."""
    db_path = TEST_DB_DIR / f"test_{uuid.uuid4().hex}.db"
    database = Database(db_path)
    yield database  # yield is used to provide the fixture value to the test function
    if db_path.exists():  # Clean up the test database after the test is done.
        db_path.unlink()  # unlink() is used to delete the file at db_path


@pytest.fixture
def tobias():
    """Create a fresh user object for each test."""
    return User(None, "Test", "2000-02-22", 185, "m", "beginner", [], [], [], [], [])


# AI-generated content end


# connection related tests
def test_database_connection(db):
    """This test checks if the database connection can be established."""
    assert db is not None, "Database instance could not be created."
    conn = db.connect()
    assert conn is not None, "Connection could not be established."
    conn.close()


def test_close_connection(db):
    """This test checks if the database connection can be closed."""
    conn = db.connect()
    try:
        conn.close()
    except Exception as e:
        assert False, f"Closing the connection not successful: {e}"


# User related tests
# AI-generated content start.
def test_user_table_creation(db):
    """This test checks if the users table is created successfully."""

    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table_exists = cursor.fetchone() is not None
    assert table_exists, "User table could not be created"
    conn.close()


def test_add_a_user(db, tobias):
    """This test try to insert a user in datebase. Partly AI-generated content."""

    db.add_user(
        tobias.name,
        tobias.birthdate,
        tobias.height_in_cm,
        tobias.gender,
        tobias.fitness_lvl,
    )
    row = db.get_user(tobias.name)
    assert row is not None, "User could not be added to the database"
    assert row[1] == tobias.name, "User name does not match"
    assert row[2] == tobias.birthdate, "Birthdate does not match"
    assert row[3] == tobias.height_in_cm, "Height does not match"
    assert row[4] == tobias.gender, "Gender does not match"
    assert row[5] == tobias.fitness_lvl, "Fitness level does not match"


# AI-generated content end


# water log related tests
def test_water_log_table_creation(db):
    """This test checks if the water log table is created successfully."""

    conn = db.connect()
    cursor = conn.cursor()
    db.create_water_log_table()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='water_logs'"
    )
    table_exists = cursor.fetchone() is not None
    assert table_exists, "User table could not be created"
    conn.close()


def test_get_all_water_logs(db, tobias):
    """This test checks if the get_all_water_logs method retrieves logs correctly."""

    db.add_user(
        tobias.name,
        tobias.birthdate,
        tobias.height_in_cm,
        tobias.gender,
        tobias.fitness_lvl,
    )
    conn = db.connect()
    db.add_water_log(1, 500, "2026-03-20T10:00:00")
    logs = db.get_all_water_logs()
    assert len(logs) == 1, "There could not be one water log"
    assert logs[0][1] == 1, "User ID could not be 1"
    assert logs[0][2] == 500, "Amount in ml could not be 500"
    assert logs[0][3] == "2026-03-20T10:00:00", "Timestamp could not match"
    conn.close()


# weight log related tests
def test_weight_log_table_creation(db):
    """This test checks if the weight logs table is created successfully."""
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='weight_logs'"
    )
    table_exists = cursor.fetchone() is not None
    assert table_exists, "Weight logs table could not be created"
    conn.close()


def test_add_and_get_weight_log(db, tobias):
    """This test checks if weight entries can be added and retrieved correctly."""
    # 1. Setup: Create user
    db.add_user(
        tobias.name, tobias.birthdate, tobias.height_in_cm, tobias.gender, tobias.fitness_lvl
    )
    
    # 2. Add weight log (User ID 1)
    db.add_weight_log(1, 85.5, "2026-04-19T09:00:00")
    
    # 3. Retrieve and validate
    logs = db.get_all_weight_logs()
    assert len(logs) == 1, "There should be exactly one weight log entry"
    assert logs[0][1] == 1, "User ID does not match"
    assert logs[0][2] == 85.5, "Weight value does not match"
    assert logs[0][3] == "2026-04-19T09:00:00", "Timestamp does not match"


def test_delete_weight_log(db, tobias):
    """This test checks if a weight log entry can be deleted."""
    # Setup
    db.add_user(tobias.name, tobias.birthdate, tobias.height_in_cm, tobias.gender, tobias.fitness_lvl)
    db.add_weight_log(1, 90.0, "2026-04-18T08:00:00")
    
    # Get the ID of the entry
    logs_before = db.get_all_weight_logs()
    weight_log_id = logs_before[0][0]
    
    # Delete
    deleted_count = db.delete_weight_log(weight_log_id)
    assert deleted_count == 1, "One row should have been deleted"
    
    # Verify
    logs_after = db.get_all_weight_logs()
    assert len(logs_after) == 0, "Weight log table should be empty after deletion"

# delete tests
def test_delete_user(db, tobias):
    """Test checks if user can be deleted."""
    db.add_user(
        tobias.name,
        tobias.birthdate,
        tobias.height_in_cm,
        tobias.gender,
        tobias.fitness_lvl,
    )
    db.delete_user(tobias.name)
    row = db.get_user(tobias.name)
    assert row is None, "User could not be deleted from the database"


def test_delete_water_log(db, tobias):
    """Test checks if water log can be deleted."""
    db.add_user(
        tobias.name,
        tobias.birthdate,
        tobias.height_in_cm,
        tobias.gender,
        tobias.fitness_lvl,
    )
    db.add_water_log(1, 500, "2026-03-20T10:00:00")
    db.delete_water_log(1)
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM water_logs WHERE water_log_id = ?", (1,))
    row = cursor.fetchone()
    assert row is None, "Water log could not be deleted from the database"
    conn.close()

# activity log related tests
def test_activity_log_table_creation(db):
    """This test checks if the activity log table is created successfully."""
    conn = db.connect()
    cursor = conn.cursor()
    # Since create_tables() is called in the database init function, it should already be there
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='activity_logs'"
    )
    table_exists = cursor.fetchone() is not None
    assert table_exists, "Activity log table could not be created"
    conn.close()


def test_add_and_get_activity_log(db, tobias):
    """This test checks if activities can be added and retrieved."""
    # Create a user to get an ID
    db.add_user(
        tobias.name, tobias.birthdate, tobias.height_in_cm, tobias.gender, tobias.fitness_lvl
    )
    
    # Add activity (User ID 1, since it's a new database)
    db.add_activity_log(1, "Jogging", 450.5, "2026-04-11T18:00:00")
    
    logs = db.get_all_activity_logs()
    assert len(logs) == 1, "Activity log count should be 1"
    assert logs[0][2] == "Jogging", "Activity name does not match"
    assert logs[0][3] == 450.5, "Calories burned do not match"


def test_delete_activity_log(db, tobias):
    """This test checks if an activity log can be deleted."""
    db.add_user(
        tobias.name, tobias.birthdate, tobias.height_in_cm, tobias.gender, tobias.fitness_lvl
    )
    db.add_activity_log(1, "Swimming", 300, "2026-04-11T19:00:00")
    
    # retrieving ID first
    logs = db.get_all_activity_logs()
    activity_id = logs[0][0]
    
    # deleting
    deleted_rows = db.delete_activity_log(activity_id)
    assert deleted_rows == 1, "One row should have been deleted"
    
    # verifying
    logs_after = db.get_all_activity_logs()
    assert len(logs_after) == 0, "Activity log table should be empty after deletion"


# food master data related tests
def test_food_table_creation(db):
    """This test checks if the food master data table is created successfully."""
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='foods'"
    )
    table_exists = cursor.fetchone() is not None
    assert table_exists, "Foods table could not be created"
    conn.close()

def test_add_and_get_food(db):
    """This test checks if a food item can be added and retrieved with all nutrients."""
    # We simulate the nutritional values as a dictionary (to match the `add_food` method)
    apple_nutrients = {
        'calorie': 52,
        'fat': 0.2,
        'saturated_fat': 0.0,
        'carbohydrate': 14.0,
        'fibre': 2.4,
        'sugar': 10.0,
        'protein': 0.3,
        'salt': 0.0,
        'sodium': 0.0
    }
    
    # 1. adding Food
    db.add_food("Apple", "food", apple_nutrients)
    
    # 2. view all
    all_foods = db.get_all_foods()
    assert len(all_foods) == 1
    
    # 3. checking all (Index: 0=id, 1=name, 2=food_type, 3=calorie, ...)
    apple_row = all_foods[0]
    assert apple_row[1] == "Apple"
    assert apple_row[2] == "food"
    assert apple_row[3] == 52       # calorie
    assert apple_row[9] == 0.3      # protein


def test_delete_food(db):
    """This test checks if a food item can be deleted from master data."""
    # Placeholder nutritional values for the test
    nutrients = {k: 0 for k in ['calorie', 'fat', 'saturated_fat', 'carbohydrate', 
                                'fibre', 'sugar', 'protein', 'salt', 'sodium']}
    
    db.add_food("Testfood", "food", nutrients)
    foods_before = db.get_all_foods()
    food_id = foods_before[0][0]
    
    # deleting
    deleted_count = db.delete_food(food_id)
    assert deleted_count == 1
    
    # verifying
    foods_after = db.get_all_foods()
    assert len(foods_after) == 0

# food log related tests
def test_food_log_table_creation(db):
    """This test checks if the food logs table is created successfully."""
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='food_logs'"
    )
    table_exists = cursor.fetchone() is not None
    assert table_exists, "Food logs table could not be created"
    conn.close()

def test_add_and_get_food_log(db, tobias):
    """Checks if a user can log a food item and retrieve it with the food name."""
    # 1. Setup: Create user and food master data
    db.add_user(
        tobias.name, tobias.birthdate, tobias.height_in_cm, tobias.gender, tobias.fitness_lvl
    )
    
    nutrients = {k: 0 for k in ['calorie', 'fat', 'saturated_fat', 'carbohydrate', 
                                'fibre', 'sugar', 'protein', 'salt', 'sodium']}
    db.add_food("Banana", "fruit", nutrients)
    
    # Using ID 1 as it is a fresh test database
    user_id = 1
    food_id = 1
    
    # 2. Add log entry
    db.add_food_log(user_id, food_id, 150.0, "2026-04-19T12:00:00")
    
    # 3. Retrieve and validate
    logs = db.get_user_food_logs(user_id)
    assert len(logs) == 1, "There should be exactly one food log entry"
    
    # Check JOIN logic (Index 2 is the name from the foods table)
    assert logs[0][2] == "Banana", "Food name from JOIN does not match"
    assert logs[0][3] == 150.0, "Amount in gram does not match"
    assert logs[0][4] == "2026-04-19T12:00:00", "Timestamp does not match"

def test_delete_food_log(db, tobias):
    """Checks if a food log entry can be deleted."""
    # Setup
    db.add_user(tobias.name, tobias.birthdate, tobias.height_in_cm, tobias.gender, tobias.fitness_lvl)
    nutrients = {k: 0 for k in ['calorie', 'fat', 'saturated_fat', 'carbohydrate', 'fibre', 'sugar', 'protein', 'salt', 'sodium']}
    db.add_food("Apple", "fruit", nutrients)
    
    db.add_food_log(1, 1, 100.0, "2026-04-19T13:00:00")
    
    # Get log ID
    logs_before = db.get_user_food_logs(1)
    log_id = logs_before[0][0]
    
    # Delete
    deleted_count = db.delete_food_log(log_id)
    assert deleted_count == 1
    
    # Verify deletion
    logs_after = db.get_user_food_logs(1)
    assert len(logs_after) == 0

# meal related tests
def test_meal_table_creation(db):
    """This test checks if the meals table is created successfully."""
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='meals'"
    )
    table_exists = cursor.fetchone() is not None
    assert table_exists, "Meals table could not be created"
    conn.close()


def test_add_and_get_meal(db):
    """This test checks if a meal template can be added and retrieved."""
    meal_id = db.add_meal("Protein Breakfast")
    assert meal_id == 1, "First meal ID should be 1"
    
    all_meals = db.get_all_meals()
    assert len(all_meals) == 1, "There should be one meal in the database"
    assert all_meals[0][1] == "Protein Breakfast", "Meal name does not match"


def test_delete_meal(db):
    """This test checks if a meal template can be deleted."""
    db.add_meal("Lunch")
    db.delete_meal(1)
    
    all_meals = db.get_all_meals()
    assert len(all_meals) == 0, "Meal table should be empty after deletion"


# meal item related tests
def test_meal_item_table_creation(db):
    """This test checks if the meal items table is created successfully."""
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='meal_items'"
    )
    table_exists = cursor.fetchone() is not None
    assert table_exists, "Meal items table could not be created"
    conn.close()


def test_add_and_get_meal_item(db):
    """This test checks if a food can be linked to a meal as an item."""
    # Setup: Food and Meal
    nutrients = {k: 0 for k in ['calorie', 'fat', 'saturated_fat', 'carbohydrate', 
                                'fibre', 'sugar', 'protein', 'salt', 'sodium']}
    db.add_food("Oats", "grain", nutrients)
    db.add_meal("Porridge")
    
    # Add Item
    db.add_meal_item(1, 1, 50.0)
    
    items = db.get_meal_items(1)
    assert len(items) == 1, "There should be one item in the meal"
    assert items[0][2] == "Oats", "Food name in meal item does not match"
    assert items[0][3] == 50.0, "Amount in gram does not match"


# meal log related tests
def test_meal_log_table_creation(db):
    """This test checks if the meal logs table is created successfully."""
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='meal_logs'"
    )
    table_exists = cursor.fetchone() is not None
    assert table_exists, "Meal logs table could not be created"
    conn.close()


def test_add_and_get_meal_log(db, tobias):
    """This test checks if a consumed meal can be logged and retrieved."""
    # Setup
    db.add_user(tobias.name, tobias.birthdate, tobias.height_in_cm, tobias.gender, tobias.fitness_lvl)
    db.add_meal("Standard Shake")
    
    # Log Meal
    db.add_meal_log(1, 1, "2026-04-19T08:00:00")
    
    logs = db.get_user_meal_logs(1)
    assert len(logs) == 1, "There should be one meal log entry"
    assert logs[0][2] == "Standard Shake", "Logged meal name does not match"
    assert logs[0][3] == "2026-04-19T08:00:00", "Timestamp does not match"


def test_delete_meal_log(db, tobias):
    """This test checks if a meal log entry can be deleted."""
    db.add_user(tobias.name, tobias.birthdate, tobias.height_in_cm, tobias.gender, tobias.fitness_lvl)
    db.add_meal("Snack")
    db.add_meal_log(1, 1, "2026-04-19T20:00:00")
    
    # Delete
    db.delete_meal_log(1)
    
    logs = db.get_user_meal_logs(1)
    assert len(logs) == 0, "Meal logs should be empty after deletion"