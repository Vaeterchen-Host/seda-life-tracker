# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Shared GUI theme and label constants for SEDA."""

# AI note: The constants below were extracted during the GUI split.

# pylint: disable=all

import flet as ft

PAGE_BACKGROUND = "#111315"
SURFACE_BACKGROUND = "#171B21"
SURFACE_BACKGROUND_ALT = "#1C2626"
SURFACE_BORDER = "#3E4B5D"
SURFACE_MUTED = "#AAB5C3"
BRAND_MINT = "#00A69C"
BRAND_YELLOW = "#EBE46E"
BRAND_RED = "#EB6E85"

NAV_ITEMS = [
    ("dashboard", "nav_dashboard", ft.Icons.DASHBOARD_OUTLINED),
    ("nutrition", "nav_nutrition", ft.Icons.RESTAURANT_MENU),
    ("water", "nav_water", ft.Icons.WATER_DROP_OUTLINED),
    ("activity", "nav_activity", ft.Icons.DIRECTIONS_RUN),
    ("profile", "nav_profile", ft.Icons.PERSON_OUTLINE),
    ("about", "nav_about", ft.Icons.INFO_OUTLINE),
]

BIG_SEVEN_LABELS = {
    "fat": "Fat",
    "saturated_fat": "Saturated fat",
    "carbohydrate": "Carbohydrate",
    "fibre": "Fibre",
    "sugar": "Sugar",
    "protein": "Protein",
    "salt": "Salt",
}

BIG_SEVEN_LABELS_DE = {
    "fat": "Fett",
    "saturated_fat": "Gesättigte Fettsäuren",
    "carbohydrate": "Kohlenhydrate",
    "fibre": "Ballaststoffe",
    "sugar": "Zucker",
    "protein": "Eiweiß",
    "salt": "Salz",
}
