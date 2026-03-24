"""This is a test file for the database module."""

import uuid
from pathlib import Path

import pytest

from model.database import Database
import model.classes

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
    return model.classes.User(
        "Test", "2000-02-22", 185, "m", "beginner", [], [], [], []
    )


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


# weight log related tests (tbd)


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
