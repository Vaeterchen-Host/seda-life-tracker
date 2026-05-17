# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Biometrics page builder for the SEDA desktop GUI. Partly AI-generated."""

# pylint: disable=all

from __future__ import annotations

from typing import TYPE_CHECKING

import flet as ft

from application.status_service import get_today_calorie_status
from ui.gui_components import (
    LabelValueRow,
    PrimaryButton,
    SurfaceItem,
    SurfaceSection,
)
from ui.gui_dialogs import close_dialog, open_confirm_dialog, open_weight_log_dialog
from ui.gui_theme import SEDA_RED

if TYPE_CHECKING:
    from ui.gui import SedaGuiApp


def build_biometrics_view(app: "SedaGuiApp"):
    """Build the biometrics page with weight, BMI and weight history. AI-generated."""
    app.refresh_current_user_logs()
    calorie_status = get_today_calorie_status(app.current_user)
    current_weight_log = app.get_current_weight_log()

    current_status_section = SurfaceSection(
        app,
        app.t("current_status"),
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
            ],
            spacing=10,
        ),
    )

    add_measurement_section = SurfaceSection(
        app,
        app.t("add_weight_log"),
        PrimaryButton(
            app.t("add_weight_log"),
            icon=ft.Icons.ASSESSMENT_OUTLINED,
            on_click=lambda _: open_weight_log_dialog(app),
        ),
    )

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

    history_section = SurfaceSection(
        app,
        app.t("weight_history"),
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
    )

    return ft.Column(
        [
            current_status_section,
            calculated_section,
            add_measurement_section,
            history_section,
        ],
        spacing=20,
    )
