# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""This module contains the user class for the application."""

from datetime import datetime

from model.classes_food import _validate_log_list  # refactored by ai
from model.classes_log import (  # refactored by ai
    ActivityLog,
    MealLog,
    WaterLog,
    WeightLog,
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
        water: list[WaterLog],
        weight: list[WeightLog],
        meal: list[MealLog],
        activity: list[ActivityLog],
        food=None,  # refactored by ai
    ):
        """This is the constructor of User."""
        self._id = user_id
        self.name = name  # refactored by ai
        self.birthdate = birthdate  # refactored by ai
        self.height_in_cm = height_in_cm  # refactored by ai
        self.gender = gender  # refactored by ai
        self.fitness_lvl = fitness_lvl  # refactored by ai
        self.water_logs = water  # refactored by ai
        self.weight_logs = weight  # refactored by ai
        self._food = [] if food is None else food  # refactored by ai
        self.meal_logs = meal  # refactored by ai
        self.activity_logs = activity  # refactored by ai

    # Here are the biometrical data related methods.
    @property
    def id(self):
        """This is the getter for id"""
        return self._id

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
    def water_logs(self):
        """This is the getter for water logs."""
        return self._water

    @water_logs.setter
    def water_logs(self, new_water_logs):
        """This is the setter for water logs. Partly AI-generated."""
        self._water = _validate_log_list(
            new_water_logs, WaterLog, "Water logs"
        )  # refactored by ai

    @property
    def weight_logs(self):
        """This is the getter for weight logs."""
        return self._weight

    @weight_logs.setter
    def weight_logs(self, new_weight_logs):
        """This is the setter for weight logs. Partly AI-generated."""
        self._weight = _validate_log_list(new_weight_logs, WeightLog, "Weight logs")

    @property
    def food_logs(self):
        """This is the getter for food logs."""
        return self._food

    @food_logs.setter
    def food_logs(self, new_food_logs):
        """This is the setter for food logs. Partly AI-generated."""
        self._food = _validate_log_list(new_food_logs, "Food logs")  # refactored by ai

    @property
    def meal_logs(self):
        """This is the getter for meal logs."""
        return self._meal

    @meal_logs.setter
    def meal_logs(self, new_meal_logs):
        """This is the setter for meal logs. Partly AI-generated."""
        self._meal = _validate_log_list(
            new_meal_logs, MealLog, "Meal logs"
        )  # refactored by ai

    @property
    def activity_logs(self):
        """This is the getter for activity logs."""
        return self._activity

    @activity_logs.setter
    def activity_logs(self, new_activity_logs):
        """This is the setter for activity logs."""
        self._activity = _validate_log_list(
            new_activity_logs, ActivityLog, "Activity logs"
        )  # refactored by ai

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

    # Here are the weight log related methods.
    def add_weight_log(self, weight_in_kg, timestamp=None):
        """Method for adding a weightlog."""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        new_weight_log = WeightLog(None, weight_in_kg, timestamp)
        self._weight.append(new_weight_log)

    def delete_weight_log(self, weight_log_id):
        """Method for deleting a weightlog within the class instance. AI-generated."""
        remaining_weight_logs = []

        for weight_log in self._weight:
            if weight_log.id != weight_log_id:
                remaining_weight_logs.append(weight_log)

        self._weight = remaining_weight_logs

    def show_weight_logs(self):
        """Method for showing all weightlogs. Partly AI-generated."""
        if not self._weight:
            print("No weight logs found.")
            return
        for log in self._weight:
            print(
                f"ID: {log.id}, Weight: {log.weight_in_kg} kg, Timestamp: {log.timestamp}"
            )

    def calculate_bmi(self):
        """Method for calculating the BMI. Partly AI-generated."""
        if self.height_in_cm is None or not self._weight:
            return "BMI cannot be calculated. Please add a weight log first."
        height_in_m = self.height_in_cm / 100
        latest_weight = self._weight[-1].weight_in_kg
        bmi = latest_weight / (height_in_m**2)
        return round(bmi, 2)

    # Here are the water log related methods.
    def add_water_log(self, amount_in_ml, timestamp=None):
        """Method for adding a waterlog."""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        new_water_log = WaterLog(None, amount_in_ml, timestamp)
        self._water.append(new_water_log)

    def show_water_logs(self):
        """Method for showing all waterlogs. Partly AI-generated."""
        if not self._water:
            print("No water logs found.")
            return
        for log in self._water:
            print(
                f"ID: {log.id}, Amount: {log.amount_in_ml} ml, Timestamp: {log.timestamp}"
            )

    def delete_water_log(self, water_log_id):
        """Method for deleting a waterlog. AI-generated."""
        remaining_water_logs = []

        for water_log in self._water:
            if water_log.id != water_log_id:
                remaining_water_logs.append(water_log)

        self._water = remaining_water_logs

    def water_intake_today(self):
        """Method for calculating the total water intake of today. Partly AI-generated."""
        today = datetime.now().date()
        total_intake = sum(
            log.amount_in_ml
            for log in self._water
            if datetime.fromisoformat(log.timestamp).date() == today
        )
        return total_intake

    # Here are the food log related methods.
    def add_food_log(self, food_log_id, food, amount_in_gram, timestamp=None):
        """Method for adding a foodlog."""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        new_food_log = FoodLog(food_log_id, food, amount_in_gram, timestamp)
        self._food.append(new_food_log)

    def delete_food_log(self, food_log_id):
        """Method for deleting a foodlog. AI-generated."""
        remaining_food_logs = []

        for food_log in self._food:
            if food_log.id != food_log_id:
                remaining_food_logs.append(food_log)

        self._food = remaining_food_logs

    # Here are the meal log related methods.
    def add_meal_log(self, meal_log_id, meal, amount_in_gram, timestamp=None):
        """Method for adding a meallog."""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        new_meal_log = MealLog(meal_log_id, meal, amount_in_gram, timestamp)
        self._meal.append(new_meal_log)

    def delete_meal_log(self, meal_log_id):
        """Method for deleting a meallog. AI-generated."""
        remaining_meal_logs = []

        for meal_log in self._meal:
            if meal_log.id != meal_log_id:
                remaining_meal_logs.append(meal_log)

        self._meal = remaining_meal_logs

    # Here are the activity log related methods.
    def add_activity_log(self, activity_name, calories_burned, timestamp=None):
        """Method for adding an activity log."""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        new_activity_log = ActivityLog(None, activity_name, calories_burned, timestamp)
        self._activity.append(new_activity_log)

    def delete_activity_log(self, activity_log_id):
        """Method for deleting an activity log. AI-generated."""
        self._activity = [log for log in self._activity if log.id != activity_log_id]
