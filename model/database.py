# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Database layer for SEDA."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# pylint: disable=C0413, E1120, C0301
import sqlite3
from config import DB_PATH, FOOD_DB_PATH


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


# added class for Food-DB, which is static. It will coexist with the(main-)DB and the OFF API calls.
# The DB must be read-only(!), so we only need methods for fetching data.

FOOD_DB_TEST_QUERY = """
PRAGMA table_info(foods);
"""


class FoodDatabase:
    """This class defines the Food_Database. Read-only!"""

    def __init__(self, db=FOOD_DB_PATH):
        """This is the constructor of the Food_Database."""
        self._db = db

    def connect(self):
        """This method connects to the food database."""
        conn = sqlite3.connect(self._db)
        conn.row_factory = sqlite3.Row  # refactored by ai
        return conn

    def end_connection(self, conn):
        """This method ends the connection to the food database."""
        conn.close()

    @connector
    def get_one_food_by_name_en(self, conn, food_name):
        """This method retrieves a food item from the database by its name."""
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM foods WHERE name_en = ?", (food_name,))
        return cursor.fetchone()

    @connector
    def get_query_food_by_name_en(self, conn, food_name):
        """This method retrieves a list of food items from the database that match the query name."""
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM foods WHERE name_en LIKE ?", (f"%{food_name}%",))
        return cursor.fetchall()

    @connector
    def search_foods(self, conn, food_name):
        """Search foods by German or English name. ai-generated."""
        cursor = conn.cursor()
        search_term = food_name.strip().lower()  # ai-generated
        cursor.execute(
            """
            SELECT *
            FROM foods
            WHERE lower(COALESCE(name_de, '')) LIKE ? OR lower(COALESCE(name_en, '')) LIKE ?
            ORDER BY
                CASE
                    WHEN lower(COALESCE(name_de, '')) = ? OR lower(COALESCE(name_en, '')) = ? THEN 0
                    WHEN lower(COALESCE(name_de, '')) LIKE ? OR lower(COALESCE(name_en, '')) LIKE ? THEN 1
                    ELSE 2
                END,
                LENGTH(COALESCE(name_de, name_en)) ASC,
                COALESCE(name_de, name_en) COLLATE NOCASE ASC
            LIMIT 20
            """,
            (
                f"%{search_term}%",
                f"%{search_term}%",
                search_term,
                search_term,
                f"{search_term}%",
                f"{search_term}%",
            ),
        )
        return cursor.fetchall()

    @connector
    def get_food_by_id(self, conn, food_id):
        """Retrieve one food row by id. ai-generated."""
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM foods WHERE food_id = ?", (food_id,))
        return cursor.fetchone()

    @connector
    def custom_sql_query(self, conn, query):
        """This method allows for custom SQL queries to be executed on the food database."""
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


# for dev and testing purposes.
if __name__ == "__main__":
    food_db = FoodDatabase()
    results = food_db.custom_sql_query(FOOD_DB_TEST_QUERY)
    for row in results:
        print(row)


# The main Database class for everything else.
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
        # No local foods table is created anymore. ai-refactored, due to food-db
        self.create_meal_table()  # pylint: disable=no-value-for-parameter
        self.create_meal_food_item_table()  # pylint: disable=no-value-for-parameter
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
        return cursor.lastrowid  # refactored by ai

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
    def delete_user_by_id(self, conn, user_id) -> int:
        """This method deletes a user by ID from database. ai-generated."""
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
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
            """
            INSERT INTO water_logs (user_id, amount_in_ml, timestamp)
            VALUES (?, ?, ?)
            """,
            (user_id, amount_in_ml, timestamp),
        )
        conn.commit()
        return cursor.lastrowid  # refactored by ai

    @connector
    def get_all_water_logs(self, conn) -> list:
        """This method retrieves all water logs from the database."""
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT water_log_id, user_id, amount_in_ml, timestamp
            FROM water_logs
            """
        )
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
                       height_in_cm INTEGER,
                       timestamp TEXT NOT NULL,
                       FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )"""
        )
        conn.commit()

    @connector
    def add_weight_log(self, conn, user_id, weight_in_kg, height_in_cm=None, timestamp=None):
        """This method adds a weight logs to the database. Code partly AI-generated."""
        cursor = conn.cursor()
        # The '?' is a placeholder.
        cursor.execute(
            """
            INSERT INTO weight_logs
            (user_id, weight_in_kg, height_in_cm, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, weight_in_kg, height_in_cm, timestamp),
        )
        conn.commit()
        return cursor.lastrowid  # refactored by ai

    @connector
    def get_all_weight_logs(self, conn) -> list:
        """This method retrieves all weight logs from the database."""
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT weight_log_id, user_id, weight_in_kg, height_in_cm, timestamp
            FROM weight_logs
            """
        )
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
                       activity_value REAL,
                       unit_type TEXT NOT NULL CHECK(unit_type = 'minutes'),
                       timestamp TEXT NOT NULL,
                       FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )"""
        )
        conn.commit()

    @connector
    def add_activity_log(
        self,
        conn,
        user_id,
        activity_name,
        calories_burned,
        activity_value=None,
        unit_type="minutes",
        timestamp=None,
    ):
        """Adds an activity entry to the database."""
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO activity_logs
            (user_id, activity_name, calories_burned, activity_value, unit_type, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                activity_name,
                calories_burned,
                activity_value,
                unit_type,
                timestamp,
            ),
        )
        conn.commit()
        return cursor.lastrowid  # refactored by ai

    @connector
    def get_all_activity_logs(self, conn) -> list:
        """This method retrieves all activity logs from the database."""
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                activity_log_id,
                user_id,
                activity_name,
                calories_burned,
                activity_value,
                unit_type,
                timestamp
            FROM activity_logs
            """
        )
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

    @connector
    def update_activity_log(
        self,
        conn,
        activity_log_id,
        activity_name,
        calories_burned,
        activity_value=None,
        unit_type="minutes",
        timestamp=None,
    ):
        """Update an activity entry in the database. ai-generated."""
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE activity_logs
            SET activity_name = ?, calories_burned = ?, activity_value = ?, unit_type = ?, timestamp = ?
            WHERE activity_log_id = ?
            """,
            (
                activity_name,
                calories_burned,
                activity_value,
                unit_type,
                timestamp,
                activity_log_id,
            ),
        )
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
        cursor.execute("INSERT INTO meals (name) VALUES (?)", (name,))
        conn.commit()
        return (
            cursor.lastrowid
        )  # "lastrowid" returns the new ID to immediately link ingredients (MealItems) to this meal

    @connector
    def get_all_meals(self, conn):
        """Retrieves all meal templates from the database."""
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM meals ORDER BY name ASC")
        return cursor.fetchall()

    @connector
    def get_meal_by_id(self, conn, meal_id):
        """Retrieve one meal template by ID. ai-generated."""
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM meals WHERE meal_id = ?", (meal_id,))
        return cursor.fetchone()

    @connector
    def update_meal(self, conn, meal_id, name):
        """Update a meal template name. ai-generated."""
        cursor = conn.cursor()
        cursor.execute("UPDATE meals SET name = ? WHERE meal_id = ?", (name, meal_id))
        conn.commit()
        return cursor.rowcount

    @connector
    def delete_meal(self, conn, meal_id):
        """Deletes a meal template by its ID."""
        cursor = conn.cursor()
        cursor.execute("DELETE FROM meals WHERE meal_id = ?", (meal_id,))
        conn.commit()
        return cursor.rowcount

    # Here are the meal food item related methods.
    @connector
    def create_meal_food_item_table(self, conn):
        """Creates the table that links foods to meals (ingredients)."""
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS meal_food_items (
                meal_food_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                meal_id INTEGER NOT NULL,
                food_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                unit_type TEXT NOT NULL CHECK(unit_type IN ('g', 'ml')),
                FOREIGN KEY (meal_id) REFERENCES meals (meal_id) ON DELETE CASCADE
            )
            """
        )
        conn.commit()

    @connector
    def add_meal_food_item(self, conn, meal_id, food_id, amount, unit_type="g"):
        """Adds a food item (ingredient) to a specific meal."""
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO meal_food_items (meal_id, food_id, amount, unit_type)
            VALUES (?, ?, ?, ?)
            """,
            (meal_id, food_id, amount, unit_type),
        )
        conn.commit()
        return cursor.lastrowid  # refactored by ai

    @connector
    def delete_meal_food_items(self, conn, meal_id):
        """Delete all food items of one meal template. ai-generated."""
        cursor = conn.cursor()
        cursor.execute("DELETE FROM meal_food_items WHERE meal_id = ?", (meal_id,))
        conn.commit()
        return cursor.rowcount

    @connector
    def get_meal_food_items(self, conn, meal_id):
        """Retrieves all ingredients for a specific meal including food details."""
        cursor = conn.cursor()
        # Join meal food items against the external BLS food database. ai-refactored, due to food-db
        cursor.execute("ATTACH DATABASE ? AS food_db", (str(FOOD_DB_PATH),))
        try:
            cursor.execute(
                """
                SELECT
                    mfi.meal_food_item_id,
                    mfi.food_id,
                    COALESCE(f.name_de, f.name_en) AS name,
                    mfi.amount,
                    mfi.unit_type,
                    f.kcal AS calorie,
                    f.fat,
                    f.saturated_fat,
                    f.carbohydrate,
                    f.fibre,
                    f.sugar,
                    f.protein,
                    f.salt,
                    f.sodium
                FROM meal_food_items mfi
                LEFT JOIN food_db.foods f ON mfi.food_id = f.food_id
                WHERE mfi.meal_id = ?
                """,
                (meal_id,),
            )
            rows = cursor.fetchall()
        finally:
            cursor.execute("DETACH DATABASE food_db")
        return rows

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
                amount REAL NOT NULL,
                unit_type TEXT NOT NULL CHECK(unit_type IN ('g', 'ml')),
                timestamp TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                FOREIGN KEY (meal_id) REFERENCES meals (meal_id) ON DELETE CASCADE
            )
            """
        )
        conn.commit()

    @connector
    def add_meal_log(self, conn, user_id, meal_id, amount, unit_type="g", timestamp=None):
        """Adds a meal consumption entry to the log."""
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO meal_logs (user_id, meal_id, amount, unit_type, timestamp)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, meal_id, amount, unit_type, timestamp),
        )
        conn.commit()
        return cursor.lastrowid  # refactored by ai

    @connector
    def get_user_meal_logs(self, conn, user_id):
        """Retrieves all meal log entries for a specific user with meal names."""
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                ml.meal_log_id,
                ml.user_id,
                ml.meal_id,
                m.name,
                ml.amount,
                ml.unit_type,
                ml.timestamp
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

    @connector
    def update_meal_log(self, conn, meal_log_id, meal_id, amount, unit_type="g", timestamp=None):
        """Update a meal log entry. ai-generated."""
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE meal_logs
            SET meal_id = ?, amount = ?, unit_type = ?, timestamp = ?
            WHERE meal_log_id = ?
            """,
            (meal_id, amount, unit_type, timestamp, meal_log_id),
        )
        conn.commit()
        return cursor.rowcount
