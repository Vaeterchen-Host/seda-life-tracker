# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Shared daily-status helpers for CLI and GUI."""

from model.class_user import User


# ---------------------------
# Daily status helpers
# These return plain dicts first, so CLI and GUI can use the same data easily.
# ---------------------------
def get_today_water_status(user: User):
    """Return today's water status as plain data. AI-generated."""
    return {
        "intake": user.water_log_handler.water_intake_today(),
        "target": user.daily_water_target,
        "difference": user.today_water_balance,
        "progress": user.today_water_progress,
    }


def get_today_calorie_status(user: User):
    """Return today's calorie status as plain data. AI-generated."""
    intake = user.today_calorie_intake
    burned = user.today_calories_burned
    net = user.today_net_calories
    target = user.daily_calorie_target
    difference = None if target is None else round(target - net, 2)
    return {
        "intake": intake,
        "burned": burned,
        "net": net,
        "target": target,
        "difference": difference,
    }
