# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Database layer for SEDA."""

import sqlite3
from config import DB_PATH


def connector(func):
    """This is a decorator for connecting and disconnecting to DB."""

    # minor ai-generated fixes
    def wrapper(self, *args, **kwargs):
        """This is the wrapper function for the decorator."""
        conn = self.connect()
        result = func(self, conn, *args, **kwargs)
        self.end_connection(conn)
        return result

    return wrapper


class Database:
    """This class defines the Database."""

    def __init__(self, db=DB_PATH):
        """This is the constructor of the Database."""
        self._db = db
        self.create_tables()

    def connect(self):
        """This method connects to the database."""
        conn = sqlite3.connect(self._db)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def create_tables(self):
        """This method creates the tables in the database. Further tables can be added here."""
        self.create_user_table()  # pylint: disable=no-value-for-parameter
        self.create_water_log_table()  # pylint: disable=no-value-for-parameter
        self.create_weight_log_table()  # pylint: disable=no-value-for-parameter
        self.create_activity_log_table()  # pylint: disable=no-value-for-parameter
        self.create_food_table()  # pylint: disable=no-value-for-parameter
        self.create_food_log_table()  # pylint: disable=no-value-for-parameter
        self.create_meal_table()  # pylint: disable=no-value-for-parameter
        self.create_meal_item_table()  # pylint: disable=no-value-for-parameter
        self.create_meal_log_table()  # pylint: disable=no-value-for-parameter

    def end_connection(self, conn):
        """This method ends the connection to the database."""
        conn.close()

    # Here are the user related methods.
    @connector
    def create_user_table(self, conn):
        """This method creates a users table"""
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                       user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_name TEXT NOT NULL,
                       date_of_birth TEXT NOT NULL,
                       height INTEGER NOT NULL CHECK(height > 0 AND height <= 250),
                       gender TEXT NOT NULL CHECK(gender IN ('m', 'f', 'd')),
                       fitness_lvl TEXT NOT NULL CHECK(fitness_lvl IN ('beginner', 'intermediate', 'advanced'))
            )"""
        )
        conn.commit()

    @connector
    def add_user(self, conn, name, birthdate, height_in_cm, gender, fitness_lvl):
        """This method adds a user to the db."""
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (user_name, date_of_birth, height,  gender, fitness_lvl) VALUES (?, ?, ?, ?, ?)",
            (name, birthdate, height_in_cm, gender, fitness_lvl),
        )
        conn.commit()

    @connector
    def get_user(self, conn, name) -> list:
        """This method retrieves a user from database."""
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ?", (name,))
        row = cursor.fetchone()
        return row

    @connector
    def get_all_users(self, conn) -> list:
        """This method retrieves all users from the database."""
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    @connector
    def delete_user(self, conn, name) -> int:
        """This method deletes a user from database."""
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_name = ?", (name,))
        conn.commit()
        return cursor.rowcount

    @connector
    def update_user(
        self, conn, user_id, name, birthdate, height_in_cm, gender, fitness_lvl
    ):
        """This method updates a user's information in the database. Partly AI-generated."""
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users
            SET user_name = ?, date_of_birth = ?, height = ?, gender = ?, fitness_lvl = ?
            WHERE user_id = ?
            """,
            (name, birthdate, height_in_cm, gender, fitness_lvl, user_id),
        )
        conn.commit()

    # Here are the waterlog related methods.

    @connector
    def create_water_log_table(self, conn):
        """This method creates the water logs table in the database."""
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS water_logs (
                       water_log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id INTEGER NOT NULL,
                       amount_in_ml INTEGER NOT NULL,
                       timestamp TEXT NOT NULL,
                       FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )"""
        )
        conn.commit()

    @connector
    def add_water_log(self, conn, user_id, amount_in_ml, timestamp):
        """This method adds a water logs to the database. Code partly AI-generated."""
        cursor = conn.cursor()
        # The '?' is a placeholder.
        cursor.execute(
            "INSERT INTO water_logs (user_id, amount_in_ml, timestamp) VALUES (?, ?, ?)",
            (user_id, amount_in_ml, timestamp),
        )
        conn.commit()

    @connector
    def get_all_water_logs(self, conn) -> list:
        """This method retrieves all water logs from the database."""
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM water_logs")
        rows = cursor.fetchall()
        return rows

    @connector
    def delete_water_log(self, conn, water_log_id) -> int:
        """This method deletes a water log from the database."""
        cursor = conn.cursor()
        cursor.execute("DELETE FROM water_logs WHERE water_log_id = ?", (water_log_id,))
        conn.commit()
        return cursor.rowcount

    # Here are the weightlog related methods. (BINE)
    @connector
    def create_weight_log_table(self, conn):
        """This method creates the weight logs table in the database."""
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS weight_logs (
                       weight_log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id INTEGER NOT NULL,
                       weight_in_kg DECIMAL NOT NULL,
                       timestamp TEXT NOT NULL,
                       FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )"""
        )
        conn.commit()

    @connector
    def add_weight_log(self, conn, user_id, weight_in_kg, timestamp):
        """This method adds a weight logs to the database. Code partly AI-generated."""
        cursor = conn.cursor()
        # The '?' is a placeholder.
        cursor.execute(
            "INSERT INTO weight_logs (user_id, weight_in_kg, timestamp) VALUES (?, ?, ?)",
            (user_id, weight_in_kg, timestamp),
        )
        conn.commit()

    @connector
    def get_all_weight_logs(self, conn) -> list:
        """This method retrieves all weight logs from the database."""
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM weight_logs")
        rows = cursor.fetchall()
        return rows

    @connector
    def delete_weight_log(self, conn, weight_log_id) -> int:
        """This method deletes a weight log from the database."""
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM weight_logs WHERE weight_log_id = ?", (weight_log_id,)
        )
        conn.commit()
        return cursor.rowcount
    
    # Here are the activity log related methods.
    @connector
    def create_activity_log_table(self, conn):
        """This method creates the activity logs table."""
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS activity_logs (
                       activity_log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id INTEGER NOT NULL,
                       activity_name TEXT NOT NULL,
                       calories_burned REAL NOT NULL CHECK(calories_burned >= 0),
                       timestamp TEXT NOT NULL,
                       FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )"""
        )
        conn.commit()

    @connector
    def add_activity_log(self, conn, user_id, activity_name, calories_burned, timestamp):
        """Adds an activity entry to the database."""
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO activity_logs (user_id, activity_name, calories_burned, timestamp) VALUES (?, ?, ?, ?)",
            (user_id, activity_name, calories_burned, timestamp),
        )
        conn.commit()  

    @connector
    def get_all_activity_logs(self, conn) -> list:
        """This method retrieves all activity logs from the database."""
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activity_logs")
        rows = cursor.fetchall()
        return rows

    @connector
    def delete_activity_log(self, conn, activity_log_id) -> int:
        """This method deletes an activity log from the database."""
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM activity_logs WHERE activity_log_id = ?", (activity_log_id,)
        )
        conn.commit()
        return cursor.rowcount

    # Here are the food related methods.
    @connector
    def create_food_table(self, conn):
        """This method creates the food master data table based on the NutrientSummary."""
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS foods (
                food_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                food_type TEXT NOT NULL,
                calorie INTEGER NOT NULL,
                fat REAL NOT NULL,
                saturated_fat REAL NOT NULL,
                carbohydrate REAL NOT NULL,
                fibre REAL NOT NULL,
                sugar REAL NOT NULL,
                protein REAL NOT NULL,
                salt REAL NOT NULL,
                sodium REAL NOT NULL
            )"""
        )
        conn.commit()

    @connector
    def add_food(self, conn, name, food_type, nutrients: dict):
        """Adds a new food item. Expects nutrients as a dict matching NutrientSummary."""
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO foods (
                name, food_type, calorie, fat, saturated_fat, carbohydrate, 
                fibre, sugar, protein, salt, sodium
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                name, food_type, 
                nutrients['calorie'], nutrients['fat'], nutrients['saturated_fat'],
                nutrients['carbohydrate'], nutrients['fibre'], nutrients['sugar'],
                nutrients['protein'], nutrients['salt'], nutrients['sodium']
            )
        )
        conn.commit()

    @connector
    def get_all_foods(self, conn):
        """Retrieves all available foods."""
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM foods ORDER BY name ASC")
        return cursor.fetchall()

    @connector
    def delete_food(self, conn, food_id):
        """Deletes a food item by ID."""
        cursor = conn.cursor()
        cursor.execute("DELETE FROM foods WHERE food_id = ?", (food_id,))
        conn.commit()
        return cursor.rowcount

    # Here are the food log related methods.
    @connector
    def create_food_log_table(self, conn):
        """Creates the table for logging food consumption."""
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS food_logs (
                food_log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                food_id INTEGER NOT NULL,
                amount_in_gram REAL NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                FOREIGN KEY (food_id) REFERENCES foods (food_id) ON DELETE CASCADE
            )
            """
        )
        conn.commit()

    @connector
    def add_food_log(self, conn, user_id, food_id, amount_in_gram, timestamp):
        """Adds a new entry to the food log."""
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO food_logs (user_id, food_id, amount_in_gram, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, food_id, amount_in_gram, timestamp),
        )
        conn.commit()

    @connector
    def get_user_food_logs(self, conn, user_id):
        """Retrieves all food log entries for a specific user with food names."""
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT fl.food_log_id, fl.food_id, f.name, fl.amount_in_gram, fl.timestamp
            FROM food_logs fl
            JOIN foods f ON fl.food_id = f.food_id
            WHERE fl.user_id = ?
            ORDER BY fl.timestamp DESC
            """,
            (user_id,),
        )
        return cursor.fetchall()

    @connector
    def delete_food_log(self, conn, food_log_id):
        """Deletes a specific food log entry."""
        cursor = conn.cursor()
        cursor.execute("DELETE FROM food_logs WHERE food_log_id = ?", (food_log_id,))
        conn.commit()
        return cursor.rowcount

    # Here are the meal related methods.
    @connector
    def create_meal_table(self, conn):
        """Creates the table for meal templates."""
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS meals (
                meal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
            """
        )
        conn.commit()

    @connector
    def add_meal(self, conn, name):
        """Adds a new meal template and returns its ID."""
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO meals (name) VALUES (?)",
            (name,)
        )
        conn.commit()
        return cursor.lastrowid # "lastrowid" returns the new ID to immediately link ingredients (MealItems) to this meal

    @connector
    def get_all_meals(self, conn):
        """Retrieves all meal templates from the database."""
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM meals ORDER BY name ASC")
        return cursor.fetchall()

    @connector
    def delete_meal(self, conn, meal_id):
        """Deletes a meal template by its ID."""
        cursor = conn.cursor()
        cursor.execute("DELETE FROM meals WHERE meal_id = ?", (meal_id,))
        conn.commit()
        return cursor.rowcount

    # Here are the meal item related methods.
    @connector
    def create_meal_item_table(self, conn):
        """Creates the table that links foods to meals (ingredients)."""
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS meal_items (
                meal_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                meal_id INTEGER NOT NULL,
                food_id INTEGER NOT NULL,
                amount_in_gram REAL NOT NULL,
                FOREIGN KEY (meal_id) REFERENCES meals (meal_id) ON DELETE CASCADE,
                FOREIGN KEY (food_id) REFERENCES foods (food_id) ON DELETE CASCADE
            )
            """
        )
        conn.commit()

    @connector
    def add_meal_item(self, conn, meal_id, food_id, amount_in_gram):
        """Adds a food item (ingredient) to a specific meal."""
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO meal_items (meal_id, food_id, amount_in_gram)
            VALUES (?, ?, ?)
            """,
            (meal_id, food_id, amount_in_gram),
        )
        conn.commit()

    @connector
    def get_meal_items(self, conn, meal_id):
        """Retrieves all ingredients for a specific meal including food details."""
        cursor = conn.cursor()
        # Joining with foods to get nutrient data and name for the MealItem objects
        cursor.execute(
            """
            SELECT mi.meal_item_id, mi.food_id, f.name, mi.amount_in_gram, f.calorie, 
                   f.fat, f.saturated_fat, f.carbohydrate, f.fibre, f.sugar, 
                   f.protein, f.salt, f.sodium
            FROM meal_items mi
            JOIN foods f ON mi.food_id = f.food_id
            WHERE mi.meal_id = ?
            """,
            (meal_id,),
        )
        return cursor.fetchall()
    
    # Here are the meal log related methods.
    @connector
    def create_meal_log_table(self, conn):
        """Creates the table for logging consumed meals."""
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS meal_logs (
                meal_log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                meal_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                FOREIGN KEY (meal_id) REFERENCES meals (meal_id) ON DELETE CASCADE
            )
            """
        )
        conn.commit()

    @connector
    def add_meal_log(self, conn, user_id, meal_id, timestamp):
        """Adds a meal consumption entry to the log."""
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO meal_logs (user_id, meal_id, timestamp)
            VALUES (?, ?, ?)
            """,
            (user_id, meal_id, timestamp),
        )
        conn.commit()

    @connector
    def get_user_meal_logs(self, conn, user_id):
        """Retrieves all meal log entries for a specific user with meal names."""
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT ml.meal_log_id, ml.meal_id, m.name, ml.timestamp
            FROM meal_logs ml
            JOIN meals m ON ml.meal_id = m.meal_id
            WHERE ml.user_id = ?
            ORDER BY ml.timestamp DESC
            """,
            (user_id,),
        )
        return cursor.fetchall()

    @connector
    def delete_meal_log(self, conn, meal_log_id):
        """Deletes a specific meal log entry."""
        cursor = conn.cursor()
        cursor.execute("DELETE FROM meal_logs WHERE meal_log_id = ?", (meal_log_id,))
        conn.commit()
        return cursor.rowcount
