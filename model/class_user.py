# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""This module contains the user class for the application."""

from datetime import datetime

from model.classes_log import (
    ActivityLog,
    ActivityLogHandler,
    MealLog,
    MealLogHandler,
    WaterLog,
    WaterLogHandler,
    WeightLog,
    WeightLogHandler,
)


# User class. Somehow the main node of all classes.
class User:
    """This is the class User."""

    def __init__(
        self,
        user_id,
        name,
        birthdate,
        height_in_cm,
        gender,
        fitness_lvl,
        water_logs: list[WaterLog],
        weight_logs: list[WeightLog],
        meal_logs: list[MealLog],
        activity_logs: list[ActivityLog],
    ):
        """This is the constructor of User."""
        self._user_id = user_id
        self.name = name
        self.birthdate = birthdate
        self.height_in_cm = height_in_cm
        self.gender = gender
        self.fitness_lvl = fitness_lvl
        self._water_log_handler = WaterLogHandler(
            self.user_id, water_logs
        )  # refactored by ai
        self._weight_log_handler = WeightLogHandler(
            self.user_id, weight_logs
        )  # refactored by ai
        self._meal_log_handler = MealLogHandler(
            self.user_id, meal_logs
        )  # refactored by ai
        self._activity_log_handler = ActivityLogHandler(
            self.user_id, activity_logs
        )  # refactored by ai

    # Aliases
    @property
    def user_id(self):
        """This is the getter for user_id"""
        return self._user_id

    @property
    def name(self):
        """This is the getter for name."""
        return self._name

    @name.setter
    def name(self, new_name):
        """This is the setter for name."""
        if not new_name:
            raise ValueError("Name must not be empty.")
        self._name = new_name

    @property
    def birthdate(self):
        """This is the getter for birthdate."""
        return self._birthdate

    @birthdate.setter
    def birthdate(self, new_birthdate):
        """This is the setter for birthdate."""
        self._birthdate = new_birthdate

    @property
    def height_in_cm(self):
        """This is the getter for height_in_cm."""
        return self._height_in_cm

    @height_in_cm.setter
    def height_in_cm(self, new_height):
        """This is the setter for height_in_cm."""
        if new_height <= 0 or new_height > 250:
            raise ValueError("Height must be between 0 and 250 cm.")
        self._height_in_cm = new_height

    @property
    def gender(self):
        """This is the getter for gender."""
        return self._gender

    @gender.setter
    def gender(self, new_gender):
        """This is the setter for gender."""
        if new_gender not in ("m", "f", "d"):
            raise ValueError("Gender must be 'm', 'f' or 'd'.")
        self._gender = new_gender

    @property
    def fitness_lvl(self):
        """This is the getter for fitness_lvl."""
        return self._fitness_lvl

    @fitness_lvl.setter
    def fitness_lvl(self, new_fitness_lvl):
        """This is the setter for fitness_lvl."""
        if new_fitness_lvl not in ("beginner", "intermediate", "advanced"):
            raise ValueError(
                "Fitness level must be 'beginner', 'intermediate' or 'advanced'."
            )
        self._fitness_lvl = new_fitness_lvl

    @property
    def water_log_handler(self):
        """This is the getter for the water log handler. Refactored by ai."""
        return self._water_log_handler  # refactored by ai

    @property
    def weight_log_handler(self):
        """This is the getter for the weight log handler. Refactored by ai."""
        return self._weight_log_handler  # refactored by ai

    @property
    def meal_log_handler(self):
        """This is the getter for the meal log handler. Refactored by ai."""
        return self._meal_log_handler  # refactored by ai

    @property
    def activity_log_handler(self):
        """This is the getter for the activity log handler. Refactored by ai."""
        return self._activity_log_handler  # refactored by ai

    # User methods

    def update_biometrical_data(
        self, birthdate=None, height_in_cm=None, gender=None, fitness_lvl=None
    ):
        """This method updates the biometrical data of the user."""
        if birthdate is not None:
            self.birthdate = birthdate
        if height_in_cm is not None:
            self.height_in_cm = height_in_cm
        if gender is not None:
            self.gender = gender
        if fitness_lvl is not None:
            self.fitness_lvl = fitness_lvl

    def return_bmi(self):
        """Method for calculating the BMI. Partly AI-generated."""
        if self.height_in_cm is None or not self.weight_logs:
            return "BMI cannot be calculated. Please add a weight log first."
        height_in_m = self.height_in_cm / 100
        latest_weight = self.weight_logs[-1].weight_in_kg
        bmi = latest_weight / (height_in_m**2)
        return round(bmi, 2)

    def water_intake_today(self):
        """Method for calculating the total water intake of today. Partly AI-generated."""
        today = datetime.now().date()
        total_intake = sum(
            log.amount_in_ml
            for log in self.water_logs
            if datetime.fromisoformat(log.timestamp).date() == today
        )
        return total_intake
