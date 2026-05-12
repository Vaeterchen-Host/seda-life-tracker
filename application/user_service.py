# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Shared user-loading and refresh helpers for CLI and GUI."""

from model.class_user import User
from model.database import Database

from application.builders import (
    create_activity_log_instances_for_user,
    create_meal_log_instances_for_user,
    create_water_log_instances_for_user,
    create_weight_log_instances_for_user,
)


# ---------------------------
# User loading and refresh
# These functions create the current user and keep the in-memory handlers in sync with the DB.
# ---------------------------
def refresh_water_logs_from_db(main_db: Database, user: User):
    """Refresh the water logs from DB into the current user object."""
    user.water_log_handler.logs = create_water_log_instances_for_user(
        main_db, user.user_id
    )


def refresh_weight_logs_from_db(main_db: Database, user: User):
    """Refresh the weight logs from DB into the current user object."""
    user.weight_log_handler.logs = create_weight_log_instances_for_user(
        main_db, user.user_id
    )


def refresh_meal_logs_from_db(main_db: Database, user: User):
    """Refresh the meal logs from DB into the current user object."""
    user.meal_log_handler.logs = create_meal_log_instances_for_user(
        main_db, user.user_id
    )


def refresh_activity_logs_from_db(main_db: Database, user: User):
    """Refresh the activity logs from DB into the current user object."""
    user.activity_log_handler.logs = create_activity_log_instances_for_user(
        main_db, user.user_id
    )


def refresh_user_logs_from_db(main_db: Database, user: User):
    """Refresh all log handlers of the current user from DB."""
    refresh_water_logs_from_db(main_db, user)
    refresh_weight_logs_from_db(main_db, user)
    refresh_meal_logs_from_db(main_db, user)
    refresh_activity_logs_from_db(main_db, user)
