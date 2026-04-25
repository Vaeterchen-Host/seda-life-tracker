# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Tests for the SEDA food classes. Refactored by ai."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dataclasses import replace

import pytest

from model.classes_food import BigSeven, Food, Meal, NutrientSummary, _zero_dataclass

# pylint: skip-file


@pytest.fixture
def zero_nutrient_summary():
    """Create a zero nutrient summary for each test. Refactored by ai."""
    return _zero_dataclass(NutrientSummary)


@pytest.fixture
def test_food(zero_nutrient_summary):
    """Create a food object for each test. Refactored by ai."""
    return Food(
        1,
        "Apple",
        150,
        "g",
        52,
        BigSeven(0.2, 0.03, 14, 2.4, 10, 0.3, 0.01),
        zero_nutrient_summary,
    )


def test_food_amount_setter_rejects_invalid_amount(test_food):
    """This test checks if invalid food amounts are rejected. Refactored by ai."""
    with pytest.raises(ValueError):
        test_food.amount = 0


def test_food_constructor_rejects_invalid_amount(zero_nutrient_summary):
    """This test checks if constructor amount validation works. Refactored by ai."""
    with pytest.raises(ValueError):
        Food(
            1,
            "Apple",
            0,
            "g",
            52,
            BigSeven(0.2, 0.03, 14, 2.4, 10, 0.3, 0.01),
            zero_nutrient_summary,
        )


def test_food_constructor_rejects_invalid_unit_type(zero_nutrient_summary):
    """This test checks if invalid unit types are rejected. Refactored by ai."""
    with pytest.raises(ValueError):
        Food(
            1,
            "Apple",
            150,
            "piece",
            52,
            BigSeven(0.2, 0.03, 14, 2.4, 10, 0.3, 0.01),
            zero_nutrient_summary,
        )


def test_meal_calculates_calories(test_food):
    """This test checks if meal calories are calculated correctly. Refactored by ai."""
    meal = Meal(1, "Fruit", [test_food])

    assert meal.calories == 78


def test_meal_preserves_unknown_calories(zero_nutrient_summary):
    """This test checks if unknown calories stay unknown. Refactored by ai."""
    food = Food(
        1,
        "Apple",
        150,
        "g",
        None,
        BigSeven(0.2, 0.03, 14, 2.4, 10, 0.3, 0.01),
        zero_nutrient_summary,
    )
    meal = Meal(1, "Fruit", [food])

    assert meal.calories is None


def test_meal_uses_zero_for_unknown_calories_with_multiple_foods(zero_nutrient_summary):
    """This test checks if unknown calories count as zero in mixed meals. Refactored by ai."""
    known_food = Food(
        1,
        "Apple",
        150,
        "g",
        52,
        BigSeven(0.2, 0.03, 14, 2.4, 10, 0.3, 0.01),
        zero_nutrient_summary,
    )
    unknown_food = Food(
        2,
        "Berry",
        100,
        "g",
        None,
        BigSeven(0.2, 0.03, 14, 2.4, 10, 0.3, 0.01),
        zero_nutrient_summary,
    )
    meal = Meal(1, "Fruit", [known_food, unknown_food])

    assert meal.calories == 78


def test_meal_calculates_big_seven(test_food):
    """This test checks if big seven values are calculated correctly. Refactored by ai."""
    meal = Meal(1, "Fruit", [test_food])
    summary = meal.big_seven

    assert summary.fat == pytest.approx(0.3)
    assert summary.carbohydrate == pytest.approx(21)
    assert summary.sugar == pytest.approx(15)


def test_meal_preserves_unknown_big_seven_values(zero_nutrient_summary):
    """This test checks if unknown big seven values stay unknown. Refactored by ai."""
    food = Food(
        1,
        "Apple",
        150,
        "g",
        52,
        BigSeven(None, 0.03, 14, 2.4, 10, 0.3, 0.01),
        zero_nutrient_summary,
    )
    meal = Meal(1, "Fruit", [food])

    assert meal.big_seven.fat is None


def test_meal_uses_zero_for_unknown_big_seven_with_multiple_foods(
    zero_nutrient_summary,
):
    """This test checks if unknown big seven values count as zero in mixed meals. Refactored by ai."""
    known_food = Food(
        1,
        "Apple",
        150,
        "g",
        52,
        BigSeven(0.2, 0.03, 14, 2.4, 10, 0.3, 0.01),
        zero_nutrient_summary,
    )
    unknown_food = Food(
        2,
        "Berry",
        100,
        "g",
        52,
        BigSeven(None, 0.03, 14, 2.4, 10, 0.3, 0.01),
        zero_nutrient_summary,
    )
    meal = Meal(1, "Fruit", [known_food, unknown_food])

    assert meal.big_seven.fat == pytest.approx(0.3)


def test_meal_preserves_unknown_nutrient_summary_values(zero_nutrient_summary):
    """This test checks if unknown nutrient values stay unknown. Refactored by ai."""
    nutrient_summary = replace(zero_nutrient_summary, water=None, sodium=2)
    food = Food(
        1,
        "Apple",
        150,
        "g",
        52,
        BigSeven(0.2, 0.03, 14, 2.4, 10, 0.3, 0.01),
        nutrient_summary,
    )
    meal = Meal(1, "Fruit", [food])
    summary = meal.nutrient_summary

    assert summary.water is None
    assert summary.sodium == pytest.approx(3)


def test_meal_uses_zero_for_unknown_nutrients_with_multiple_foods(
    zero_nutrient_summary,
):
    """This test checks if unknown nutrients count as zero in mixed meals. Refactored by ai."""
    known_summary = replace(zero_nutrient_summary, water=10, sodium=2)
    unknown_summary = replace(zero_nutrient_summary, water=None, sodium=3)
    known_food = Food(
        1,
        "Apple",
        150,
        "g",
        52,
        BigSeven(0.2, 0.03, 14, 2.4, 10, 0.3, 0.01),
        known_summary,
    )
    unknown_food = Food(
        2,
        "Berry",
        100,
        "g",
        52,
        BigSeven(0.2, 0.03, 14, 2.4, 10, 0.3, 0.01),
        unknown_summary,
    )
    meal = Meal(1, "Fruit", [known_food, unknown_food])
    summary = meal.nutrient_summary

    assert summary.water == pytest.approx(15)
    assert summary.sodium == pytest.approx(6)
