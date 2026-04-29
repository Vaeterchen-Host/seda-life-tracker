# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""This module contains the log classes for the application."""

from dataclasses import fields
from datetime import datetime
from model.classes_food import BigSeven, Meal, NutrientSummary


## All classes for logging
# Parent classes.


# ai-generated content start: helper function for validating log lists. ai-generated.
def _validate_log_list(logs, log_type, label):
    """Validate that logs is a list containing only the expected log type."""
    if not isinstance(logs, list) or not all(isinstance(log, log_type) for log in logs):
        raise ValueError(f"{label} must be a list of {log_type.__name__} objects.")
    return logs


# ai-generated content end

VALID_UNIT_TYPES = {
    "g",  # Meal
    "ml",  # Meal/Water
    "kg",  # Meal/Weight
    "kcal",  # Calories
    "minutes",  # Activity
}


class LogItem:
    """This is the parent class for all log items."""

    def __init__(self, log_id, user_id, timestamp=None):
        """This is the constructor of LogItem."""
        if user_id is None:
            raise ValueError("User ID must not be None.")
        self._log_id = log_id
        self._user_id = user_id

        if timestamp is None:
            self.create_timestamp()
        else:
            self.timestamp = timestamp  # refactored by ai

    @property
    def id(self):
        """This is the getter for 'log_id'. Read only, no Setter."""
        return self._log_id

    def set_database_id(self, new_id):
        """Set the database id once after insert. Refactored by ai."""
        if self._log_id is not None:
            raise ValueError("ID is already set.")
        if new_id is None:
            raise ValueError("Database ID must not be None.")
        self._log_id = new_id

    @property
    def user_id(self):
        """This is the getter for 'user_id'. Read only, no Setter."""
        return self._user_id

    @property
    def unit_type(self):
        """This is the getter for 'unit_type'. Refactored by ai."""
        return self._unit_type

    @property
    def timestamp(self):
        """This is the getter for 'timestamp'."""
        return self._timestamp

    @timestamp.setter
    def timestamp(self, new_timestamp):
        """This is the setter for timestamp."""
        self._timestamp = new_timestamp

    @unit_type.setter
    def unit_type(self, new_unit_type):
        """This is the setter for 'unit_type'. Refactored by ai."""
        if not isinstance(new_unit_type, str):
            raise ValueError("Unit type must be a string.")
        if new_unit_type not in VALID_UNIT_TYPES:
            raise ValueError(f"Unit type must be one of {VALID_UNIT_TYPES}.")
        self._unit_type = new_unit_type

    def create_timestamp(self):
        """Method for creating a timestamp. It can be used when creating a new log item."""
        self._timestamp = datetime.now().isoformat()


class LogHandler:
    """This is the parent class for all log handlers."""

    def __init__(self, user_id, logitems: list[LogItem], log_type=LogItem):
        """This is the constructor of LogHandler."""
        if user_id is None:
            raise ValueError("User ID must not be None.")
        self._user_id = user_id
        self._log_type = log_type  # refactored by ai
        self.logs = logitems

    @property
    def user_id(self):
        """This is the getter for user_id. Read only, no Setter."""
        return self._user_id

    @property
    def logs(self):
        """This is the getter for logs."""
        return self._logs

    @logs.setter
    def logs(self, new_logs):
        """This is the setter for logs."""
        self._logs = _validate_log_list(new_logs, self._log_type, "Logs")

    # Logs must be created and updated in their child classes.
    # Delete logic stays here because it is the same for all log handlers.
    # Use handler.logs and len(handler.logs) for pythonic retrieve/count access.

    def delete_log(self, log_id):
        """Method for deleting a log item."""
        self.logs = [log for log in self.logs if log.id != log_id]


class MealLog(LogItem):  # refactored by ai
    """This class defines the meal log."""

    def __init__(self, meal_log_id, user_id, meal: Meal, amount, unit_type="g", timestamp=None):
        """This is the constructor of MealLog."""
        super().__init__(meal_log_id, user_id, timestamp)
        self.meal = meal  # refactored by ai
        self.amount = amount  # refactored by ai
        self.unit_type = unit_type  # refactored by ai

    @property
    def meal(self):
        """This is the getter for meal."""
        return self._meal

    @meal.setter
    def meal(self, new_meal):
        """This is the setter for meal."""
        self._meal = new_meal

    @property
    def amount(self):
        """This is the getter for amount."""
        return self._amount

    @amount.setter
    def amount(self, new_amount):
        """This is the setter for amount."""
        if new_amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        self._amount = new_amount

    @property
    def calories(self):
        """Return the calories of the logged meal amount. ai-generated."""
        if self.meal is None or self.meal.calories is None:
            return None
        if self.meal.total_amount <= 0:
            return None
        # A meal log can represent only part of a meal template, so calories are scaled by ratio.
        return round(self.meal.calories * (self.amount / self.meal.total_amount), 2)

    @property
    def big_seven(self):
        """Return the logged amount of the meal's big seven nutrients. ai-generated."""
        if self.meal is None or self.meal.total_amount <= 0:
            return BigSeven(None, None, None, None, None, None, None)
        factor = self.amount / self.meal.total_amount
        # fields(BigSeven) lets us scale every nutrient without hardcoding each attribute twice.
        return BigSeven(
            **{
                nutrient_field.name: (
                    None
                    if getattr(self.meal.big_seven, nutrient_field.name) is None
                    else round(getattr(self.meal.big_seven, nutrient_field.name) * factor, 2)
                )
                for nutrient_field in fields(BigSeven)
            }
        )

    @property
    def nutrient_summary(self):
        """Return the logged amount of the meal's additional nutrients. ai-generated."""
        if self.meal is None or self.meal.total_amount <= 0:
            return NutrientSummary(**{field.name: None for field in fields(NutrientSummary)})
        factor = self.amount / self.meal.total_amount
        # The nutrient summary follows the same ratio logic as calories and Big Seven.
        return NutrientSummary(
            **{
                nutrient_field.name: (
                    None
                    if getattr(self.meal.nutrient_summary, nutrient_field.name) is None
                    else round(
                        getattr(self.meal.nutrient_summary, nutrient_field.name) * factor,
                        2,
                    )
                )
                for nutrient_field in fields(NutrientSummary)
            }
        )


class MealLogHandler(LogHandler):  # refactored by ai
    """This class defines the meal log handler."""

    def __init__(self, user_id, logitems: list[MealLog]):
        """This is the constructor of MealLogHandler."""
        super().__init__(user_id, logitems, MealLog)

    def create_log(self, meal_log_id, meal: Meal, amount, unit_type="g", timestamp=None):
        """Method for creating a meal log item and adding it to the logs list."""
        new_log = MealLog(meal_log_id, self.user_id, meal, amount, unit_type, timestamp)
        self.logs.append(new_log)
        return new_log

    def update_log(
        self,
        log_id,
        new_meal=None,
        new_amount=None,
        new_timestamp=None,
        new_unit_type=None,
    ):
        """Method for updating a meal log item."""
        for log in self.logs:
            if log.id == log_id:
                if new_meal is not None:
                    log.meal = new_meal
                if new_amount is not None:
                    log.amount = new_amount
                if new_timestamp is not None:
                    log.timestamp = new_timestamp
                if new_unit_type is not None:
                    log.unit_type = new_unit_type
                return log
        raise ValueError("Log with the given ID not found.")


class WaterLog(LogItem):  # refactored by ai
    """This class defines the water log."""

    def __init__(self, water_log_id, user_id, amount, timestamp):
        """This is the constructor of WaterLog."""
        super().__init__(water_log_id, user_id, timestamp)
        self.amount_in_ml = amount  # refactored by ai
        self.unit_type = "ml"  # refactored by ai

    @property
    def amount_in_ml(self):
        """This is the getter for amount_in_ml."""
        return self._amount_in_ml

    @amount_in_ml.setter
    def amount_in_ml(self, new_amount):
        """This is the setter for amount_in_ml."""
        int(new_amount)
        if new_amount <= 0 or new_amount >= 2000:
            raise ValueError("Amount must be greater than 0 ml.")
        self._amount_in_ml = new_amount


class WaterLogHandler(LogHandler):  # refactored by ai
    """This class defines the water log handler."""

    def __init__(self, user_id, logitems: list[WaterLog]):
        """This is the constructor of WaterLogHandler."""
        super().__init__(user_id, logitems, WaterLog)

    def create_log(self, water_log_id, amount, timestamp):
        """Method for creating a water log item and adding it to the logs list."""
        new_log = WaterLog(water_log_id, self.user_id, amount, timestamp)
        self.logs.append(new_log)
        return new_log

    def update_log(self, log_id, new_amount=None, new_timestamp=None):
        """Method for updating a water log item."""
        for log in self.logs:
            if log.id == log_id:
                if new_amount is not None:
                    log.amount_in_ml = new_amount
                if new_timestamp is not None:
                    log.timestamp = new_timestamp
                return log
        raise ValueError("Log with the given ID not found.")

    def water_intake_today(self):
        """Method for calculating the total water intake of today. Partly AI-generated."""
        today = datetime.now().date()
        total_intake = sum(
            log.amount_in_ml
            for log in self.logs
            if datetime.fromisoformat(log.timestamp).date() == today
        )
        return total_intake


class WeightLog(LogItem):  # refactored by ai
    """This class defines weightlog."""

    def __init__(self, weight_log_id, user_id, weight_in_kg, height_in_cm=None, timestamp=None):
        """This is the constructor of weightlog."""
        super().__init__(weight_log_id, user_id, timestamp)
        self.weight_in_kg = weight_in_kg  # refactored by ai
        self.height_in_cm = height_in_cm  # refactored by ai
        self.unit_type = "kg"  # refactored by ai

    @property
    def weight_in_kg(self):
        """This is the getter for weight_in_kg."""
        return self._weight_in_kg

    @weight_in_kg.setter
    def weight_in_kg(self, new_weight):
        """This is the setter for weight_in_kg."""
        if new_weight <= 0 or new_weight > 350:
            raise ValueError("Weight must be between 0 and 350 kg.")
        self._weight_in_kg = new_weight

    @property
    def height_in_cm(self):
        """This is the getter for height_in_cm. Refactored by ai."""
        return self._height_in_cm

    @height_in_cm.setter
    def height_in_cm(self, new_height):
        """This is the setter for height_in_cm. Refactored by ai."""
        if new_height is not None and (new_height <= 0 or new_height > 300):
            raise ValueError("Height must be between 0 and 300 cm.")
        self._height_in_cm = new_height

    @property
    def bmi(self):
        """This is the getter for current-BMI."""
        if self.height_in_cm is None or self.weight_in_kg is None:
            return None
        return round(self.weight_in_kg / (self.height_in_cm / 100) ** 2, 2)


class WeightLogHandler(LogHandler):  # refactored by ai
    """This class defines the weight log handler."""

    def __init__(self, user_id, logitems: list[WeightLog]):
        """This is the constructor of WeightLogHandler."""
        super().__init__(user_id, logitems, WeightLog)

    def create_log(self, weight_log_id, weight_in_kg, height_in_cm=None, timestamp=None):
        """Method for creating a weight log item and adding it to the logs list."""
        new_log = WeightLog(
            weight_log_id, self.user_id, weight_in_kg, height_in_cm, timestamp
        )
        self.logs.append(new_log)
        return new_log

    def update_log(self, log_id, new_weight=None, new_timestamp=None, new_height=None):
        """Method for updating a weight log item."""
        for log in self.logs:
            if log.id == log_id:
                if new_weight is not None:
                    log.weight_in_kg = new_weight
                if new_timestamp is not None:
                    log.timestamp = new_timestamp
                if new_height is not None:
                    log.height_in_cm = new_height
                return log
        raise ValueError("Log with the given ID not found.")


class ActivityLog(LogItem):  # refactored by ai
    """This class defines the activity log for burned calories."""

    def __init__(
        self,
        activity_log_id,
        user_id,
        activity_name,
        calories_burned,
        activity_value=None,
        unit_type="minutes",
        timestamp=None,
    ):
        """This is the constructor of ActivityLog."""
        super().__init__(activity_log_id, user_id, timestamp)
        self.activity_name = activity_name
        self.calories_burned = calories_burned
        self.activity_value = activity_value  # refactored by ai
        self.unit_type = unit_type  # refactored by ai

    @property
    def activity_name(self):
        """This is the getter for activity_name."""
        return self._activity_name

    @activity_name.setter
    def activity_name(self, new_activity_name):
        """This is the setter for activity_name."""
        if not new_activity_name:
            raise ValueError("Activity name must not be empty.")
        self._activity_name = new_activity_name

    @property
    def calories_burned(self):
        """This is the getter for calories_burned."""
        return self._calories_burned

    @calories_burned.setter
    def calories_burned(self, new_calories_burned):
        """This is the setter for calories_burned."""
        if new_calories_burned < 0:
            raise ValueError("Calories burned must not be negative.")
        self._calories_burned = new_calories_burned

    @property
    def activity_value(self):
        """This is the getter for activity_value. Refactored by ai."""
        return self._activity_value

    @activity_value.setter
    def activity_value(self, new_activity_value):
        """This is the setter for activity_value. Refactored by ai."""
        if new_activity_value is not None and new_activity_value < 0:
            raise ValueError("Activity value must not be negative.")
        self._activity_value = new_activity_value

    @LogItem.unit_type.setter
    def unit_type(self, new_unit_type):
        """This is the setter for activity unit_type. Refactored by ai."""
        if new_unit_type not in VALID_UNIT_TYPES:
            raise ValueError(f"Activity unit type must be one of {VALID_UNIT_TYPES}.")
        self._unit_type = new_unit_type


class ActivityLogHandler(LogHandler):  # refactored by ai
    """This class defines the activity log handler."""

    def __init__(self, user_id, logitems: list[ActivityLog]):
        """This is the constructor of ActivityLogHandler."""
        super().__init__(user_id, logitems, ActivityLog)

    def create_log(
        self,
        activity_log_id,
        activity_name,
        calories_burned,
        activity_value=None,
        unit_type="minutes",
        timestamp=None,
    ):
        """Method for creating an activity log item and adding it to the logs list."""
        new_log = ActivityLog(
            activity_log_id,
            self.user_id,
            activity_name,
            calories_burned,
            activity_value,
            unit_type,
            timestamp,
        )
        self.logs.append(new_log)
        return new_log

    def update_log(
        self,
        log_id,
        new_activity_name=None,
        new_calories_burned=None,
        new_timestamp=None,
        new_activity_value=None,
        new_unit_type=None,
    ):
        """Method for updating an activity log item."""
        for log in self.logs:
            if log.id == log_id:
                if new_activity_name is not None:
                    log.activity_name = new_activity_name
                if new_calories_burned is not None:
                    log.calories_burned = new_calories_burned
                if new_timestamp is not None:
                    log.timestamp = new_timestamp
                if new_activity_value is not None:
                    log.activity_value = new_activity_value
                if new_unit_type is not None:
                    log.unit_type = new_unit_type
                return log
        raise ValueError("Log with the given ID not found.")
