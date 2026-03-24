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

#------------------------------------

# AI-generated content end

def test_create_weight_log_table(db):
    """Test if the weight log table is created successfully."""
    conn = db.connect()
    cursor = conn.cursor()
    db.create_weight_log_table()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='weight_logs'"
    )
    table_exists = cursor.fetchone() is not None
    assert table_exists, "Weight log table could not be created"
    conn.close()


def test_add_weight_log(db, tobias):
    """Test adding a weight log entry."""
    db.create_weight_log_table()
    db.add_user(
        tobias.name,
        tobias.birthdate,
        tobias.height_in_cm,
        tobias.gender,
        tobias.fitness_lvl,
    )
    user = db.get_user(tobias.name)
    # user structure: (id, name, dob, height, gender, fitness)

    db.add_weight_log(user[0], 80.5, "2026-03-24T10:00:00")
    logs = db.get_all_weight_logs()

    assert len(logs) == 1, "Weight log was not added"
    assert logs[0][1] == user[0], "User ID does not match"
    assert logs[0][2] == 80.5, "Weight does not match"
    assert logs[0][3] == "2026-03-24T10:00:00", "Timestamp does not match"


def test_delete_weight_log(db, tobias):
    """Test deleting a weight log entry."""
    db.create_weight_log_table()
    db.add_user(
        tobias.name,
        tobias.birthdate,
        tobias.height_in_cm,
        tobias.gender,
        tobias.fitness_lvl,
    )
    user = db.get_user(tobias.name)
    db.add_weight_log(user[0], 80.5, "2026-03-24T10:00:00")
    logs = db.get_all_weight_logs()
    weight_log_id = logs[0][0]

    db.delete_weight_log(weight_log_id)
    logs_after = db.get_all_weight_logs()
    assert len(logs_after) == 0, "Weight log was not deleted"
