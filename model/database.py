"""This module defines everything that is needed for the database."""

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
        self.create_weight_log_table()  # pylint: disable=no-value-for-parameter
    
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
        cursor.execute("DELETE FROM weight_logs WHERE weight_log_id = ?", (weight_log_id,))
        conn.commit()
        return cursor.rowcount
