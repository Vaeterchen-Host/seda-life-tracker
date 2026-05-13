# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Nutrition page builder for the SEDA desktop GUI. AI-generated."""

# pylint: disable=all

from __future__ import annotations

from typing import TYPE_CHECKING

import flet as ft

from application.status_service import get_today_calorie_status
from ui.gui_components import MetricChip, PrimaryButton, SurfaceItem, SurfaceSection
from ui.gui_dialogs import (
    close_dialog,
    open_confirm_dialog,
    open_food_amount_dialog,
    open_meal_log_details_dialog,
    open_meal_log_dialog,
)
from ui.gui_theme import SEDA_MINT, SEDA_RED, SEDA_YELLOW

if TYPE_CHECKING:
    from ui.gui import SedaGuiApp


def build_nutrition_view(app: "SedaGuiApp"):
    """Build the nutrition page with the full meal-management workflow. Partly AI-generated."""
    app.refresh_current_user_logs()
    calorie_status = get_today_calorie_status(app.current_user)

    def save_builder(_):
        """Persist the current meal template or show the error in the GUI footer."""
        try:
            app.save_meal_template()
        except Exception as exc:
            app.show_message(str(exc), error=True)

    def reset_builder(_):
        """Reset the current builder selection and redraw the nutrition page."""
        app.reset_meal_builder()
        app.show_message(app.t("msg_builder_reset"))
        app.render()

    search_field = ft.TextField(
        label=app.t("search_term"),
        value=app.food_search_term,
        expand=True,
        on_change=lambda e: setattr(app, "food_search_term", e.control.value),
        on_submit=lambda _: app.search_foods(),
    )

    calorie_section = SurfaceSection(
        app,
        app.t("calorie_status_today"),
        ft.Row(
            [
                MetricChip(
                    app,
                    app.t("calories_eaten"),
                    app.format_amount(calorie_status["intake"], "kcal"),
                    accent=SEDA_MINT,
                ),
                MetricChip(
                    app,
                    app.t("calories_burned_label"),
                    app.format_amount(calorie_status["burned"], "kcal"),
                    accent=SEDA_YELLOW,
                ),
                MetricChip(
                    app,
                    app.t("calorie_balance_label"),
                    app.format_amount(calorie_status["net"], "kcal"),
                    accent=app.primary_text_color(),
                ),
                MetricChip(
                    app,
                    app.t("calorie_goal"),
                    app.format_amount(calorie_status["target"], "kcal"),
                    accent=SEDA_MINT,
                ),
                MetricChip(
                    app,
                    app.t("remaining_to_goal"),
                    app.format_amount(calorie_status["difference"], "kcal"),
                    accent=SEDA_YELLOW,
                ),
            ],
            wrap=True,
            spacing=12,
        ),
    )

    search_rows = []
    for food_row in app.food_search_results:
        search_rows.append(
            SurfaceItem(
                app,
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(
                                    app.get_food_name(food_row),
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    f"{app.format_amount(food_row['kcal'], 'kcal')} / 100 {food_row['unit_type']}",
                                    color=app.surface_muted_color(),
                                ),
                            ],
                            spacing=4,
                            expand=True,
                        ),
                        PrimaryButton(
                            app.t("consume"),
                            on_click=lambda _, row=food_row: open_food_amount_dialog(
                                app,
                                row,
                                "consume",
                            ),
                        ),
                        ft.OutlinedButton(
                            content=app.t("add_to_template"),
                            on_click=lambda _, row=food_row: open_food_amount_dialog(
                                app,
                                row,
                                "template",
                            ),
                        ),
                    ],
                    spacing=12,
                ),
            )
        )

    search_section = SurfaceSection(
        app,
        app.t("food_search"),
        ft.Column(
            [
                ft.Text(app.t("food_search_copy"), color=app.surface_muted_color()),
                ft.Row(
                    [
                        search_field,
                        PrimaryButton(
                            app.t("search"),
                            icon=ft.Icons.SEARCH,
                            on_click=lambda _: app.search_foods(),
                        ),
                    ],
                    spacing=12,
                ),
                ft.Column(
                    search_rows
                    or [
                        ft.Text(
                            app.t("no_food_results"),
                            color=app.surface_muted_color(),
                        )
                    ],
                    spacing=10,
                ),
            ],
            spacing=12,
        ),
    )

    builder_name_field = ft.TextField(
        label=app.t("template_name"),
        value=app.meal_builder_name,
        on_change=lambda e: setattr(app, "meal_builder_name", e.control.value),
    )

    builder_rows = []
    for index, food_item in enumerate(app.meal_builder_items):
        builder_rows.append(
            SurfaceItem(
                app,
                ft.Row(
                    [
                        ft.Text(app.get_food_item_display_name(food_item), expand=True),
                        ft.Text(
                            app.format_amount(food_item.amount, food_item.unit_type),
                            width=110,
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            icon_color=SEDA_RED,
                            on_click=lambda _, item_index=index: (
                                app.meal_builder_items.pop(item_index),
                                app.render(),
                            ),
                        ),
                    ]
                ),
            )
        )

    builder_section = SurfaceSection(
        app,
        app.t("meal_template_builder"),
        ft.Column(
            [
                ft.Text(app.t("builder_copy"), color=app.surface_muted_color()),
                builder_name_field,
                ft.Text(app.t("selected_items"), weight=ft.FontWeight.BOLD),
                ft.Column(
                    builder_rows
                    or [
                        ft.Text(
                            app.t("builder_empty"),
                            color=app.surface_muted_color(),
                        )
                    ],
                    spacing=10,
                ),
                ft.Row(
                    [
                        PrimaryButton(
                            app.t(
                                "update_template"
                                if app.editing_meal_template_id is not None
                                else "save_template"
                            ),
                            icon=ft.Icons.SAVE,
                            on_click=save_builder,
                        ),
                        ft.OutlinedButton(
                            content=app.t("reset_builder"),
                            icon=ft.Icons.RESTART_ALT,
                            on_click=reset_builder,
                        ),
                    ],
                    spacing=12,
                ),
            ],
            spacing=12,
        ),
    )

    template_rows = []
    for meal in app.get_meal_templates():
        template_rows.append(
            ft.Container(
                padding=12,
                border_radius=8,
                bgcolor=app.surface_background_alt_color(),
                border=ft.border.all(1, app.surface_border_color()),
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    app.get_meal_display_name(meal),
                                    weight=ft.FontWeight.BOLD,
                                    expand=True,
                                ),
                                ft.Text(
                                    app.format_amount(meal.calories, "kcal"),
                                    color=app.surface_muted_color(),
                                ),
                            ]
                        ),
                        ft.Text(
                            ", ".join(
                                [
                                    f"{app.get_food_item_display_name(item)} "
                                    f"({app.format_amount(item.amount, item.unit_type)})"
                                    for item in meal.food_items
                                ]
                            ),
                            color=app.surface_muted_color(),
                        ),
                        ft.Row(
                            [
                                ft.FilledButton(
                                    app.t("log_meal"),
                                    icon=ft.Icons.ADD_TASK,
                                    style=ft.ButtonStyle(
                                        bgcolor=SEDA_MINT,
                                        color=ft.Colors.WHITE,
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                    ),
                                    on_click=lambda _, selected_meal=meal: open_meal_log_dialog(
                                        app,
                                        meal=selected_meal,
                                    ),
                                ),
                                ft.OutlinedButton(
                                    app.t("edit_template"),
                                    icon=ft.Icons.EDIT,
                                    on_click=lambda _, selected_meal=meal: (
                                        app.start_meal_template_edit(selected_meal)
                                    ),
                                ),
                                ft.OutlinedButton(
                                    app.t("delete"),
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    style=ft.ButtonStyle(color=SEDA_RED),
                                    on_click=lambda _, selected_meal=meal: open_confirm_dialog(
                                        app,
                                        app.t("msg_confirm_delete_template"),
                                        app.get_meal_display_name(selected_meal),
                                        lambda dialog, meal_id=selected_meal.id: (
                                            close_dialog(app, dialog),
                                            app.delete_meal_template(meal_id),
                                        ),
                                    ),
                                ),
                            ],
                            spacing=10,
                            wrap=True,
                        ),
                    ],
                    spacing=10,
                ),
            )
        )

    templates_section = SurfaceSection(
        app,
        app.t("meal_templates"),
        ft.Column(
            template_rows
            or [ft.Text(app.t("no_meal_templates"), color=app.surface_muted_color())],
            spacing=10,
        ),
    )

    meal_log_rows = []
    for meal_log in app.sort_logs_desc(app.current_user.meal_log_handler.logs):
        enriched_log = app.enrich_meal_log(meal_log)
        meal_log_rows.append(
            ft.Container(
                padding=12,
                border_radius=8,
                bgcolor=app.surface_background_alt_color(),
                border=ft.border.all(1, app.surface_border_color()),
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text(
                                            app.get_meal_display_name(
                                                enriched_log.meal
                                            ),
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(
                                            f"{app.format_amount(enriched_log.amount, enriched_log.unit_type)} | "
                                            f"{app.format_amount(enriched_log.calories, 'kcal')}",
                                            color=app.surface_muted_color(),
                                        ),
                                    ],
                                    spacing=4,
                                    expand=True,
                                ),
                                ft.Text(
                                    app.format_timestamp(meal_log.timestamp),
                                    color=app.surface_muted_color(),
                                ),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.FilledButton(
                                    app.t("show_details"),
                                    icon=ft.Icons.ARTICLE_OUTLINED,
                                    style=ft.ButtonStyle(
                                        bgcolor=SEDA_MINT,
                                        color=ft.Colors.WHITE,
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                    ),
                                    on_click=lambda _, log=enriched_log: open_meal_log_details_dialog(
                                        app,
                                        log,
                                    ),
                                ),
                                ft.OutlinedButton(
                                    app.t("edit_log"),
                                    icon=ft.Icons.EDIT,
                                    on_click=lambda _, log=meal_log: open_meal_log_dialog(
                                        app,
                                        existing_log=log,
                                    ),
                                ),
                                ft.OutlinedButton(
                                    app.t("delete"),
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    style=ft.ButtonStyle(color=SEDA_RED),
                                    on_click=lambda _, log_id=meal_log.id: open_confirm_dialog(
                                        app,
                                        app.t("msg_confirm_delete_entry"),
                                        app.get_meal_display_name(enriched_log.meal),
                                        lambda dialog, target_id=log_id: (
                                            close_dialog(app, dialog),
                                            app.delete_meal_log(target_id),
                                        ),
                                    ),
                                ),
                            ],
                            spacing=10,
                            wrap=True,
                        ),
                    ],
                    spacing=10,
                ),
            )
        )

    meal_logs_section = SurfaceSection(
        app,
        app.t("meal_logs"),
        ft.Column(
            meal_log_rows
            or [ft.Text(app.t("no_meal_logs"), color=app.surface_muted_color())],
            spacing=10,
        ),
    )

    return ft.Column(
        [
            calorie_section,
            search_section,
            builder_section,
            templates_section,
            meal_logs_section,
        ],
        spacing=20,
    )
