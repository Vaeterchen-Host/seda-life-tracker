# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Tests for local GUI settings persistence. AI-generated."""

import json

from config import DEFAULT_GUI_SETTINGS, get_gui_settings, update_gui_settings


def test_get_gui_settings_returns_defaults_for_missing_file(tmp_path):
    """Missing GUI settings files should fall back to defaults and be created."""
    settings_path = tmp_path / "gui_settings.json"

    settings = get_gui_settings(settings_path)

    assert settings == DEFAULT_GUI_SETTINGS
    assert json.loads(settings_path.read_text(encoding="utf-8")) == DEFAULT_GUI_SETTINGS


def test_get_gui_settings_recovers_from_invalid_json(tmp_path):
    """Invalid GUI settings files should be replaced with valid defaults."""
    settings_path = tmp_path / "gui_settings.json"
    settings_path.write_text("{invalid json", encoding="utf-8")

    settings = get_gui_settings(settings_path)

    assert settings == DEFAULT_GUI_SETTINGS
    assert json.loads(settings_path.read_text(encoding="utf-8")) == DEFAULT_GUI_SETTINGS


def test_update_gui_settings_merges_selected_values(tmp_path):
    """Updating one GUI setting should keep the other persisted values intact."""
    settings_path = tmp_path / "gui_settings.json"

    update_gui_settings(language="en", settings_path=settings_path)
    updated_settings = update_gui_settings(user_id=5, settings_path=settings_path)

    assert updated_settings == {
        "user_id": 5,
        "language": "en",
        "dark_mode": False,
    }
