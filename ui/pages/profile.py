# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Profile page builder for the SEDA desktop GUI. AI-generated."""

# pylint: disable=all

from __future__ import annotations

from typing import TYPE_CHECKING

import flet as ft

from ui.gui_components import DatePickerField, PrimaryButton, SurfaceSection
from ui.gui_dialogs import close_dialog, open_confirm_dialog
from ui.gui_theme import SEDA_MINT, SEDA_RED

if TYPE_CHECKING:
    from ui.gui import SedaGuiApp


def build_profile_view(app: "SedaGuiApp"):
    """Build the profile page with inline forms and account settings. AI-generated."""
    app.refresh_current_user_logs()

    name_field = ft.TextField(label=app.t("name"), value=app.current_user.name)
    birthdate_value, _ = app.split_timestamp(f"{app.current_user.birthdate}T00:00:00")
    birthdate_field = DatePickerField(
        app,
        app.t("birthdate"),
        value=birthdate_value,
        expand=True,
    )
    height_field = ft.TextField(
        label=app.t("height_cm"),
        value=str(app.current_user.height_in_cm),
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    gender_dropdown = ft.Dropdown(
        label=app.t("gender"),
        value=app.current_user.gender,
        options=[
            ft.DropdownOption(key="m", text=app.t("gender_m")),
            ft.DropdownOption(key="f", text=app.t("gender_f")),
            ft.DropdownOption(key="d", text=app.t("gender_d")),
        ],
    )
    fitness_dropdown = ft.Dropdown(
        label=app.t("fitness_level"),
        value=app.current_user.fitness_lvl,
        options=[
            ft.DropdownOption(key="beginner", text=app.t("fitness_beginner")),
            ft.DropdownOption(key="intermediate", text=app.t("fitness_intermediate")),
            ft.DropdownOption(key="advanced", text=app.t("fitness_advanced")),
        ],
    )

    def submit_profile(_):
        """Validate and persist personal data edits."""
        try:
            app.save_profile(
                name_field.value.strip(),
                birthdate_field.selected_date.isoformat(),
                app.parse_required_int(height_field.value),
                gender_dropdown.value,
                fitness_dropdown.value,
            )
        except Exception as exc:
            app.show_message(str(exc), error=True)

    personal_section = SurfaceSection(
        app,
        app.t("personal_data"),
        ft.Column(
            [
                ft.Row([name_field, birthdate_field], spacing=12),
                ft.Row([height_field, gender_dropdown, fitness_dropdown], spacing=12),
                ft.Row(
                    [
                        ft.Container(expand=True),
                        PrimaryButton(
                            app.t("save"),
                            icon=ft.Icons.SAVE,
                            on_click=submit_profile,
                        ),
                    ]
                ),
            ],
            spacing=12,
        ),
    )

    language_dropdown = ft.Dropdown(
        label=app.t("language"),
        value=app.current_language,
        options=[
            ft.DropdownOption(key="en", text=app.t("language_en")),
            ft.DropdownOption(key="de", text=app.t("language_de")),
        ],
        on_select=lambda e: app.change_language(e.control.value),
        width=220,
    )
    dark_mode_switch = ft.Switch(
        value=app.is_dark_mode(),
        active_color=SEDA_MINT,
        active_track_color=app.surface_background_alt_color(),
        inactive_thumb_color=app.surface_muted_color(),
        inactive_track_color=app.surface_border_color(),
        on_change=lambda _: app.toggle_theme(),
    )
    switch_prefix_width = 36
    switch_suffix_width = 24
    dark_mode_row = ft.Row(
        [
            ft.Text(app.t("dark_mode"), width=140),
            ft.Container(
                width=160,
                content=ft.Row(
                    [
                        ft.Container(width=switch_prefix_width),
                        dark_mode_switch,
                        ft.Container(width=switch_suffix_width),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
            ),
        ],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8,
    )
    energy_unit_switch = ft.Switch(
        value=app.energy_unit == "kj",
        active_color=SEDA_MINT,
        active_track_color=app.surface_background_alt_color(),
        inactive_thumb_color=app.surface_muted_color(),
        inactive_track_color=app.surface_border_color(),
        on_change=lambda e: app.change_energy_unit("kj" if e.control.value else "kcal"),
    )
    energy_unit_row = ft.Row(
        [
            ft.Text(app.t("energy_unit"), width=140),
            ft.Container(
                width=160,
                content=ft.Row(
                    [
                        ft.Text(
                            "kcal",
                            width=switch_prefix_width,
                            color=app.surface_muted_color(),
                        ),
                        energy_unit_switch,
                        ft.Text(
                            "kJ",
                            width=switch_suffix_width,
                            color=app.surface_muted_color(),
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                ),
            ),
        ],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8,
    )

    settings_section = SurfaceSection(
        app,
        app.t("application_settings"),
        ft.Column([language_dropdown, dark_mode_row, energy_unit_row], spacing=12),
    )

    account_section = SurfaceSection(
        app,
        app.t("delete_account"),
        ft.Column(
            [
                ft.Text(
                    app.t("delete_account_copy"),
                    color=app.surface_muted_color(),
                ),
                ft.Row(
                    [
                        ft.FilledButton(
                            content=app.t("delete_account"),
                            icon=ft.Icons.DELETE_FOREVER_OUTLINED,
                            style=ft.ButtonStyle(
                                bgcolor=SEDA_RED,
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            on_click=lambda _: open_confirm_dialog(
                                app,
                                app.t("delete_account_confirm_title"),
                                app.t(
                                    "delete_account_confirm_copy",
                                    name=app.current_user.name,
                                ),
                                lambda dialog: (
                                    close_dialog(app, dialog),
                                    app.delete_current_user(),
                                ),
                            ),
                        )
                    ]
                ),
            ],
            spacing=12,
        ),
    )

    return ft.Column(
        [
            personal_section,
            settings_section,
            account_section,
        ],
        spacing=20,
    )
