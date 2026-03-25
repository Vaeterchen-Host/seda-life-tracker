"""CLI entry point for SEDA."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from model.classes import User, WaterLog, WeightLog
from model.database import Database
from ui import cli_view


def _user_from_row(user_row):
    """Create a User object from a database row."""
    return User(
        user_row[0],
        user_row[1],
        user_row[2],
        user_row[3],
        user_row[4],
        user_row[5],
        [],
        [],
        [],
        [],
    )


def _load_water_logs(db, user_id):
    """Load all water logs for one user as class objects."""
    water_logs = []
    for row in db.get_all_water_logs():
        if row[1] == user_id:
            water_logs.append(WaterLog(row[0], row[2], row[3]))
    return water_logs


def _load_weight_logs(db, user_id):
    """Load all weight logs for one user as class objects."""
    weight_logs = []
    for row in db.get_all_weight_logs():
        if row[1] == user_id:
            weight_logs.append(WeightLog(row[0], row[2], row[3]))
    return weight_logs


def _refresh_user_logs(db, user):
    """Refresh cached logs in the user object from the database."""
    user.water_logs = _load_water_logs(db, user.id)
    user.weight_logs = _load_weight_logs(db, user.id)


def _show_all_users(users):
    """Show all users from database rows."""
    for user_row in users:
        cli_view.show_message(
            f"""
            ID: {user_row[0]}
            Name: {user_row[1]}
            Birthdate: {user_row[2]}
            Height: {user_row[3]} cm
            Gender: {user_row[4]}
            Fitness level: {user_row[5]}
        """
        )


def _select_current_user(db):
    """Load an existing user or create a new one."""
    users = db.get_all_users()
    if not users:
        cli_view.show_message("No users found. Let's create a new user.")
        user = cli_view.create_user_by_input()
        db.add_user(
            user.name,
            user.birthdate,
            user.height_in_cm,
            user.gender,
            user.fitness_lvl,
        )
        users = db.get_all_users()
    else:
        cli_view.show_message("Existing user found:")
        _show_all_users(users)

    current_user = _user_from_row(users[0])
    _refresh_user_logs(db, current_user)
    return current_user


def main():
    """Run the CLI application."""
    db = Database()

    cli_view.show_message(
        """
    Welcome to SEDA - Your personal fitness assistant!
    Please follow the prompts.
    """
    )

    db_connection = db.connect()
    if db_connection is None:
        cli_view.show_message("Failed to connect to the database. Exiting.")
        sys.exit(1)
    db_connection.close()

    current_user = _select_current_user(db)

    while True:
        choice = cli_view.prompt_main_menu()

        if choice == "1":
            cli_view.show_user_info(current_user)
        elif choice == "2":
            amount_in_ml, timestamp = cli_view.create_water_log_by_input()
            current_user.add_water_log(None, amount_in_ml, timestamp)
            new_water_log = current_user.water_logs[-1]
            db.add_water_log(
                current_user.id, new_water_log.amount_in_ml, new_water_log.timestamp
            )
            _refresh_user_logs(db, current_user)
            cli_view.show_message("Water log added.")
        elif choice == "3":
            _refresh_user_logs(db, current_user)
            cli_view.show_water_logs(current_user.water_logs)
        elif choice == "4":
            water_log_id = int(input("Enter the water log ID to delete: "))
            current_user.delete_water_log(water_log_id)
            db.delete_water_log(water_log_id)
            _refresh_user_logs(db, current_user)
            cli_view.show_message("Water log deleted.")
        elif choice == "5":
            weight_in_kg, timestamp = cli_view.create_weight_log_by_input()
            current_user.add_weight_log(None, weight_in_kg, timestamp)
            new_weight_log = current_user.weight_logs[-1]
            db.add_weight_log(
                current_user.id, new_weight_log.weight_in_kg, new_weight_log.timestamp
            )
            _refresh_user_logs(db, current_user)
            cli_view.show_message("Weight log added.")
        elif choice == "6":
            _refresh_user_logs(db, current_user)
            cli_view.show_weight_logs(current_user.weight_logs)
        elif choice == "7":
            weight_log_id = int(input("Enter the weight log ID to delete: "))
            current_user.delete_weight_log(weight_log_id)
            db.delete_weight_log(weight_log_id)
            _refresh_user_logs(db, current_user)
            cli_view.show_message("Weight log deleted.")
        elif choice == "8":
            cli_view.show_message("Change user information is not implemented yet.")
        elif choice == "9":
            cli_view.show_message("Exiting SEDA. Goodbye!")
            break
        else:
            cli_view.show_message("Invalid choice. Please enter a number between 1 and 9.")


if __name__ == "__main__":
    main()
