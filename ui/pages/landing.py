# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Landing page builder for the SEDA desktop GUI. AI-generated."""

# pylint: disable=all

from __future__ import annotations

from typing import TYPE_CHECKING

import flet as ft

from ui.gui_components import SedaLogo, SurfaceSection
from ui.gui_theme import SEDA_YELLOW

if TYPE_CHECKING:
    from ui.gui import SedaGuiApp


def build_create_user_view(app: "SedaGuiApp"):
    """Build the account-creation landing page. Partly AI-generated."""
    name_field = ft.TextField(label=app.t("name"), autofocus=True)
    birthdate_field = ft.TextField(
        label=app.t("birthdate"),
        hint_text=app.birthdate_input_hint(),
    )
    height_field = ft.TextField(
        label=app.t("height_cm"),
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    gender_dropdown = ft.Dropdown(
        label=app.t("gender"),
        value="m",
        options=[
            ft.DropdownOption(key="m", text=app.t("gender_m")),
            ft.DropdownOption(key="f", text=app.t("gender_f")),
            ft.DropdownOption(key="d", text=app.t("gender_d")),
        ],
    )
    fitness_dropdown = ft.Dropdown(
        label=app.t("fitness_level"),
        value="beginner",
        options=[
            ft.DropdownOption(key="beginner", text=app.t("fitness_beginner")),
            ft.DropdownOption(key="intermediate", text=app.t("fitness_intermediate")),
            ft.DropdownOption(key="advanced", text=app.t("fitness_advanced")),
        ],
    )

    def submit_user(_):
        """Validate the landing-page form and create the first user."""
        try:
            name = name_field.value.strip()
            birthdate = app.parse_birthdate(birthdate_field.value)
            height = app.parse_required_int(height_field.value)
            if not name:
                raise ValueError(app.t("name"))
            app.create_user(
                name,
                birthdate,
                height,
                gender_dropdown.value,
                fitness_dropdown.value,
            )
        except Exception as exc:
            app.show_message(str(exc), error=True)

    form = SurfaceSection(
        app,
        app.t("create_user"),
        ft.Column(
            [
                name_field,
                birthdate_field,
                height_field,
                gender_dropdown,
                fitness_dropdown,
                ft.FilledButton(
                    content=app.t("create_user"),
                    icon=ft.Icons.PERSON_ADD,
                    style=ft.ButtonStyle(
                        bgcolor=SEDA_YELLOW,
                        color=ft.Colors.BLACK,
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=submit_user,
                ),
            ],
            spacing=12,
        ),
    )

    return ft.Row(
        [
            ft.Container(
                expand=1,
                content=ft.Column(
                    [
                        SedaLogo(app.is_dark_mode(), width=320),
                        ft.Text(
                            app.t("landing_title"),
                            size=36,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            app.t("landing_copy"),
                            size=16,
                            color=app.surface_muted_color(),
                        ),
                    ],
                    spacing=14,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=ft.padding.only(right=24),
            ),
            ft.Container(width=420, content=form),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
