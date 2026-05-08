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
        )
        self._weight_log_handler = WeightLogHandler(
            self.user_id, weight_logs
        )
        self._meal_log_handler = MealLogHandler(
            self.user_id, meal_logs
        )
        self._activity_log_handler = ActivityLogHandler(
            self.user_id, activity_logs
        )

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
        """This is the getter for the water log handler. Partly AI-generated."""
        return self._water_log_handler

    @property
    def weight_log_handler(self):
        """This is the getter for the weight log handler. Partly AI-generated."""
        return self._weight_log_handler

    @property
    def meal_log_handler(self):
        """This is the getter for the meal log handler. Partly AI-generated."""
        return self._meal_log_handler

    @property
    def activity_log_handler(self):
        """This is the getter for the activity log handler. Partly AI-generated."""
        return self._activity_log_handler

    @property
    def last_bmi(self):
        """Method for calculating the BMI. Partly AI-generated."""
        if not self.weight_log_handler.logs:
            return None
        if self.weight_log_handler.logs[-1] is not None:
            return self.weight_log_handler.logs[-1].bmi
        return None

    @property
    def age(self):
        """Return the age of the user based on the birthdate. ai-generated."""
        # fromisoformat() turns the stored ISO string back into a date we can compare.
        birthdate = datetime.fromisoformat(self.birthdate).date()
        today = datetime.now().date()
        return today.year - birthdate.year - (
            (today.month, today.day) < (birthdate.month, birthdate.day)
        )

    @property
    def latest_weight(self):
        """Return the latest logged weight. ai-generated."""
        if not self.weight_log_handler.logs:
            return None
        return self.weight_log_handler.logs[-1].weight_in_kg

    @property
    def basal_metabolic_rate(self):
        """Return the estimated daily calorie target. ai-generated."""
        if self.latest_weight is None:
            return None
        # The formula uses the user's latest weight log so the target reacts to weight changes.
        if self.gender == "m":
            bmr = (
                10 * self.latest_weight
                + 6.25 * self.height_in_cm
                - 5 * self.age
                + 5
            )
        elif self.gender == "f":
            bmr = (
                10 * self.latest_weight
                + 6.25 * self.height_in_cm
                - 5 * self.age
                - 161
            )
        else:
            bmr = (
                10 * self.latest_weight
                + 6.25 * self.height_in_cm
                - 5 * self.age
                - 78
            )
        # The activity factor translates the base metabolic rate into a daily target.
        activity_factor = {
            "beginner": 1.2,
            "intermediate": 1.55,
            "advanced": 1.725,
        }[self.fitness_lvl]
        return round(bmr * activity_factor, 2)

    @property
    def daily_calorie_target(self):
        """Return the estimated daily calorie target. ai-generated."""
        return self.basal_metabolic_rate

    @property
    def today_calorie_intake(self):
        """Return the calories of today's logged meals. ai-generated."""
        today = datetime.now().date()
        # Only logs from today are included, older meal logs stay available for later views.
        calories = [
            log.calories
            for log in self.meal_log_handler.logs
            if datetime.fromisoformat(log.timestamp).date() == today
            and log.calories is not None
        ]
        return round(sum(calories), 2)

    @property
    def today_calories_burned(self):
        """Return the calories burned by today's activity logs. ai-generated."""
        today = datetime.now().date()
        # The same date filter is used here so eaten and burned calories are comparable.
        calories = [
            log.calories_burned
            for log in self.activity_log_handler.logs
            if datetime.fromisoformat(log.timestamp).date() == today
            and log.calories_burned is not None
        ]
        return round(sum(calories), 2)

    @property
    def today_net_calories(self):
        """Return today's eaten calories minus burned calories. ai-generated."""
        return round(self.today_calorie_intake - self.today_calories_burned, 2)

    @property
    def daily_water_target(self):
        """Return the estimated daily water target in ml. ai-generated."""
        if self.latest_weight is not None:
            return round(self.latest_weight * 35)
        return 2000

    @property
    def today_water_balance(self):
        """Return the water target minus today's intake. ai-generated."""
        return self.daily_water_target - self.water_log_handler.water_intake_today()

    @property
    def today_water_progress(self):
        """Return the water progress of today in percent. ai-generated."""
        if self.daily_water_target <= 0:
            return None
        return round(
            (self.water_log_handler.water_intake_today() / self.daily_water_target) * 100,
            2,
        )

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
