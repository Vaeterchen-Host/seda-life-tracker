"""This file defines classes"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from datetime import datetime
from model.database import Database



# ai-generated content start: helper function for validating log lists.
def _validate_log_list(logs, log_type, label):
    """Validate that logs is a list containing only the expected log type."""
    if not isinstance(logs, list) or not all(isinstance(log, log_type) for log in logs):
        raise ValueError(f"{label} must be a list of {log_type.__name__} objects.")
    return logs


# All classes about food.


class NutrientSummary:
    """This class defines the nutrient summary of a food."""

    def __init__(
        self,
        calorie,
        fat,
        saturated_fat,
        carbohydrate,
        fibre,
        sugar,
        protein,
        salt,
        sodium,
    ):
        """This is the constructor of NutrientSummary."""
        self.calorie = calorie
        self.fat = fat
        self.saturated_fat = saturated_fat
        self.carbohydrate = carbohydrate
        self.fibre = fibre
        self.sugar = sugar
        self.protein = protein
        self.salt = salt
        self.sodium = sodium


class Food:
    """This class defines the food."""

    def __init__(self, food_id, name, food_type, nutrients_per_100g: NutrientSummary):
        """This is the constructor of Food."""
        self._id = food_id
        self._name = name
        self._type = food_type
        self.nutrients_per_100g = nutrients_per_100g


class MealItem:
    """This class defines the meal item."""

    def __init__(self, food: Food, amount_in_gram):
        """This is the constructor of MealItem."""
        self.food = food
        self.amount_in_gram = amount_in_gram


class Meal:
    """This class defines the meal."""

    def __init__(self, meal_id, name, items: list[MealItem]):
        """This is the constructor of Meal."""
        self._id = meal_id
        self._name = name
        self._items = items

    # Here are the meal related methods.
    def calculate_nutrient_summary(self):
        """Method for calculating the nutrient summary of the meal."""
        if not self._items:
            return NutrientSummary(0, 0, 0, 0, 0, 0, 0, 0, 0)

        total = {
            "calorie": 0,
            "fat": 0,
            "saturated_fat": 0,
            "carbohydrate": 0,
            "fibre": 0,
            "sugar": 0,
            "protein": 0,
            "salt": 0,
            "sodium": 0,
        }

        for item in self._items:
            factor = item.amount_in_gram / 100
            nutrients = item.food.nutrients_per_100g
            total["calorie"] += nutrients.calorie * factor
            total["fat"] += nutrients.fat * factor
            total["saturated_fat"] += nutrients.saturated_fat * factor
            total["carbohydrate"] += nutrients.carbohydrate * factor
            total["fibre"] += nutrients.fibre * factor
            total["sugar"] += nutrients.sugar * factor
            total["protein"] += nutrients.protein * factor
            total["salt"] += nutrients.salt * factor
            total["sodium"] += nutrients.sodium * factor

        return NutrientSummary(
            total["calorie"],
            total["fat"],
            total["saturated_fat"],
            total["carbohydrate"],
            total["fibre"],
            total["sugar"],
            total["protein"],
            total["salt"],
            total["sodium"],
        )

    def add_meal_item(self, meal_item):
        """Method for adding a meal item. (Later when DB exists)"""
        self._items.append(meal_item)


# All classes for logging


class FoodLog:
    """This class defines the food log."""

    def __init__(self, id, food, amount_in_gram, timestamp):
        """This is the constructor of FoodLog."""
        self._id = id
        self._food = food
        self._amount_in_gram = amount_in_gram
        self._timestamp = timestamp

    # Here are the food log related methods.
    @property
    def id(self):
        """This is the getter for id."""
        return self._id

    @id.setter
    def id(self, new_id):
        """This is the setter for id."""
        self._id = new_id

    def calculate_nutrient_summary(self):
        """Method for calculating the nutrient summary of the food log."""
        factor = self._amount_in_gram / 100
        nutrients = self._food.nutrients_per_100g
        return NutrientSummary(
            nutrients.calorie * factor,
            nutrients.fat * factor,
            nutrients.saturated_fat * factor,
            nutrients.carbohydrate * factor,
            nutrients.fibre * factor,
            nutrients.sugar * factor,
            nutrients.protein * factor,
            nutrients.salt * factor,
            nutrients.sodium * factor,
        )

    def create_daytime_object(self):
        """Method for creating a daytime object for the timestamp."""
        return datetime.fromisoformat(self._timestamp)


class MealLog:
    """This class defines the meal log."""

    def __init__(self, id, meal, amount_in_gram, timestamp):
        """This is the constructor of MealLog."""
        self._id = id
        self._meal = meal
        self._amount_in_gram = amount_in_gram
        self._timestamp = timestamp

    # Here are the meal log related methods.
    @property
    def id(self):
        """This is the getter for id."""
        return self._id

    @id.setter
    def id(self, new_id):
        """This is the setter for id."""
        self._id = new_id

    def calculate_nutrient_summary(self):
        """Method for calculating the nutrient summary of the meal log."""
        meal_summary = self._meal.calculate_nutrient_summary()
        factor = self._amount_in_gram / 100
        return NutrientSummary(
            meal_summary.calorie * factor,
            meal_summary.fat * factor,
            meal_summary.saturated_fat * factor,
            meal_summary.carbohydrate * factor,
            meal_summary.fibre * factor,
            meal_summary.sugar * factor,
            meal_summary.protein * factor,
            meal_summary.salt * factor,
            meal_summary.sodium * factor,
        )


class WaterLog:
    """This class defines the water log."""

    def __init__(self, id, amount_in_ml, timestamp):
        """This is the constructor of WaterLog."""
        self._id = id
        self.amount_in_ml = amount_in_ml  # refactored by ai
        self.timestamp = timestamp  # refactored by ai

    # Here are the water log related methods.
    @property
    def id(self):
        """This is the getter for id."""
        return self._id
    
    @id.setter
    def id(self, new_id):
        """This is the setter for id."""
        self._id = new_id

    @property
    def amount_in_ml(self):
        """This is the getter for amount_in_ml."""
        return self._amount_in_ml

    @amount_in_ml.setter
    def amount_in_ml(self, new_amount):
        """This is the setter for amount_in_ml."""
        if new_amount <= 0 or new_amount >= 2000:
            raise ValueError("Amount must be greater than 0 ml.")
        self._amount_in_ml = new_amount

    @property
    def timestamp(self):
        """This is the getter for timestamp."""
        return self._timestamp

    @timestamp.setter
    def timestamp(self, new_timestamp):
        """This is the setter for timestamp."""
        self._timestamp = new_timestamp

    # Here are the weight log related methods


class WeightLog:
    """This class defines weightlog."""

    def __init__(self, id, weight_in_kg, timestamp):
        """This is the constructor of weightlog."""
        self._id = id
        self.weight_in_kg = weight_in_kg  # refactored by ai
        self.timestamp = timestamp  # refactored by ai

    @property
    def id(self):
        """This is the getter for id."""
        return self._id

    @id.setter
    def id(self, new_id):
        """This is the setter for id."""
        self._id = new_id

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
    def timestamp(self):
        """This is the getter for timestamp."""
        return self._timestamp

    @timestamp.setter
    def timestamp(self, new_timestamp):
        """This is the setter for timestamp."""
        self._timestamp = new_timestamp


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
        food: list[FoodLog],
        meal: list[MealLog],
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
        self.food_logs = food  # refactored by ai
        self._meal = _validate_log_list(meal, MealLog, "Meal logs")  # refactored by ai

    # Here are the biometrical data related methods.
    @property
    def id(self):
        """This is the getter for id"""
        return self._id
    
    @id.setter
    def id(self, new_id):
        """This is the setter for id."""
        self._id = new_id

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
        self._water = _validate_log_list(new_water_logs, WaterLog, "Water logs")  # refactored by ai

    @property
    def weight_logs(self):
        """This is the getter for weight logs."""
        return self._weight
    
    @weight_logs.setter
    def weight_logs(self, new_weight_logs):
        """This is the setter for weight logs. Partly AI-generated."""
        self._weight = _validate_log_list(new_weight_logs, WeightLog, "Weight logs")  # refactored by ai

    @property
    def food_logs(self):
        """This is the getter for food logs."""
        return self._food
    
    @food_logs.setter
    def food_logs(self, new_food_logs):
        """This is the setter for food logs. Partly AI-generated."""
        self._food = _validate_log_list(new_food_logs, FoodLog, "Food logs")  # refactored by ai

    @property
    def meal_logs(self):
        """This is the getter for meal logs."""
        return self._meal

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
    def add_weight_log(self, id, weight_in_kg, timestamp=None):
        """Method for adding a weightlog."""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        new_weight_log = WeightLog(id, weight_in_kg, timestamp)
        self._weight.append(new_weight_log)

    def delete_weight_log(self, weight_log_id):
        """Method for deleting a weightlog. AI-generated."""
        remaining_weight_logs = []

        for weight_log in self._weight:
            if weight_log.id != weight_log_id:
                remaining_weight_logs.append(weight_log)

        self._weight = remaining_weight_logs


    def calculate_bmi(self):
        """Method for calculating the BMI."""
        if self.height_in_cm is None or not self._weight:
            return None
        height_in_m = self.height_in_cm / 100
        latest_weight = self._weight[-1].weight_in_kg
        bmi = latest_weight / (height_in_m**2)
        return bmi

    # Here are the water log related methods.
    def add_water_log(self, id, amount_in_ml, timestamp=None):
        """Method for adding a waterlog."""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        new_water_log = WaterLog(id, amount_in_ml, timestamp)
        self._water.append(new_water_log)

    def delete_water_log(self, water_log_id):
        """Method for deleting a waterlog. AI-generated."""
        remaining_water_logs = []

        for water_log in self._water:
            if water_log.id != water_log_id:
                remaining_water_logs.append(water_log)

        self._water = remaining_water_logs

    # Here are the food log related methods.
    def add_food_log(self, id, food, amount_in_gram, timestamp=None):
        """Method for adding a foodlog."""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        new_food_log = FoodLog(id, food, amount_in_gram, timestamp)
        self._food.append(new_food_log)

    def delete_food_log(self, food_log_id):
        """Method for deleting a foodlog. AI-generated."""
        remaining_food_logs = []

        for food_log in self._food:
            if food_log.id != food_log_id:
                remaining_food_logs.append(food_log)

        self._food = remaining_food_logs

    # Here are the meal log related methods.
    def add_meal_log(self, id, meal, amount_in_gram, timestamp=None):
        """Method for adding a meallog."""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        new_meal_log = MealLog(id, meal, amount_in_gram, timestamp)
        self._meal.append(new_meal_log)

    def delete_meal_log(self, meal_log_id):
        """Method for deleting a meallog. AI-generated."""
        remaining_meal_logs = []

        for meal_log in self._meal:
            if meal_log.id != meal_log_id:
                remaining_meal_logs.append(meal_log)

        self._meal = remaining_meal_logs
