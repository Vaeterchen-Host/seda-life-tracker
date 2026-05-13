# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""About page builder for the SEDA GUI. AI-generated."""

# pylint: disable=all

from __future__ import annotations

from typing import TYPE_CHECKING

import flet as ft

from config import DEVS, VERSION
from ui.gui_components import PrimaryButton, SurfaceSection
from ui.gui_dialogs import open_license_dialog
from ui.gui_theme import SEDA_MINT, SEDA_YELLOW

if TYPE_CHECKING:
    from ui.gui import SedaGuiApp


def _build_info_card(app: "SedaGuiApp", label: str, value: str, icon) -> ft.Control:
    """Render one compact info card for the about page. AI-generated."""
    return ft.Container(
        padding=16,
        border_radius=8,
        bgcolor=app.surface_background_alt_color(),
        border=ft.border.all(1, app.surface_border_color()),
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(icon, color=SEDA_MINT, size=18),
                        ft.Text(label, size=12, color=app.surface_muted_color()),
                    ],
                    spacing=8,
                    tight=True,
                ),
                ft.Text(value, size=16, weight=ft.FontWeight.W_600),
            ],
            spacing=10,
            tight=True,
        ),
    )


def _build_feature_card(app: "SedaGuiApp", text: str, icon) -> ft.Control:
    """Render one human-friendly feature summary card. AI-generated."""
    return ft.Container(
        padding=16,
        border_radius=8,
        bgcolor=app.surface_background_alt_color(),
        border=ft.border.all(1, app.surface_border_color()),
        content=ft.Row(
            [
                ft.Icon(icon, color=SEDA_YELLOW, size=20),
                ft.Text(text, expand=True),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
    )


def build_about_view(app: "SedaGuiApp"):
    """Build a lightweight about page connected to the live app state. Partly AI-generated."""
    feature_items = [
        (app.t("feature_water"), ft.Icons.WATER_DROP_OUTLINED),
        (app.t("feature_nutrition"), ft.Icons.RESTAURANT_MENU),
        (app.t("feature_body"), ft.Icons.PERSON_OUTLINED),
        (app.t("feature_activity"), ft.Icons.DIRECTIONS_RUN),
    ]
    info_items = [
        (
            app.t("database_status"),
            app.t("database_ready"),
            ft.Icons.STORAGE_OUTLINED,
        ),
        (app.t("developers_label"), DEVS, ft.Icons.GROUP_OUTLINED),
    ]
    license_items = [
        (
            app.t("license_name_label"),
            app.t("license_name_value"),
            ft.Icons.GAVEL_OUTLINED,
        ),
        (app.t("license_spdx_label"), "GPL-3.0-or-later", ft.Icons.LABEL_OUTLINED),
        (app.t("license_file_label"), "LICENSE.md", ft.Icons.DESCRIPTION_OUTLINED),
    ]

    intro_block = ft.Column(
        [
            ft.Container(
                padding=ft.padding.symmetric(horizontal=14, vertical=10),
                border_radius=999,
                bgcolor=app.surface_background_alt_color(),
                border=ft.border.all(1, app.surface_border_color()),
                content=ft.Text(
                    f"v{VERSION}",
                    weight=ft.FontWeight.BOLD,
                    color=SEDA_MINT,
                ),
            ),
            ft.Text(
                app.t("app_subtitle"),
                size=13,
                color=app.surface_muted_color(),
            ),
            ft.Text(
                app.t("about_copy"),
                size=22,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Text(
                app.t("about_detail"),
                color=app.surface_muted_color(),
            ),
        ],
        spacing=10,
        tight=True,
    )

    feature_section = SurfaceSection(
        app,
        app.t("feature_overview"),
        ft.Column(
            [
                ft.Text(app.t("feature_overview_copy"), color=app.surface_muted_color()),
                ft.Column(
                    [_build_feature_card(app, text, icon) for text, icon in feature_items],
                    spacing=12,
                ),
            ],
            spacing=14,
        ),
    )

    about_section = SurfaceSection(
        app,
        app.t("about_title"),
        ft.Column(
            [
                intro_block,
                ft.Column(
                    [
                        _build_info_card(app, label, value, icon)
                        for label, value, icon in info_items
                    ],
                    spacing=12,
                ),
            ],
            spacing=18,
        ),
    )

    license_section = SurfaceSection(
        app,
        app.t("license_title"),
        ft.Column(
            [
                ft.Text(app.t("license_copy"), color=app.surface_muted_color()),
                ft.Column(
                    [
                        _build_info_card(app, label, value, icon)
                        for label, value, icon in license_items
                    ],
                    spacing=12,
                ),
                PrimaryButton(
                    app.t("show_full_license"),
                    icon=ft.Icons.GAVEL_OUTLINED,
                    on_click=lambda _: open_license_dialog(app),
                ),
            ],
            spacing=10,
        ),
    )

    return ft.Column([about_section, feature_section, license_section], spacing=20)
