"""This file defines classes"""

from datetime import datetime


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
        self._calorie = calorie
        self._fat = fat
        self._saturated_fat = saturated_fat
        self._carbohydrate = carbohydrate
        self._fibre = fibre
        self._sugar = sugar
        self._protein = protein
        self._salt = salt
        self._sodium = sodium


class Food:
    """This class defines the food."""

    def __init__(self, food_id, name, food_type, nutrients_per_100g: NutrientSummary):
        """This is the constructor of Food."""
        self._id = food_id
        self._name = name
        self._type = food_type
        self._nutrients_per_100g = nutrients_per_100g


class MealItem:
    """This class defines the meal item."""

    def __init__(self, food: Food, amount_in_gramm):
        """This is the constructor of MealItem."""
        self._food = food
        self._amount_in_gramm = amount_in_gramm


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
            factor = item._amount_in_gramm / 100
            nutrients = item._food._nutrients_per_100g
            total["calorie"] += nutrients._calorie * factor
            total["fat"] += nutrients._fat * factor
            total["saturated_fat"] += nutrients._saturated_fat * factor
            total["carbohydrate"] += nutrients._carbohydrate * factor
            total["fibre"] += nutrients._fibre * factor
            total["sugar"] += nutrients._sugar * factor
            total["protein"] += nutrients._protein * factor
            total["salt"] += nutrients._salt * factor
            total["sodium"] += nutrients._sodium * factor

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

    def __init__(self, food, amount_in_gramm, timestamp):
        """This is the constructor of FoodLog."""
        self._id = None
        self._food = food
        self._amount_in_gramm = amount_in_gramm
        self._timestamp = timestamp

    # Here are the food log related methods.
    def calculate_nutrient_summary(self):
        """Method for calculating the nutrient summary of the food log."""
        factor = self._amount_in_gramm / 100
        nutrients = self._food._nutrients_per_100g
        return NutrientSummary(
            nutrients._calorie * factor,
            nutrients._fat * factor,
            nutrients._saturated_fat * factor,
            nutrients._carbohydrate * factor,
            nutrients._fibre * factor,
            nutrients._sugar * factor,
            nutrients._protein * factor,
            nutrients._salt * factor,
            nutrients._sodium * factor,
        )

    def create_daytime_object(self):
        """Method for creating a daytime object for the timestamp."""
        return datetime.fromisoformat(self._timestamp)


class MealLog:
    """This class defines the meal log."""

    def __init__(self, meal, amount_in_gramm, timestamp):
        """This is the constructor of MealLog."""
        self._id = None
        self._meal = meal
        self._amount_in_gramm = amount_in_gramm
        self._timestamp = timestamp

    # Here are the meal log related methods.
    def calculate_nutrient_summary(self):
        """Method for calculating the nutrient summary of the meal log."""
        meal_summary = self._meal.calculate_nutrient_summary()
        factor = self._amount_in_gramm / 100
        return NutrientSummary(
            meal_summary._calorie * factor,
            meal_summary._fat * factor,
            meal_summary._saturated_fat * factor,
            meal_summary._carbohydrate * factor,
            meal_summary._fibre * factor,
            meal_summary._sugar * factor,
            meal_summary._protein * factor,
            meal_summary._salt * factor,
            meal_summary._sodium * factor,
        )


class WaterLog:
    """This class defines the water log."""

    def __init__(self, amount_in_ml, timestamp):
        """This is the constructor of WaterLog."""
        self._id = None
        self._amount_in_ml = amount_in_ml
        self._timestamp = timestamp

    # Here are the water log related methods.
    @property
    def amount_in_ml(self):
        """This is the getter for amount_in_ml."""
        return self._amount_in_ml

    @amount_in_ml.setter
    def amount_in_ml(self, new_amount):
        """This is the setter for amount_in_ml."""
        if new_amount <= 0:
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


class WeightLog:
    """This class defines weightlog."""

    def __init__(self, weight_in_kg, timestamp):
        """This is the constructor of weightlog."""
        self._id = None
        self._weight_in_kg = weight_in_kg
        self._timestamp = timestamp

    # Here are the weight log related methods.
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
        self._id = None
        self._name = name
        self._birthdate = birthdate
        self._height_in_cm = height_in_cm
        self._gender = gender
        self._fitness_lvl = fitness_lvl
        self._water = water
        self._weight = weight
        self._food = food
        self._meal = meal

    # Here are the biometrical data related methods.
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
        new_weight_log = WeightLog(weight_in_kg, timestamp)
        self._weight.append(new_weight_log)

    def delete_weight_log(self, weight_log_id):
        """Method for deleting a weightlog."""
        self._weight = [log for log in self._weight if log._id != weight_log_id]

    def calculate_bmi(self):
        """Method for calculating the BMI."""
        if self.height_in_cm is None or not self._weight:
            return None
        height_in_m = self.height_in_cm / 100
        latest_weight = self._weight[-1].weight_in_kg
        bmi = latest_weight / (height_in_m**2)
        return bmi

    # Here are the water log related methods.
    def add_water_log(self, amount_in_ml, timestamp=None):
        """Method for adding a waterlog."""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        new_water_log = WaterLog(amount_in_ml, timestamp)
        self._water.append(new_water_log)

    def delete_water_log(self, water_log_id):
        """Method for deleting a waterlog."""
        self._water = [log for log in self._water if log._id != water_log_id]

    # Here are the food log related methods.
    def add_food_log(self, food, amount_in_gramm, timestamp=None):
        """Method for adding a foodlog."""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        new_food_log = FoodLog(food, amount_in_gramm, timestamp)
        self._food.append(new_food_log)

    def delete_food_log(self, food_log_id):
        """Method for deleting a foodlog."""
        self._food = [log for log in self._food if log._id != food_log_id]

    # Here are the meal log related methods.
    def add_meal_log(self, meal, amount_in_gramm, timestamp=None):
        """Method for adding a meallog."""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        new_meal_log = MealLog(meal, amount_in_gramm, timestamp)
        self._meal.append(new_meal_log)

    def delete_meal_log(self, meal_log_id):
        """Method for deleting a meallog."""
        self._meal = [log for log in self._meal if log._id != meal_log_id]
