# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Tests for the SEDA database layer."""

import sqlite3
import uuid
from pathlib import Path

import pytest

from config import FOOD_DB_PATH
from model.database import Database, FoodDatabase
from model.class_user import User

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
    return User(1, "Test", "2000-02-22", 185, "m", "beginner", [], [], [], [])


@pytest.fixture
def sample_food_row():
    """Return a stable sample row from the external food DB. AI-generated."""
    conn = sqlite3.connect(FOOD_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT *
        FROM foods
        ORDER BY food_id ASC
        LIMIT 1
        """
    )
    row = cursor.fetchone()
    conn.close()
    assert row is not None, "External food DB should contain at least one food row."
    return row


@pytest.fixture
def sample_food_with_name_en():
    """Return a food row that has an English name for name-based lookup tests. AI-generated."""
    conn = sqlite3.connect(FOOD_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT *
        FROM foods
        WHERE name_en IS NOT NULL AND TRIM(name_en) != ''
        ORDER BY food_id ASC
        LIMIT 1
        """
    )
    row = cursor.fetchone()
    conn.close()
    assert row is not None, "External food DB should contain at least one row with name_en."
    return row


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
    db.add_weight_log(1, 85.5, 185, "2026-04-19T09:00:00")
    
    # 3. Retrieve and validate
    logs = db.get_all_weight_logs()
    assert len(logs) == 1, "There should be exactly one weight log entry"
    assert logs[0][1] == 1, "User ID does not match"
    assert logs[0][2] == 85.5, "Weight value does not match"
    assert logs[0][3] == 185, "Height does not match"
    assert logs[0][4] == "2026-04-19T09:00:00", "Timestamp does not match"


def test_delete_weight_log(db, tobias):
    """This test checks if a weight log entry can be deleted."""
    # Setup
    db.add_user(tobias.name, tobias.birthdate, tobias.height_in_cm, tobias.gender, tobias.fitness_lvl)
    db.add_weight_log(1, 90.0, None, "2026-04-18T08:00:00")
    
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


def test_delete_user_by_id(db, tobias):
    """Test checks if user can be deleted by ID. ai-generated."""
    user_id = db.add_user(
        tobias.name,
        tobias.birthdate,
        tobias.height_in_cm,
        tobias.gender,
        tobias.fitness_lvl,
    )
    deleted_rows = db.delete_user_by_id(user_id)
    assert deleted_rows == 1, "User could not be deleted by ID"
    assert db.get_all_users() == [], "No users should remain in the database"


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
    db.add_activity_log(1, "Jogging", 450.5, 30, "minutes", "2026-04-11T18:00:00")
    
    logs = db.get_all_activity_logs()
    assert len(logs) == 1, "Activity log count should be 1"
    assert logs[0][2] == "Jogging", "Activity name does not match"
    assert logs[0][3] == 450.5, "Calories burned do not match"
    assert logs[0][4] == 30, "Activity value does not match"
    assert logs[0][5] == "minutes", "Unit type does not match"


def test_delete_activity_log(db, tobias):
    """This test checks if an activity log can be deleted."""
    db.add_user(
        tobias.name, tobias.birthdate, tobias.height_in_cm, tobias.gender, tobias.fitness_lvl
    )
    db.add_activity_log(1, "Swimming", 300, None, "minutes", "2026-04-11T19:00:00")
    
    # retrieving ID first
    logs = db.get_all_activity_logs()
    activity_id = logs[0][0]
    
    # deleting
    deleted_rows = db.delete_activity_log(activity_id)
    assert deleted_rows == 1, "One row should have been deleted"
    
    # verifying
    logs_after = db.get_all_activity_logs()
    assert len(logs_after) == 0, "Activity log table should be empty after deletion"


def test_update_activity_log(db, tobias):
    """This test checks if an activity log can be updated. ai-generated."""
    db.add_user(
        tobias.name, tobias.birthdate, tobias.height_in_cm, tobias.gender, tobias.fitness_lvl
    )
    db.add_activity_log(1, "Walking", 120, 30, "minutes", "2026-04-11T19:00:00")

    updated_rows = db.update_activity_log(
        1, "Running", 300, 45, "minutes", "2026-04-11T20:00:00"
    )
    logs = db.get_all_activity_logs()

    assert updated_rows == 1, "One activity log should have been updated"
    assert logs[0][2] == "Running", "Activity name should be updated"
    assert logs[0][3] == 300, "Calories burned should be updated"
    assert logs[0][4] == 45, "Activity value should be updated"
    assert logs[0][6] == "2026-04-11T20:00:00", "Timestamp should be updated"


# food database related tests
def test_food_table_is_not_created_in_main_database(db):
    """This test checks that foods are no longer stored in the main database. AI-refactored."""
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='foods'"
    )
    table_exists = cursor.fetchone() is not None
    assert not table_exists, "Main database should not create a local foods table"
    conn.close()

def test_food_database_connection():
    """This test checks if the external food database can be opened. AI-generated."""
    food_db = FoodDatabase()
    conn = food_db.connect()
    assert conn is not None, "Connection to the external food DB could not be established."
    food_db.end_connection(conn)


def test_food_database_query_by_exact_english_name(sample_food_with_name_en):
    """This test checks exact English-name lookup in the external food DB. AI-generated."""
    food_db = FoodDatabase()
    row = food_db.get_one_food_by_name_en(sample_food_with_name_en["name_en"])
    assert row is not None, "Exact English-name lookup should return a row"
    assert row[0] == sample_food_with_name_en["food_id"], "Food ID does not match expected row"


def test_food_database_query_by_partial_english_name(sample_food_with_name_en):
    """This test checks partial English-name lookup in the external food DB. AI-generated."""
    food_db = FoodDatabase()
    query_term = sample_food_with_name_en["name_en"][:3]
    rows = food_db.get_query_food_by_name_en(query_term)
    assert rows, "Partial English-name lookup should return at least one row"
    assert any(row[0] == sample_food_with_name_en["food_id"] for row in rows)


def test_food_database_custom_sql_query_returns_food_columns():
    """This test checks if the external food DB schema can be queried. AI-generated."""
    food_db = FoodDatabase()
    rows = food_db.custom_sql_query("PRAGMA table_info(foods);")
    column_names = [row[1] for row in rows]
    assert "food_id" in column_names, "Expected food_id column in external foods table"
    assert "bls_code" in column_names, "Expected bls_code column in external foods table"
    assert "name_de" in column_names, "Expected name_de column in external foods table"
    assert "unit_type" in column_names, "Expected unit_type column in external foods table"

def test_food_log_table_is_not_created(db):
    """This test checks that food_logs are replaced by meal_logs. Refactored by ai."""
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='food_logs'"
    )
    table_exists = cursor.fetchone() is not None
    assert not table_exists, "Food logs are legacy and should not be created"
    conn.close()

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


def test_update_meal(db):
    """This test checks if a meal template name can be updated. ai-generated."""
    db.add_meal("Lunch")
    updated_rows = db.update_meal(1, "Late Lunch")

    all_meals = db.get_all_meals()
    assert updated_rows == 1, "One meal should have been updated"
    assert all_meals[0][1] == "Late Lunch", "Meal name should be updated"


# meal food item related tests
def test_meal_food_item_table_creation(db):
    """This test checks if the meal food items table is created successfully."""
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='meal_food_items'"
    )
    table_exists = cursor.fetchone() is not None
    assert table_exists, "Meal food items table could not be created"
    conn.close()


def test_meal_food_item_table_has_only_meal_foreign_key(db):
    """This test checks the reduced FK shape of meal_food_items. AI-generated."""
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_key_list(meal_food_items)")
    foreign_keys = cursor.fetchall()
    conn.close()
    assert len(foreign_keys) == 1, "meal_food_items should only keep the meal foreign key"
    assert foreign_keys[0][2] == "meals", "meal_food_items should reference only meals"


def test_add_and_get_meal_food_item(db, sample_food_row):
    """This test checks if a food from the external DB can be linked to a meal. Partly AI-refactored."""
    db.add_meal("Porridge")

    # Add Item
    db.add_meal_food_item(1, sample_food_row["food_id"], 50.0)

    items = db.get_meal_food_items(1)
    assert len(items) == 1, "There should be one item in the meal"
    expected_name = sample_food_row["name_de"] or sample_food_row["name_en"]
    assert items[0][1] == sample_food_row["food_id"], "Food ID in meal item does not match"
    assert items[0][2] == expected_name, "Food name in meal item does not match"
    assert items[0][3] == 50.0, "Amount in gram does not match"
    assert items[0][4] == "g", "Unit type does not match"
    assert items[0][5] == sample_food_row["kcal"], "Calories should come from the external food DB"
    assert items[0][6] == sample_food_row["fat"], "Fat should come from the external food DB"


def test_get_meal_food_items_returns_none_values_for_missing_food_reference(db):
    """This test checks behavior for orphaned external food references in meal food items. AI-generated."""
    db.add_meal("Fallback Meal")
    db.add_meal_food_item(1, 999999999, 25.0)
    items = db.get_meal_food_items(1)
    assert len(items) == 1, "There should be one meal item"
    assert items[0][2] is None, "Missing external foods should yield a null joined name"
    assert items[0][5] is None, "Missing external foods should yield null nutrient values"


def test_delete_meal_food_items(db, sample_food_row):
    """This test checks if all meal food items of one meal can be deleted. ai-generated."""
    db.add_meal("Porridge")
    db.add_meal_food_item(1, sample_food_row["food_id"], 50.0)

    deleted_rows = db.delete_meal_food_items(1)
    items = db.get_meal_food_items(1)

    assert deleted_rows == 1, "One meal food item should have been deleted"
    assert items == [], "Meal food items should be empty after deletion"


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
    db.add_meal_log(1, 1, 250, "g", "2026-04-19T08:00:00")
    
    logs = db.get_user_meal_logs(1)
    assert len(logs) == 1, "There should be one meal log entry"
    assert logs[0][1] == 1, "User ID does not match"
    assert logs[0][3] == "Standard Shake", "Logged meal name does not match"
    assert logs[0][4] == 250, "Amount does not match"
    assert logs[0][5] == "g", "Unit type does not match"
    assert logs[0][6] == "2026-04-19T08:00:00", "Timestamp does not match"


def test_delete_meal_log(db, tobias):
    """This test checks if a meal log entry can be deleted."""
    db.add_user(tobias.name, tobias.birthdate, tobias.height_in_cm, tobias.gender, tobias.fitness_lvl)
    db.add_meal("Snack")
    db.add_meal_log(1, 1, 100, "g", "2026-04-19T20:00:00")
    
    # Delete
    db.delete_meal_log(1)
    
    logs = db.get_user_meal_logs(1)
    assert len(logs) == 0, "Meal logs should be empty after deletion"


def test_update_meal_log(db, tobias):
    """This test checks if a meal log entry can be updated. ai-generated."""
    db.add_user(tobias.name, tobias.birthdate, tobias.height_in_cm, tobias.gender, tobias.fitness_lvl)
    db.add_meal("Snack")
    db.add_meal("Dinner")
    db.add_meal_log(1, 1, 100, "g", "2026-04-19T20:00:00")

    updated_rows = db.update_meal_log(1, 2, 250, "g", "2026-04-19T21:00:00")
    logs = db.get_user_meal_logs(1)

    assert updated_rows == 1, "One meal log should have been updated"
    assert logs[0][2] == 2, "Meal ID should be updated"
    assert logs[0][3] == "Dinner", "Meal name should reflect the updated meal"
    assert logs[0][4] == 250, "Amount should be updated"
    assert logs[0][6] == "2026-04-19T21:00:00", "Timestamp should be updated"
