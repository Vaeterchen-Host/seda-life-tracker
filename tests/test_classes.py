"""This is a test file for the classes module."""

import uuid
from pathlib import Path

import pytest

from model.database import Database
from model.classes import User, WaterLog, WeightLog

# pylint: skip-file

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
def water_log():
    """Create a waterlog object for each test."""
    return WaterLog(900, "2026-03-21T12:12")

@pytest.fixture
def weight_log():
    """Create a weightlog object for each test."""
    return WeightLog(80.5, "2026-03-21T12:12")

@pytest.fixture
def tobias():
    """Create a fresh user object for each test."""
    return User(
        "Test", "2000-02-22", 185, "m", "beginner", [water_log], [weight_log], [], []
    )

# Tests for waterlog_class

def test_get_water_logs(db, tobias):
    """This test checks if the getter methods retrieves correctly."""
    test = water_log
    assert test.amount_in_ml == 900, "There could not be one water log"
