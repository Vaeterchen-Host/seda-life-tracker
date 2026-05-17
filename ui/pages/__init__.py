# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Page builders for the SEDA desktop GUI. AI-generated."""

from ui.pages.about import build_about_view
from ui.pages.activity import build_activity_view
from ui.pages.biometrics import build_biometrics_view
from ui.pages.dashboard import build_dashboard_view
from ui.pages.landing import build_create_user_view
from ui.pages.nutrition import build_nutrition_view
from ui.pages.profile import build_profile_view
from ui.pages.water import build_water_view

__all__ = [
    "build_about_view",
    "build_activity_view",
    "build_biometrics_view",
    "build_create_user_view",
    "build_dashboard_view",
    "build_nutrition_view",
    "build_profile_view",
    "build_water_view",
]
