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
SEDA_MINT = "#00A69C"
SEDA_YELLOW = "#EBE46E"
SEDA_RED = "#EB6E85"

NAV_ITEMS = [
    ("dashboard", "nav_dashboard", ft.Icons.DASHBOARD_OUTLINED),
    ("water", "nav_water", ft.Icons.WATER_DROP_OUTLINED),
    ("nutrition", "nav_nutrition", ft.Icons.RESTAURANT_MENU),
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

NUTRIENT_SUMMARY_LABELS = {
    "water": "Water",
    "monounsaturated_fat": "Monounsaturated fat",
    "polyunsaturated_fat": "Polyunsaturated fat",
    "omega_3": "Omega-3",
    "omega_6": "Omega-6",
    "starch": "Starch",
    "alcohol": "Alcohol",
    "sodium": "Sodium",
    "cholesterol": "Cholesterol",
    "potassium": "Potassium",
    "calcium": "Calcium",
    "magnesium": "Magnesium",
    "phosphorus": "Phosphorus",
    "iron": "Iron",
    "zinc": "Zinc",
    "iodine": "Iodine",
    "copper": "Copper",
    "manganese": "Manganese",
    "fluoride": "Fluoride",
    "chromium": "Chromium",
    "molybdenum": "Molybdenum",
    "vitamin_a_re": "Vitamin A (RE)",
    "vitamin_a_rae": "Vitamin A (RAE)",
    "retinol": "Retinol",
    "beta_carotene": "Beta-carotene",
    "vitamin_d": "Vitamin D",
    "vitamin_d2": "Vitamin D2",
    "vitamin_d3": "Vitamin D3",
    "vitamin_e": "Vitamin E",
    "alpha_tocopherol": "Alpha-tocopherol",
    "vitamin_k": "Vitamin K",
    "vitamin_k1": "Vitamin K1",
    "vitamin_k2": "Vitamin K2",
    "vitamin_b1": "Vitamin B1",
    "vitamin_b2": "Vitamin B2",
    "niacin": "Niacin",
    "niacin_equivalent": "Niacin equivalent",
    "pantothenic_acid": "Pantothenic acid",
    "vitamin_b6": "Vitamin B6",
    "biotin": "Biotin",
    "folate_equivalent": "Folate equivalent",
    "folate": "Folate",
    "folic_acid": "Folic acid",
    "vitamin_b12": "Vitamin B12",
    "vitamin_c": "Vitamin C",
}

NUTRIENT_SUMMARY_LABELS_DE = {
    "water": "Wasser",
    "monounsaturated_fat": "Einfach ungesättigte Fettsäuren",
    "polyunsaturated_fat": "Mehrfach ungesättigte Fettsäuren",
    "omega_3": "Omega-3",
    "omega_6": "Omega-6",
    "starch": "Stärke",
    "alcohol": "Alkohol",
    "sodium": "Natrium",
    "cholesterol": "Cholesterin",
    "potassium": "Kalium",
    "calcium": "Kalzium",
    "magnesium": "Magnesium",
    "phosphorus": "Phosphor",
    "iron": "Eisen",
    "zinc": "Zink",
    "iodine": "Jod",
    "copper": "Kupfer",
    "manganese": "Mangan",
    "fluoride": "Fluorid",
    "chromium": "Chrom",
    "molybdenum": "Molybdän",
    "vitamin_a_re": "Vitamin A (RE)",
    "vitamin_a_rae": "Vitamin A (RAE)",
    "retinol": "Retinol",
    "beta_carotene": "Beta-Carotin",
    "vitamin_d": "Vitamin D",
    "vitamin_d2": "Vitamin D2",
    "vitamin_d3": "Vitamin D3",
    "vitamin_e": "Vitamin E",
    "alpha_tocopherol": "Alpha-Tocopherol",
    "vitamin_k": "Vitamin K",
    "vitamin_k1": "Vitamin K1",
    "vitamin_k2": "Vitamin K2",
    "vitamin_b1": "Vitamin B1",
    "vitamin_b2": "Vitamin B2",
    "niacin": "Niacin",
    "niacin_equivalent": "Niacin-Äquivalent",
    "pantothenic_acid": "Pantothensäure",
    "vitamin_b6": "Vitamin B6",
    "biotin": "Biotin",
    "folate_equivalent": "Folat-Äquivalent",
    "folate": "Folat",
    "folic_acid": "Folsäure",
    "vitamin_b12": "Vitamin B12",
    "vitamin_c": "Vitamin C",
}

NUTRIENT_SUMMARY_UNITS = {
    "water": "g",
    "monounsaturated_fat": "g",
    "polyunsaturated_fat": "g",
    "omega_3": "g",
    "omega_6": "g",
    "starch": "g",
    "alcohol": "g",
    "sodium": "mg",
    "cholesterol": "mg",
    "potassium": "mg",
    "calcium": "mg",
    "magnesium": "mg",
    "phosphorus": "mg",
    "iron": "mg",
    "zinc": "mg",
    "iodine": "µg",
    "copper": "µg",
    "manganese": "µg",
    "fluoride": "µg",
    "chromium": "µg",
    "molybdenum": "µg",
    "vitamin_a_re": "µg",
    "vitamin_a_rae": "µg",
    "retinol": "µg",
    "beta_carotene": "µg",
    "vitamin_d": "µg",
    "vitamin_d2": "µg",
    "vitamin_d3": "µg",
    "vitamin_e": "mg",
    "alpha_tocopherol": "mg",
    "vitamin_k": "µg",
    "vitamin_k1": "µg",
    "vitamin_k2": "µg",
    "vitamin_b1": "mg",
    "vitamin_b2": "mg",
    "niacin": "mg",
    "niacin_equivalent": "mg",
    "pantothenic_acid": "mg",
    "vitamin_b6": "µg",
    "biotin": "µg",
    "folate_equivalent": "µg",
    "folate": "µg",
    "folic_acid": "µg",
    "vitamin_b12": "µg",
    "vitamin_c": "mg",
}
