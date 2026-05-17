# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Tests for locale-aware GUI number parsing. AI-generated."""

import pytest

from ui.gui import SedaGuiApp


class _DummyGui:
    """Minimal stand-in for SedaGuiApp number-formatting helpers. AI-generated."""

    def __init__(self, language):
        self.current_language = language
        self.energy_unit = "kcal"

    def t(self, key, **kwargs):
        if key == "msg_invalid_decimal_number":
            if self.current_language == "de":
                return (
                    f"Bitte gib eine gültige Zahl mit höchstens "
                    f"{kwargs['max_places']} Nachkommastellen ein."
                )
            return (
                f"Please enter a valid number with up to "
                f"{kwargs['max_places']} decimal places."
            )
        return key


def test_parse_required_float_accepts_german_comma():
    """German GUI inputs should accept a comma as decimal separator. AI-generated."""
    dummy = _DummyGui("de")

    parsed_value = SedaGuiApp.parse_required_float(dummy, "78,5")

    assert parsed_value == 78.5


def test_parse_required_float_rejects_more_than_two_decimal_places():
    """GUI float parsing should reject values with more than two decimals. AI-generated."""
    dummy = _DummyGui("de")

    with pytest.raises(ValueError) as exc_info:
        SedaGuiApp.parse_required_float(dummy, "78,555")

    assert "2 Nachkommastellen" in str(exc_info.value)


def test_format_amount_uses_decimal_comma_in_german():
    """German amount formatting should display decimal commas. AI-generated."""
    dummy = _DummyGui("de")
    dummy.format_amount = SedaGuiApp.format_amount.__get__(dummy, _DummyGui)

    assert dummy.format_amount(1.5, "kg") == "1,5 kg"


def test_format_amount_converts_kcal_to_kj_for_gui_display():
    """Energy display should convert kcal to kJ when the GUI setting requests it. AI-generated."""
    dummy = _DummyGui("de")
    dummy.energy_unit = "kj"
    dummy.format_amount = SedaGuiApp.format_amount.__get__(dummy, _DummyGui)

    assert dummy.format_amount(100, "kcal") == "418 kJ"
