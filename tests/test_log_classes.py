# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Tests for the SEDA log classes. Refactored by ai."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from model.classes_log import ActivityLog, MealLog, MealLogHandler, WaterLog, WeightLog

# pylint: skip-file


def test_water_log_stores_amount_and_timestamp():
    """This test checks if water logs store values correctly. Refactored by ai."""
    water_log = WaterLog(1, 1, 900, "2026-03-21T12:12")

    assert water_log.amount_in_ml == 900
    assert water_log.unit_type == "ml"
    assert water_log.timestamp == "2026-03-21T12:12"


def test_weight_log_stores_weight_and_timestamp():
    """This test checks if weight logs store values correctly. Refactored by ai."""
    weight_log = WeightLog(1, 1, 80.5, "2026-03-21T12:12", 185)

    assert weight_log.weight_in_kg == 80.5
    assert weight_log.height_in_cm == 185
    assert weight_log.unit_type == "kg"
    assert weight_log.timestamp == "2026-03-21T12:12"


def test_meal_log_id_is_read_only():
    """This test checks if meal log ids cannot be changed. Refactored by ai."""
    meal_log = MealLog(1, 1, None, 250, "2026-03-22T12:00")

    assert meal_log.id == 1
    assert meal_log.unit_type == "g"
    with pytest.raises(AttributeError):
        meal_log.id = 2


def test_log_item_database_id_can_be_set_once_after_insert():
    """This test checks if database ids can be set once. Refactored by ai."""
    water_log = WaterLog(None, 1, 900, "2026-03-21T12:12")

    water_log.set_database_id(1)

    assert water_log.id == 1
    with pytest.raises(ValueError):
        water_log.set_database_id(2)


def test_activity_log_stores_value_unit_and_calories():
    """This test checks if activity logs store values correctly. Refactored by ai."""
    activity_log = ActivityLog(1, 1, "walking", 120, "2026-03-21T12:12", 30, "minutes")

    assert activity_log.activity_name == "walking"
    assert activity_log.calories_burned == 120
    assert activity_log.activity_value == 30
    assert activity_log.unit_type == "minutes"


def test_activity_log_rejects_invalid_unit_type():
    """This test checks if activity logs only accept minutes. Refactored by ai."""
    with pytest.raises(ValueError):
        ActivityLog(1, 1, "walking", 120, "2026-03-21T12:12", 30, "steps")


def test_meal_log_handler_accepts_meal_logs():
    """This test checks if meal log handlers manage meal logs. Refactored by ai."""
    meal_log = MealLog(1, 1, None, 250, "2026-03-22T12:00")
    handler = MealLogHandler(1, [meal_log])

    assert handler.user_id == 1
    assert len(handler.logs) == 1
    assert handler.logs[0].id == 1


def test_meal_log_handler_rejects_wrong_log_type():
    """This test checks if meal log handlers reject other log types. Refactored by ai."""
    water_log = WaterLog(1, 1, 900, "2026-03-21T12:12")

    with pytest.raises(ValueError):
        MealLogHandler(1, [water_log])


def test_meal_log_rejects_missing_user_id():
    """This test checks if meal logs require a user id. Refactored by ai."""
    with pytest.raises(ValueError):
        MealLog(1, None, None, 250, "2026-03-22T12:00")


def test_meal_log_handler_create_and_delete_log():
    """This test checks if meal log handlers create and delete logs. Refactored by ai."""
    handler = MealLogHandler(1, [])
    new_log = handler.create_log(1, None, 250, "2026-03-22T12:00")

    assert new_log.id == 1
    assert len(handler.logs) == 1

    handler.delete_log(1)

    assert len(handler.logs) == 0
