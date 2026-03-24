"""This is a test file for the classes module."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


import pytest

from model.classes import User, WaterLog, WeightLog

# pylint: skip-file

@pytest.fixture
def water_log_1():
    """Create a waterlog object for each test."""
    return WaterLog(1, 900, "2026-03-21T12:12")

@pytest.fixture
def weight_log_1():
    """Create a weightlog object for each test."""
    return WeightLog(1, 80.5, "2026-03-21T12:12")

@pytest.fixture
def tobias(water_log_1, weight_log_1):
    """Create a fresh user object for each test."""
    return User(
        None, "Test", "2000-02-22", 185, "m", "beginner", [water_log_1], [weight_log_1], [], []
    )

# Tests for waterlog_class

def test_get_water_logs(tobias):
    """This test checks if the getter method retrieves correctly. Partly AI-generated content."""
    assert len(tobias.water_logs) == 1
    assert tobias.water_logs[0].amount_in_ml == 900
    assert tobias.water_logs[0].timestamp == "2026-03-21T12:12"

def test_add_water_log(tobias):
    """This test checks if the add method adds correctly. Partly AI-generated content."""
    tobias.add_water_log(2, 500, "2026-03-22T08:00")
    assert len(tobias.water_logs) == 2
    assert tobias.water_logs[1].amount_in_ml == 500
    assert tobias.water_logs[1].timestamp == "2026-03-22T08:00"

def test_remove_water_log(tobias):
    """This test checks if the remove method removes correctly. Partly AI-generated content."""
    tobias.add_water_log(2, 500, "2026-03-22T08:00")
    assert len(tobias.water_logs) == 2
    assert tobias.water_logs[1].amount_in_ml == 500
    assert tobias.water_logs[1].timestamp == "2026-03-22T08:00"
    tobias.delete_water_log(1)
    assert len(tobias.water_logs) == 1

def test_get_weight_logs(tobias):
    """This test checks if the getter method retrieves correctly. Partly AI-generated content."""
    assert len(tobias.weight_logs) == 1
    assert tobias.weight_logs[0].weight_in_kg == 80.5
    assert tobias.weight_logs[0].timestamp == "2026-03-21T12:12"

def test_add_weight_log(tobias):
    """This test checks if the add method adds correctly. Partly AI-generated content."""
    tobias.add_weight_log(2, 79.8, "2026-03-22T08:00")
    assert len(tobias.weight_logs) == 2
    assert tobias.weight_logs[1].weight_in_kg == 79.8
    assert tobias.weight_logs[1].timestamp == "2026-03-22T08:00"

def test_remove_weight_log(tobias):
    """This test checks if the remove method removes correctly. Partly AI-generated content."""
    tobias.add_weight_log(2, 79.8, "2026-03-22T08:00")
    assert len(tobias.weight_logs) == 2
    assert tobias.weight_logs[1].weight_in_kg == 79.8
    assert tobias.weight_logs[1].timestamp == "2026-03-22T08:00"
    tobias.delete_weight_log(1)
    assert len(tobias.weight_logs) == 1

