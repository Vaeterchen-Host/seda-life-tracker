# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Tests for the CLI view."""

import builtins
import sqlite3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# pylint: disable=C0413
from model.class_user import User
from ui import cli_view


def test_change_user_information_allows_name_change(monkeypatch):
    """Changing user information should also allow changing the name. AI-generated."""
    user = User(
        1,
        "Old Name",
        "2000-02-22",
        185,
        "m",
        "beginner",
        [],
        [],
        [],
        [],
    )
    answers = iter(
        [
            "New Name",
            "2001-03-03",
            "190",
            "d",
            "advanced",
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda prompt: next(answers))

    result = cli_view.change_user_information(user)

    assert result == ("New Name", "2001-03-03", 190, "d", "advanced")


def test_example_query_displays_unit_type(capsys):
    """The food example query should show the unit type from the external DB."""
    conn = sqlite3.connect(Path(__file__).resolve().parents[1] / "data" / "bls_foods.sqlite")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT name_de, unit_type
        FROM foods
        WHERE name_de IS NOT NULL AND TRIM(name_de) != ''
          AND unit_type IS NOT NULL AND TRIM(unit_type) != ''
        ORDER BY food_id ASC
        LIMIT 1
        """
    )
    row = cursor.fetchone()
    conn.close()

    assert row is not None, "Expected at least one food with name_de and unit_type."

    food_name, unit_type = row

    cli_view.example_query(food_name)

    output = capsys.readouterr().out
    assert f"Unit type: {unit_type}" in output
