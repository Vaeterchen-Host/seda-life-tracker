# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""This module contains the food and meal classes for the application."""


from dataclasses import dataclass, fields
from typing import Optional


# Helper functions for dataclass initialization and log validation. ai-generated.
def _zero_dataclass(cls):
    """Create a zero-valued dataclass instance for nutrient objects."""
    return cls(**{field.name: 0 for field in fields(cls)})


# ai-generated content start: helper function for validating log lists. ai-generated.
def _validate_log_list(logs, log_type, label):
    """Validate that logs is a list containing only the expected log type."""
    if not isinstance(logs, list) or not all(isinstance(log, log_type) for log in logs):
        raise ValueError(f"{label} must be a list of {log_type.__name__} objects.")
    return logs


def _validate_non_negative(values):
    """Validate that nutrient values are non-negative."""
    for name, value in values.items():
        if value is not None and value < 0:
            raise ValueError(f"{name} must be non-negative. Got {value}.")


def _add_optional_nutrient(current_total, nutrient_value, factor, none_as_zero=False):
    """Add nutrient values while handling unknown values by meal context."""
    if nutrient_value is None and none_as_zero:
        nutrient_value = 0
    if current_total is None or nutrient_value is None:
        return None
    return current_total + nutrient_value * factor


# ai-generated content end: helper for optional nutrient calculations.


## All classes about food.
@dataclass
class BigSeven:
    """This class defines the nutrient summary of a food."""

    fat: Optional[float]
    saturated_fat: Optional[float]
    carbohydrate: Optional[float]
    fibre: Optional[float]
    sugar: Optional[float]
    protein: Optional[float]
    salt: Optional[float]

    def __post_init__(self):
        """Validate that the nutrient values are non-negative."""
        _validate_non_negative(
            {
                "fat": self.fat,
                "saturated_fat": self.saturated_fat,
                "carbohydrate": self.carbohydrate,
                "fibre": self.fibre,
                "sugar": self.sugar,
                "protein": self.protein,
                "salt": self.salt,
            }
        )


@dataclass
class NutrientSummary:
    """This class defines the nutrient summary outside of the big seven."""

    water: Optional[float]  # in g per 100 Units
    monounsaturated_fat: Optional[float]  # in g per 100 Units
    polyunsaturated_fat: Optional[float]  # in g per 100 Units
    omega_3: Optional[float]  # in g per 100 Units
    omega_6: Optional[float]  # in g per 100 Units
    starch: Optional[float]  # in g per 100 Units
    alcohol: Optional[float]  # in g per 100 Units
    sodium: Optional[float]  # in mg per 100 Units
    cholesterol: Optional[float]  # in mg per 100 Units
    potassium: Optional[float]  # in mg per 100 Units
    calcium: Optional[float]  # in mg per 100 Units
    magnesium: Optional[float]  # in mg per 100 Units
    phosphorus: Optional[float]  # in mg per 100 Units
    iron: Optional[float]  # in mg per 100 Units
    zinc: Optional[float]  # in mg per 100 Units
    iodine: Optional[float]  # in µg per 100 Units
    copper: Optional[float]  # in µg per 100 Units
    manganese: Optional[float]  # in µg per 100 Units
    fluoride: Optional[float]  # in µg per 100 Units
    chromium: Optional[float]  # in µg per 100 Units
    molybdenum: Optional[float]  # in µg per 100 Units
    vitamin_a_re: Optional[float]  # in µg per 100 Units
    vitamin_a_rae: Optional[float]  # in µg per 100 Units
    retinol: Optional[float]  # in µg per 100 Units
    beta_carotene: Optional[float]  # in µg per 100 Units
    vitamin_d: Optional[float]  # in µg per 100 Units
    vitamin_d2: Optional[float]  # in µg per 100 Units
    vitamin_d3: Optional[float]  # in µg per 100 Units
    vitamin_e: Optional[float]  # in mg per 100 Units
    alpha_tocopherol: Optional[float]  # in mg per 100 Units
    vitamin_k: Optional[float]  # in µg per 100 Units
    vitamin_k1: Optional[float]  # in µg per 100 Units
    vitamin_k2: Optional[float]  # in µg per 100 Units
    vitamin_b1: Optional[float]  # in mg per 100 Units
    vitamin_b2: Optional[float]  # in mg per 100 Units
    niacin: Optional[float]  # in mg per 100 Units
    niacin_equivalent: Optional[float]  # in mg per 100 Units
    pantothenic_acid: Optional[float]  # in mg per 100 Units
    vitamin_b6: Optional[float]  # in µg per 100 Units
    biotin: Optional[float]  # in µg per 100 Units
    folate_equivalent: Optional[float]  # in µg per 100 Units
    folate: Optional[float]  # in µg per 100 Units
    folic_acid: Optional[float]  # in µg per 100 Units
    vitamin_b12: Optional[float]  # in µg per 100 Units
    vitamin_c: Optional[float]  # in mg per 100 Units

    def __post_init__(self):
        """Validate that the nutrient values are non-negative."""
        _validate_non_negative(
            {
                "water": self.water,
                "monounsaturated_fat": self.monounsaturated_fat,
                "polyunsaturated_fat": self.polyunsaturated_fat,
                "omega_3": self.omega_3,
                "omega_6": self.omega_6,
                "starch": self.starch,
                "alcohol": self.alcohol,
                "sodium": self.sodium,
                "cholesterol": self.cholesterol,
                "potassium": self.potassium,
                "calcium": self.calcium,
                "magnesium": self.magnesium,
                "phosphorus": self.phosphorus,
                "iron": self.iron,
                "zinc": self.zinc,
                "iodine": self.iodine,
                "copper": self.copper,
                "manganese": self.manganese,
                "fluoride": self.fluoride,
                "chromium": self.chromium,
                "molybdenum": self.molybdenum,
                "vitamin_a_re": self.vitamin_a_re,
                "vitamin_a_rae": self.vitamin_a_rae,
                "retinol": self.retinol,
                "beta_carotene": self.beta_carotene,
                "vitamin_d": self.vitamin_d,
                "vitamin_d2": self.vitamin_d2,
                "vitamin_d3": self.vitamin_d3,
                "vitamin_e": self.vitamin_e,
                "alpha_tocopherol": self.alpha_tocopherol,
                "vitamin_k": self.vitamin_k,
                "vitamin_k1": self.vitamin_k1,
                "vitamin_k2": self.vitamin_k2,
                "vitamin_b1": self.vitamin_b1,
                "vitamin_b2": self.vitamin_b2,
                "niacin": self.niacin,
                "niacin_equivalent": self.niacin_equivalent,
                "pantothenic_acid": self.pantothenic_acid,
                "vitamin_b6": self.vitamin_b6,
                "biotin": self.biotin,
                "folate_equivalent": self.folate_equivalent,
                "folate": self.folate,
                "folic_acid": self.folic_acid,
                "vitamin_b12": self.vitamin_b12,
                "vitamin_c": self.vitamin_c,
            }
        )


class Food:
    """This class defines the food-items."""

    VALID_UNIT_TYPES = {
        "g",
        "ml",
    }

    def __init__(
        self,
        food_id,
        name,
        amount,
        unit_type,
        calories,
        big_seven_per_100_units: BigSeven,
        nutrient_summary: NutrientSummary,
    ):
        """This is the constructor of Food."""
        self._id = food_id
        self.name = name  # refactored by ai
        self.amount = amount  # refactored by ai
        self.unit_type = unit_type  # refactored by ai
        self._calories_per_100_units = calories
        self._big_seven_per_100_units = big_seven_per_100_units
        self._nutrient_summary = nutrient_summary

    # Here are the food related methods.
    @property
    def id(self):
        """This is the getter for 'food_id'. Read only, no Setter."""
        return self._id

    @property
    def name(self):
        """This is the getter for 'name'."""
        return self._name

    @name.setter
    def name(self, new_name):
        """This is the setter for 'name'."""
        self._name = new_name

    @property
    def amount(self):
        """This is the getter for 'amount'."""
        return self._amount

    @amount.setter
    def amount(self, new_amount):
        """This is the setter for 'amount'."""
        if new_amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        self._amount = new_amount

    @property
    def unit_type(self):
        """This is the getter for 'unit_type'."""
        return self._unit_type

    @unit_type.setter
    def unit_type(self, new_unit_type):
        """This is the setter for 'unit_type'."""
        if new_unit_type not in self.VALID_UNIT_TYPES:
            raise ValueError(f"Unit type must be one of {self.VALID_UNIT_TYPES}.")
        self._unit_type = new_unit_type

    @property
    def calories_per_100_units(self):
        """This is the getter for 'calories'. Read only, no Setter."""
        return self._calories_per_100_units

    @property
    def big_seven_per_100_units(self):
        """This is the getter for 'big_seven_per_100_units'. Read only, no Setter."""
        return self._big_seven_per_100_units

    @property
    def nutrient_summary(self):
        """This is the getter for 'nutrient_summary'. Read only, no Setter."""
        return self._nutrient_summary


class Meal:
    """This class defines the meal."""

    def __init__(self, meal_id, name, food_items: list[Food]):
        """This is the constructor of Meal."""
        self._id = meal_id
        self.name = name
        self.food_items = food_items

    # Here are the meal related methods.
    @property
    def id(self):
        """This is the getter for 'meal_id'. Read only, no Setter."""
        return self._id

    @property
    def name(self):
        """This is the getter for 'name'."""
        return self._name

    @name.setter
    def name(self, new_name):
        """This is the setter for 'name'."""
        self._name = new_name

    @property
    def food_items(self):
        """This is the getter for 'food_items'."""
        return self._food_items

    @food_items.setter
    def food_items(self, new_food_items):
        """This is the setter for 'food_items'."""
        if not isinstance(new_food_items, list) or not all(
            isinstance(item, Food) for item in new_food_items
        ):
            raise ValueError("Food items must be a list of Food objects.")
        self._food_items = new_food_items

    @property
    def calories(self):
        """Getter of the total calories of the meal."""
        if not self.food_items:
            return 0
        total_calories = 0
        none_as_zero = len(self.food_items) > 1
        for item in self.food_items:
            factor = item.amount / 100
            total_calories = _add_optional_nutrient(
                total_calories, item.calories_per_100_units, factor, none_as_zero
            )
        return total_calories

    # ai-generated content start: meal nutrient aggregations. ai-generated.
    @property
    def big_seven(self):
        """Getter of the big seven nutrients of the meal."""
        if not self.food_items:
            return _zero_dataclass(BigSeven)

        total = {
            "fat": 0,
            "saturated_fat": 0,
            "carbohydrate": 0,
            "fibre": 0,
            "sugar": 0,
            "protein": 0,
            "salt": 0,
        }

        none_as_zero = len(self.food_items) > 1
        for item in self.food_items:
            factor = item.amount / 100
            nutrients = item.big_seven_per_100_units
            total["fat"] = _add_optional_nutrient(
                total["fat"], nutrients.fat, factor, none_as_zero
            )
            total["saturated_fat"] = _add_optional_nutrient(
                total["saturated_fat"], nutrients.saturated_fat, factor, none_as_zero
            )
            total["carbohydrate"] = _add_optional_nutrient(
                total["carbohydrate"], nutrients.carbohydrate, factor, none_as_zero
            )
            total["fibre"] = _add_optional_nutrient(
                total["fibre"], nutrients.fibre, factor, none_as_zero
            )
            total["sugar"] = _add_optional_nutrient(
                total["sugar"], nutrients.sugar, factor, none_as_zero
            )
            total["protein"] = _add_optional_nutrient(
                total["protein"], nutrients.protein, factor, none_as_zero
            )
            total["salt"] = _add_optional_nutrient(
                total["salt"], nutrients.salt, factor, none_as_zero
            )

        return BigSeven(
            fat=total["fat"],
            saturated_fat=total["saturated_fat"],
            carbohydrate=total["carbohydrate"],
            fibre=total["fibre"],
            sugar=total["sugar"],
            protein=total["protein"],
            salt=total["salt"],
        )

    @property
    def nutrient_summary(self):
        """Getter of the nutrient summary of the meal."""
        if not self.food_items:
            return _zero_dataclass(NutrientSummary)

        total = _zero_dataclass(NutrientSummary)
        none_as_zero = len(self.food_items) > 1
        for item in self.food_items:
            factor = item.amount / 100
            nutrients = item.nutrient_summary
            # refactored by ai: fields() lists all dataclass fields of NutrientSummary.
            for nutrient_field in fields(NutrientSummary):
                # refactored by ai: getattr(obj, name) reads an attribute by its name.
                current_total = getattr(total, nutrient_field.name)
                nutrient_value = getattr(nutrients, nutrient_field.name)
                new_total = _add_optional_nutrient(
                    current_total, nutrient_value, factor, none_as_zero
                )
                # refactored by ai: setattr(obj, name, value) writes an attribute by name.
                setattr(total, nutrient_field.name, new_total)

        return total

    # ai-generated content end: meal nutrient aggregations.

    def add_food_item(self, food_item):
        """Method for adding a food item to meal-composition."""
        self.food_items.append(food_item)

    def remove_food_item(self, food_item_id):
        """Method for removing a food item from meal-composition by id."""
        self.food_items = [item for item in self.food_items if item.id != food_item_id]
