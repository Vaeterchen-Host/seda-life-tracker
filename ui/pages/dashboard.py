# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Dashboard page builder for the SEDA desktop GUI. AI-generated."""

# pylint: disable=all

from __future__ import annotations

from typing import TYPE_CHECKING

import flet as ft

from application.status_service import get_today_calorie_status, get_today_water_status
from ui.gui_components import (
    LabelValueRow,
    MetricChip,
    PrimaryButton,
    SurfaceSection,
)
from ui.gui_theme import SEDA_MINT

if TYPE_CHECKING:
    from ui.gui import SedaGuiApp


def build_dashboard_view(app: "SedaGuiApp"):
    """Build the first overview page with water, calories and quick actions. Partly AI-generated."""
    calorie_status = get_today_calorie_status(app.current_user)
    water_status = get_today_water_status(app.current_user)
    current_weight_log = app.get_current_weight_log()

    hero = ft.Row(
        [
            ft.Container(
                width=96,
                height=96,
                border_radius=8,
                border=ft.border.all(1, app.surface_border_color()),
                content=ft.Icon(ft.Icons.MONITOR_HEART_OUTLINED, size=42),
                alignment=ft.Alignment.CENTER,
            ),
            ft.Column(
                [
                    ft.Text(
                        app.t("welcome_back", name=app.current_user.name),
                        size=34,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        app.t("dashboard_intro"),
                        size=16,
                        color=app.surface_muted_color(),
                    ),
                ],
                spacing=8,
                expand=True,
            ),
        ],
        spacing=20,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    calorie_card = SurfaceSection(
        app,
        app.t("calorie_balance_today"),
        ft.Row(
            [
                ft.Column(
                    [
                        LabelValueRow(
                            app,
                            app.t("calories_eaten"),
                            app.format_amount(calorie_status["intake"], "kcal"),
                        ),
                        LabelValueRow(
                            app,
                            app.t("calories_burned_label"),
                            app.format_amount(calorie_status["burned"], "kcal"),
                        ),
                        LabelValueRow(
                            app,
                            app.t("calorie_balance_label"),
                            app.format_amount(calorie_status["net"], "kcal"),
                        ),
                        LabelValueRow(
                            app,
                            app.t("calorie_goal"),
                            app.format_amount(calorie_status["target"], "kcal"),
                        ),
                    ],
                    spacing=10,
                    expand=1,
                ),
                ft.Container(
                    width=340,
                    content=ft.Column(
                        [
                            ft.ProgressBar(
                                value=(
                                    0
                                    if not calorie_status["target"]
                                    else min(
                                        1,
                                        calorie_status["intake"]
                                        / calorie_status["target"],
                                    )
                                ),
                                color=SEDA_MINT,
                                bgcolor=app.surface_border_color(),
                            ),
                            ft.Text(
                                f"{app.t('remaining_to_goal')}: "
                                f"{app.format_amount(calorie_status['difference'], 'kcal')}",
                                color=app.surface_muted_color(),
                            ),
                        ],
                        spacing=10,
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )

    cards_row = ft.ResponsiveRow(
        [
            ft.Container(
                col={"md": 6},
                content=SurfaceSection(
                    app,
                    app.t("water_today"),
                    ft.Column(
                        [
                            ft.Text(
                                app.t(
                                    "water_progress",
                                    intake=water_status["intake"],
                                    target=water_status["target"],
                                ),
                                size=20,
                            ),
                            ft.ProgressBar(
                                value=min(1, (water_status["progress"] or 0) / 100),
                                color=SEDA_MINT,
                                bgcolor=app.surface_border_color(),
                            ),
                            ft.Text(
                                app.t(
                                    "water_to_go",
                                    difference=water_status["difference"],
                                ),
                                color=app.surface_muted_color(),
                            ),
                        ],
                        spacing=12,
                    ),
                ),
            ),
            ft.Container(
                col={"md": 6},
                content=SurfaceSection(
                    app,
                    app.t("weight_bmi"),
                    ft.Column(
                        [
                            LabelValueRow(
                                app,
                                app.t("current_weight"),
                                (
                                    app.format_amount(
                                        current_weight_log.weight_in_kg, "kg"
                                    )
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
                ),
            ),
        ],
        run_spacing=16,
        spacing=16,
    )

    quick_actions = SurfaceSection(
        app,
        app.t("quick_actions"),
        ft.ResponsiveRow(
            [
                ft.Container(
                    col={"md": 3},
                    content=PrimaryButton(
                        app.t("add_water"),
                        icon=ft.Icons.WATER_DROP,
                        expand=True,
                        on_click=lambda _: app.navigate("water"),
                    ),
                ),
                ft.Container(
                    col={"md": 3},
                    content=PrimaryButton(
                        app.t("log_meal"),
                        icon=ft.Icons.RESTAURANT,
                        expand=True,
                        on_click=lambda _: app.navigate("nutrition"),
                    ),
                ),
                ft.Container(
                    col={"md": 3},
                    content=PrimaryButton(
                        app.t("add_activity"),
                        icon=ft.Icons.DIRECTIONS_RUN,
                        expand=True,
                        on_click=lambda _: app.navigate("activity"),
                    ),
                ),
                ft.Container(
                    col={"md": 3},
                    content=PrimaryButton(
                        app.t("go_to_biometrics"),
                        icon=ft.Icons.ASSESSMENT_OUTLINED,
                        expand=True,
                        on_click=lambda _: app.navigate("biometrics"),
                    ),
                ),
            ],
            spacing=12,
            run_spacing=12,
        ),
    )

    return ft.Column([hero, calorie_card, cards_row, quick_actions], spacing=20)
