# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Tests for the SEDA user class. Partly AI-generated."""

from dataclasses import fields
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from model.class_user import User
from model.classes_food import BigSeven, Food, Meal, NutrientSummary
from model.classes_log import MealLog, WaterLog, WeightLog

# pylint: skip-file


@pytest.fixture
def water_log_1():
    """Create a waterlog object for each test. Partly AI-generated."""
    return WaterLog(1, 1, 900, "2026-03-21T12:12")


@pytest.fixture
def weight_log_1():
    """Create a weightlog object for each test. Partly AI-generated."""
    return WeightLog(1, 1, 80.5, None, "2026-03-21T12:12")


@pytest.fixture
def test_user_class(water_log_1, weight_log_1):
    """Create a fresh user object for each test. Partly AI-generated."""
    return User(
        1,
        "Test",
        "2000-02-22",
        185,
        "m",
        "beginner",
        [water_log_1],
        [weight_log_1],
        [],
        [],
    )


def test_get_water_logs(test_user_class):
    """This test checks if water logs are retrieved correctly. Partly AI-generated."""
    assert len(test_user_class.water_log_handler.logs) == 1
    assert test_user_class.water_log_handler.logs[0].amount_in_ml == 900
    assert test_user_class.water_log_handler.logs[0].unit_type == "ml"
    assert test_user_class.water_log_handler.logs[0].timestamp == "2026-03-21T12:12"


def test_add_water_log(test_user_class):
    """This test checks if water logs are added correctly. Partly AI-generated."""
    test_user_class.water_log_handler.create_log(
        None, 500, "2026-03-22T08:00"
    )

    assert len(test_user_class.water_log_handler.logs) == 2
    assert test_user_class.water_log_handler.logs[1].amount_in_ml == 500
    assert test_user_class.water_log_handler.logs[1].unit_type == "ml"
    assert test_user_class.water_log_handler.logs[1].timestamp == "2026-03-22T08:00"


def test_get_weight_logs(test_user_class):
    """This test checks if weight logs are retrieved correctly. Partly AI-generated."""
    assert len(test_user_class.weight_log_handler.logs) == 1
    assert test_user_class.weight_log_handler.logs[0].weight_in_kg == 80.5
    assert test_user_class.weight_log_handler.logs[0].unit_type == "kg"
    assert test_user_class.weight_log_handler.logs[0].timestamp == "2026-03-21T12:12"


def test_add_weight_log(test_user_class):
    """This test checks if weight logs are added correctly. Partly AI-generated."""
    test_user_class.weight_log_handler.create_log(
        None, 79.8, test_user_class.height_in_cm, "2026-03-22T08:00"
    )

    assert len(test_user_class.weight_log_handler.logs) == 2
    assert test_user_class.weight_log_handler.logs[1].weight_in_kg == 79.8
    assert test_user_class.weight_log_handler.logs[1].height_in_cm == 185
    assert test_user_class.weight_log_handler.logs[1].unit_type == "kg"
    assert test_user_class.weight_log_handler.logs[1].timestamp == "2026-03-22T08:00"


def test_add_activity_log(test_user_class):
    """This test checks if activity logs are added correctly. Partly AI-generated."""
    test_user_class.activity_log_handler.create_log(
        None, "walking", 120, 30, "minutes", "2026-03-22T08:00"
    )

    assert len(test_user_class.activity_log_handler.logs) == 1
    assert test_user_class.activity_log_handler.logs[0].activity_name == "walking"
    assert test_user_class.activity_log_handler.logs[0].calories_burned == 120
    assert test_user_class.activity_log_handler.logs[0].activity_value == 30
    assert test_user_class.activity_log_handler.logs[0].unit_type == "minutes"


def test_last_bmi_returns_bmi_of_latest_weight_log(test_user_class):
    """This test checks if the latest weight log BMI is returned. ai-generated."""
    test_user_class.weight_log_handler.create_log(
        None, 79.8, test_user_class.height_in_cm, "2026-03-22T08:00"
    )

    assert test_user_class.last_bmi == 23.32


def test_latest_weight_and_bmr_use_newest_weight_timestamp(test_user_class):
    """This test checks if biometrics use the chronologically newest weight log. AI-generated."""
    test_user_class.weight_log_handler.create_log(
        None, 79.8, test_user_class.height_in_cm, "2026-03-22T08:00"
    )
    test_user_class.weight_log_handler.create_log(
        None, 92.0, test_user_class.height_in_cm, "2026-03-01T08:00"
    )

    assert test_user_class.latest_weight == 79.8
    assert test_user_class.last_bmi == 23.32
    assert test_user_class.daily_water_target == 2793


def test_last_bmi_returns_none_without_weight_logs():
    """This test checks if BMI is None without weight logs. ai-generated."""
    test_user = User(
        1,
        "Test",
        "2000-02-22",
        185,
        "m",
        "beginner",
        [],
        [],
        [],
        [],
    )

    assert test_user.last_bmi is None


def test_get_meal_log_handler(test_user_class):
    """This test checks if the meal log handler is available. ai-generated."""
    meal_log = MealLog(1, 1, None, 250, "g", "2026-03-22T12:00")
    test_user_class.meal_log_handler.logs = [meal_log]

    assert len(test_user_class.meal_log_handler.logs) == 1
    assert test_user_class.meal_log_handler.logs[0].id == 1


def test_set_invalid_meal_log_handler_logs_raises_value_error(test_user_class):
    """This test checks if invalid handler logs are rejected. ai-generated."""
    with pytest.raises(ValueError):
        test_user_class.meal_log_handler.logs = ["not a meal log"]


def test_today_calories_burned_sums_only_today_activity_logs(
    test_user_class, monkeypatch
):
    """This test checks if only today's burned calories are summed. ai-generated."""
    class FrozenDateTime:
        """Minimal datetime stand-in for today's date. ai-generated."""

        @staticmethod
        def now():
            from datetime import datetime

            return datetime.fromisoformat("2026-04-29T18:00:00")

        @staticmethod
        def fromisoformat(value):
            from datetime import datetime

            return datetime.fromisoformat(value)

    monkeypatch.setattr("model.class_user.datetime", FrozenDateTime)
    test_user_class.activity_log_handler.create_log(
        1, "walking", 120, 30, "minutes", "2026-04-29T08:00:00"
    )
    test_user_class.activity_log_handler.create_log(
        2, "cycling", 200, 45, "minutes", "2026-04-29T18:00:00"
    )
    test_user_class.activity_log_handler.create_log(
        3, "running", 300, 60, "minutes", "2026-04-28T18:00:00"
    )

    assert test_user_class.today_calories_burned == 320


def test_today_net_calories_subtracts_burned_from_intake(monkeypatch):
    """This test checks if net calories subtract activity from meal intake. ai-generated."""
    user = User(
        1,
        "Test",
        "2000-02-22",
        185,
        "m",
        "beginner",
        [],
        [],
        [],
        [],
    )
    food_item = Food(
        1,
        "Oats",
        100,
        "g",
        370,
        BigSeven(7, 1, 58, 10, 1, 13, 0.01),
        NutrientSummary(*([0] * len(fields(NutrientSummary)))),
    )
    meal = Meal(1, "Porridge", [food_item])
    user.meal_log_handler.create_log(
        1, meal, 100, "g", "2026-04-29T08:00:00"
    )
    user.activity_log_handler.create_log(
        1, "walking", 120, 30, "minutes", "2026-04-29T12:00:00"
    )

    class FrozenDateTime:
        """Minimal datetime stand-in for today's date. ai-generated."""

        @staticmethod
        def now():
            from datetime import datetime

            return datetime.fromisoformat("2026-04-29T18:00:00")

        @staticmethod
        def fromisoformat(value):
            from datetime import datetime

            return datetime.fromisoformat(value)

    monkeypatch.setattr("model.class_user.datetime", FrozenDateTime)

    assert user.today_calorie_intake == 370
    assert user.today_calories_burned == 120
    assert user.today_net_calories == 250


def test_daily_water_target_and_progress_use_latest_weight(test_user_class, monkeypatch):
    """This test checks if the daily water status uses the latest weight. ai-generated."""
    class FrozenDateTime:
        """Minimal datetime stand-in for today's date. ai-generated."""

        @staticmethod
        def now():
            from datetime import datetime

            return datetime.fromisoformat("2026-03-22T18:00:00")

        @staticmethod
        def fromisoformat(value):
            from datetime import datetime

            return datetime.fromisoformat(value)

    monkeypatch.setattr("model.class_user.datetime", FrozenDateTime)
    monkeypatch.setattr("model.classes_log.datetime", FrozenDateTime)
    test_user_class.water_log_handler.create_log(2, 1400, "2026-03-22T08:00")

    assert test_user_class.daily_water_target == 2818
    assert test_user_class.today_water_balance == 1418
    assert test_user_class.today_water_progress == 49.68
