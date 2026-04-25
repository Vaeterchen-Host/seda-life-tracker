# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Tests for the SEDA log classes. Refactored by ai."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from model.classes_log import MealLog, WaterLog, WeightLog

# pylint: skip-file


def test_water_log_stores_amount_and_timestamp():
    """This test checks if water logs store values correctly. Refactored by ai."""
    water_log = WaterLog(1, 900, "2026-03-21T12:12")

    assert water_log.amount_in_ml == 900
    assert water_log.timestamp == "2026-03-21T12:12"


def test_weight_log_stores_weight_and_timestamp():
    """This test checks if weight logs store values correctly. Refactored by ai."""
    weight_log = WeightLog(1, 80.5, "2026-03-21T12:12")

    assert weight_log.weight_in_kg == 80.5
    assert weight_log.timestamp == "2026-03-21T12:12"


def test_meal_log_id_is_read_only():
    """This test checks if meal log ids cannot be changed. Refactored by ai."""
    meal_log = MealLog(1, None, 250, "2026-03-22T12:00")

    assert meal_log.id == 1
    with pytest.raises(AttributeError):
        meal_log.id = 2
