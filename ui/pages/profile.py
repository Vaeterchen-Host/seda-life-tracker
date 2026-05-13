# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Profile page builder for the SEDA desktop GUI. AI-generated."""

# pylint: disable=all

from __future__ import annotations

from typing import TYPE_CHECKING

import flet as ft

from application.status_service import get_today_calorie_status
from ui.gui_components import LabelValueRow, PrimaryButton, SurfaceItem, SurfaceSection
from ui.gui_dialogs import close_dialog, open_confirm_dialog
from ui.gui_theme import SEDA_RED

if TYPE_CHECKING:
    from ui.gui import SedaGuiApp


def build_profile_view(app: "SedaGuiApp"):
    """Build the profile page with inline forms and calculated values. Partly AI-generated."""
    app.refresh_current_user_logs()
    calorie_status = get_today_calorie_status(app.current_user)
    current_weight_log = app.get_current_weight_log()

    name_field = ft.TextField(label=app.t("name"), value=app.current_user.name)
    birthdate_field = ft.TextField(
        label=app.t("birthdate"),
        value=app.format_birthdate(app.current_user.birthdate),
        hint_text=app.birthdate_input_hint(),
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
                app.parse_birthdate(birthdate_field.value),
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

    weight_field = ft.TextField(
        label=app.t("weight_kg"),
        keyboard_type=ft.KeyboardType.NUMBER,
        width=220,
    )
    weight_timestamp_field = ft.TextField(
        label=app.t("optional_timestamp"),
        hint_text=app.timestamp_input_hint(),
        expand=True,
    )

    def submit_weight(_):
        """Create one new weight log from the profile page."""
        try:
            weight = app.parse_required_float(weight_field.value)
            timestamp = app.parse_optional_timestamp(weight_timestamp_field.value)
            app.add_weight_log(weight, timestamp)
        except Exception as exc:
            app.show_message(str(exc), error=True)

    weight_rows = []
    for weight_log in app.sort_logs_desc(app.current_user.weight_log_handler.logs):
        weight_rows.append(
            SurfaceItem(
                app,
                ft.Row(
                    [
                        ft.Text(
                            app.format_amount(weight_log.weight_in_kg, "kg"),
                            width=110,
                        ),
                        ft.Text(
                            app.format_amount(weight_log.bmi),
                            width=100,
                            color=app.surface_muted_color(),
                        ),
                        ft.Text(
                            app.format_timestamp(weight_log.timestamp),
                            expand=True,
                            color=app.surface_muted_color(),
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            icon_color=SEDA_RED,
                            on_click=lambda _, log_id=weight_log.id: open_confirm_dialog(
                                app,
                                app.t("msg_confirm_delete_entry"),
                                app.t("weight_bmi"),
                                lambda dialog, target_id=log_id: (
                                    close_dialog(app, dialog),
                                    app.delete_weight_log(target_id),
                                ),
                            ),
                        ),
                    ]
                ),
            )
        )

    body_section = SurfaceSection(
        app,
        app.t("body_statistics"),
        ft.Column(
            [
                LabelValueRow(
                    app,
                    app.t("latest_weight"),
                    (
                        app.format_amount(current_weight_log.weight_in_kg, "kg")
                        if current_weight_log is not None
                        else app.t("no_weight_logged")
                    ),
                ),
                LabelValueRow(
                    app,
                    app.t("bmi"),
                    (
                        app.format_amount(current_weight_log.bmi)
                        if current_weight_log is not None
                        and current_weight_log.bmi is not None
                        else app.t("bmi_not_available")
                    ),
                ),
                ft.Row(
                    [
                        weight_field,
                        weight_timestamp_field,
                        PrimaryButton(
                            app.t("add_weight_log"),
                            icon=ft.Icons.MONITOR_WEIGHT_OUTLINED,
                            on_click=submit_weight,
                        ),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                ),
                ft.Text(app.t("weight_logs"), weight=ft.FontWeight.BOLD),
                ft.Column(
                    weight_rows
                    or [
                        ft.Text(
                            app.t("no_weight_logs"),
                            color=app.surface_muted_color(),
                        )
                    ],
                    spacing=10,
                ),
            ],
            spacing=12,
        ),
    )

    calculated_section = SurfaceSection(
        app,
        app.t("calculated_values"),
        ft.Column(
            [
                LabelValueRow(
                    app,
                    app.t("daily_calorie_target"),
                    app.format_amount(calorie_status["target"], "kcal"),
                ),
                LabelValueRow(
                    app,
                    app.t("daily_water_target"),
                    app.format_amount(app.current_user.daily_water_target, "ml"),
                ),
                LabelValueRow(
                    app,
                    app.t("bmi"),
                    (
                        app.format_amount(current_weight_log.bmi)
                        if current_weight_log is not None
                        and current_weight_log.bmi is not None
                        else app.t("bmi_not_available")
                    ),
                ),
            ],
            spacing=10,
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

    settings_section = SurfaceSection(
        app,
        app.t("application_settings"),
        ft.Column([language_dropdown], spacing=12),
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
            body_section,
            calculated_section,
            settings_section,
            account_section,
        ],
        spacing=20,
    )
