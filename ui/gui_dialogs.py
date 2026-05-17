# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Dialog helpers for the SEDA GUI. Partly AI-generated."""

# pylint: disable=all

from __future__ import annotations

from dataclasses import fields
from typing import TYPE_CHECKING

import flet as ft

from application.builders import create_food_instance_from_food_row
from application.meal_service import create_single_food_meal
from model.classes_food import BigSeven, Meal, NutrientSummary
from ui.gui_components import (
    DatePickerField,
    LabelValueRow,
    PrimaryButton,
    SurfaceSection,
    TimePickerField,
)
from ui.gui_theme import (
    BIG_SEVEN_LABELS,
    BIG_SEVEN_LABELS_DE,
    NUTRIENT_SUMMARY_LABELS,
    NUTRIENT_SUMMARY_LABELS_DE,
    NUTRIENT_SUMMARY_UNITS,
    SEDA_RED,
)

if TYPE_CHECKING:
    from ui.gui import SedaGuiApp


def close_dialog(app: "SedaGuiApp", dialog):
    """Close one currently visible dialog. Partly AI-generated."""
    dialog.open = False
    app.page.update()


def open_confirm_dialog(app: "SedaGuiApp", title, content, on_confirm):
    """Show a reusable yes/no confirmation dialog. Partly AI-generated."""
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(title),
        content=ft.Text(content),
        actions=[
            ft.TextButton(
                app.t("no_keep"),
                on_click=lambda _: close_dialog(app, dialog),
            ),
            ft.FilledButton(
                content=app.t("yes_delete"),
                style=ft.ButtonStyle(
                    bgcolor=SEDA_RED,
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
                on_click=lambda _: on_confirm(dialog),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    app.page.show_dialog(dialog)


def open_license_dialog(app: "SedaGuiApp", _=None):
    """Show the full license text in a readable scrollable dialog. Partly AI-generated."""
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(app.t("license_dialog_title")),
        content=ft.Container(
            width=760,
            height=560,
            content=ft.Column(
                [
                    ft.Text(
                        app.get_license_text(),
                        selectable=True,
                        color=app.primary_text_color(),
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
            ),
        ),
        actions=[
            PrimaryButton(
                app.t("close"),
                on_click=lambda _: close_dialog(app, dialog),
            )
        ],
    )
    app.page.show_dialog(dialog)


def open_activity_edit_dialog(app: "SedaGuiApp", activity_log):
    """Edit one activity entry in-place without leaving the activity page. Partly AI-generated."""
    name_field = ft.TextField(
        label=app.t("activity_name"),
        value=activity_log.activity_name,
    )
    calories_field = ft.TextField(
        label=app.t("calories_burned"),
        value=str(activity_log.calories_burned),
        keyboard_type=ft.KeyboardType.TEXT,
    )
    duration_field = ft.TextField(
        label=app.t("duration_minutes"),
        value=(
            ""
            if activity_log.activity_value is None
            else str(activity_log.activity_value)
        ),
        keyboard_type=ft.KeyboardType.TEXT,
    )
    selected_date, selected_time = app.split_timestamp(activity_log.timestamp)
    date_field = DatePickerField(
        app,
        app.t("date"),
        value=selected_date,
        expand=True,
    )
    time_field = TimePickerField(
        app,
        app.t("time"),
        value=selected_time,
    )

    def save_changes(_):
        """Persist the dialog values to DB and in-memory state."""
        try:
            new_activity_name = name_field.value.strip()
            new_calories = app.parse_required_float(calories_field.value)
            new_duration = app.parse_optional_float(duration_field.value)
            new_timestamp = app.combine_date_and_time(
                date_field.selected_date,
                time_field.selected_time,
            )

            app.main_db.update_activity_log(
                activity_log.id,
                new_activity_name,
                new_calories,
                new_duration,
                "minutes",
                new_timestamp or activity_log.timestamp,
            )
            app.current_user.activity_log_handler.update_log(
                activity_log.id,
                new_activity_name=new_activity_name,
                new_calories_burned=new_calories,
                new_activity_value=new_duration,
                new_timestamp=new_timestamp,
            )
            close_dialog(app, dialog)
            app.show_message(app.t("msg_activity_updated"))
            app.render()
        except Exception as exc:
            app.show_message(str(exc), error=True)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(app.t("edit_log")),
        content=ft.Container(
            width=440,
            content=ft.Column(
                [
                    name_field,
                    calories_field,
                    duration_field,
                    date_field,
                    time_field,
                ],
                tight=True,
            ),
        ),
        actions=[
            ft.TextButton(
                app.t("cancel"),
                on_click=lambda _: close_dialog(app, dialog),
            ),
            PrimaryButton(
                app.t("save"),
                on_click=save_changes,
            ),
        ],
    )
    app.page.show_dialog(dialog)


def open_activity_create_dialog(app: "SedaGuiApp", _=None):
    """Create one activity entry through a dedicated dialog. AI-generated."""
    name_field = ft.TextField(
        label=app.t("activity_name"),
        autofocus=True,
    )
    calories_field = ft.TextField(
        label=app.t("calories_burned"),
        keyboard_type=ft.KeyboardType.TEXT,
    )
    duration_field = ft.TextField(
        label=app.t("duration_minutes"),
        keyboard_type=ft.KeyboardType.TEXT,
    )
    date_field = DatePickerField(
        app,
        app.t("date"),
        expand=True,
    )
    time_field = TimePickerField(
        app,
        app.t("time"),
        expand=True,
    )

    def save_activity(_):
        """Validate and persist one new activity entry. AI-generated."""
        try:
            activity_name = name_field.value.strip()
            calories = app.parse_required_float(calories_field.value)
            duration = app.parse_optional_float(duration_field.value)
            timestamp = app.combine_date_and_time(
                date_field.selected_date,
                time_field.selected_time,
            )
            app.add_activity_log(activity_name, calories, duration, timestamp)
            close_dialog(app, dialog)
        except Exception as exc:
            app.show_message(str(exc), error=True)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(app.t("add_activity")),
        content=ft.Container(
            width=460,
            content=ft.Column(
                [
                    ft.Text(app.t("activity_copy"), color=app.surface_muted_color()),
                    name_field,
                    calories_field,
                    duration_field,
                    date_field,
                    time_field,
                ],
                tight=True,
            ),
        ),
        actions=[
            ft.TextButton(
                app.t("cancel"),
                on_click=lambda _: close_dialog(app, dialog),
            ),
            PrimaryButton(
                app.t("save"),
                on_click=save_activity,
            ),
        ],
    )
    app.page.show_dialog(dialog)


def open_water_log_dialog(app: "SedaGuiApp", _=None):
    """Create one water entry through a dedicated dialog. AI-generated."""
    amount_field = ft.TextField(
        label=app.t("amount_ml"),
        keyboard_type=ft.KeyboardType.NUMBER,
        autofocus=True,
    )
    date_field = DatePickerField(
        app,
        app.t("date"),
        expand=True,
    )
    time_field = TimePickerField(
        app,
        app.t("time"),
        expand=True,
    )

    def save_water(_):
        """Validate and persist one new water entry. AI-generated."""
        try:
            amount = app.parse_required_int(amount_field.value)
            timestamp = app.combine_date_and_time(
                date_field.selected_date,
                time_field.selected_time,
            )
            app.add_water_log(amount, timestamp)
            close_dialog(app, dialog)
        except Exception as exc:
            app.show_message(str(exc), error=True)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(app.t("add_water")),
        content=ft.Container(
            width=440,
            content=ft.Column(
                [
                    amount_field,
                    date_field,
                    time_field,
                ],
                tight=True,
            ),
        ),
        actions=[
            ft.TextButton(
                app.t("cancel"),
                on_click=lambda _: close_dialog(app, dialog),
            ),
            PrimaryButton(
                app.t("save"),
                on_click=save_water,
            ),
        ],
    )
    app.page.show_dialog(dialog)


def open_weight_log_dialog(app: "SedaGuiApp", _=None):
    """Create one weight entry through a dedicated dialog. AI-generated."""
    weight_field = ft.TextField(
        label=app.t("weight_kg"),
        keyboard_type=ft.KeyboardType.TEXT,
        autofocus=True,
    )
    date_field = DatePickerField(
        app,
        app.t("date"),
        expand=True,
    )
    time_field = TimePickerField(
        app,
        app.t("time"),
        expand=True,
    )

    def save_weight(_):
        """Validate and persist one new weight entry. AI-generated."""
        try:
            weight = app.parse_required_float(weight_field.value)
            timestamp = app.combine_date_and_time(
                date_field.selected_date,
                time_field.selected_time,
            )
            app.add_weight_log(weight, timestamp)
            close_dialog(app, dialog)
        except Exception as exc:
            app.show_message(str(exc), error=True)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(app.t("add_weight_log")),
        content=ft.Container(
            width=440,
            content=ft.Column(
                [
                    weight_field,
                    date_field,
                    time_field,
                ],
                tight=True,
            ),
        ),
        actions=[
            ft.TextButton(
                app.t("cancel"),
                on_click=lambda _: close_dialog(app, dialog),
            ),
            PrimaryButton(
                app.t("save"),
                on_click=save_weight,
            ),
        ],
    )
    app.page.show_dialog(dialog)


def open_meal_log_dialog(app: "SedaGuiApp", meal: Meal = None, existing_log=None):
    """Create or edit one meal log via a small dialog. Partly AI-generated."""
    meal_templates = app.get_meal_templates()
    selected_meal = meal if meal is not None else existing_log.meal
    is_portion_mode = meal is not None or (
        existing_log is not None and existing_log.unit_type == "portion"
    )
    meal_dropdown_options = [
        ft.DropdownOption(key=str(template.id), text=app.get_meal_display_name(template))
        for template in meal_templates
    ]
    if selected_meal is not None and all(
        option.key != str(selected_meal.id) for option in meal_dropdown_options
    ):
        meal_dropdown_options.append(
            ft.DropdownOption(
                key=str(selected_meal.id),
                text=app.get_meal_display_name(selected_meal),
            )
        )
    meal_dropdown = ft.Dropdown(
        label=app.t("meal_templates"),
        value=str(selected_meal.id) if selected_meal is not None else None,
        options=meal_dropdown_options,
    )
    amount_field = ft.TextField(
        label=app.t("consumed_amount"),
        value=(
            "1.0"
            if existing_log is None and is_portion_mode
            else ("" if existing_log is None else str(existing_log.amount))
        ),
        keyboard_type=ft.KeyboardType.TEXT,
    )
    unit_control = (
        ft.TextField(
            label=app.t("unit_type"),
            value=app.t("portion"),
            read_only=True,
        )
        if is_portion_mode
        else ft.Dropdown(
            label=app.t("unit_type"),
            value="g" if existing_log is None else existing_log.unit_type,
            options=[
                ft.DropdownOption(key="g", text="g"),
                ft.DropdownOption(key="ml", text="ml"),
            ],
        )
    )
    selected_date, selected_time = app.split_timestamp(
        None if existing_log is None else existing_log.timestamp
    )
    date_field = DatePickerField(
        app,
        app.t("date"),
        value=selected_date,
        expand=True,
    )
    time_field = TimePickerField(
        app,
        app.t("time"),
        value=selected_time,
    )

    title = (
        app.t("edit_log")
        if existing_log is not None
        else (
            app.t("meal_log_form_title")
            if meal is not None
            else app.t("single_food_form_title")
        )
    )
    copy = (
        app.t("meal_log_form_copy")
        if meal is not None or existing_log is not None
        else app.t("single_food_form_copy")
    )

    def save_log(_):
        """Persist one new or updated meal log."""
        try:
            chosen_meal = next(
                (
                    template
                    for template in meal_templates
                    if str(template.id) == meal_dropdown.value
                ),
                None,
            )
            if chosen_meal is None:
                raise ValueError(app.t("msg_no_template_selected"))

            amount = app.parse_required_float(amount_field.value)
            timestamp = app.combine_date_and_time(
                date_field.selected_date,
                time_field.selected_time,
            )
            selected_unit_type = "portion" if is_portion_mode else unit_control.value

            if existing_log is None:
                new_log = app.current_user.meal_log_handler.create_log(
                    None,
                    chosen_meal,
                    amount,
                    selected_unit_type,
                    timestamp,
                )
                db_id = app.main_db.add_meal_log(
                    app.current_user.user_id,
                    chosen_meal.id,
                    amount,
                    selected_unit_type,
                    new_log.timestamp,
                )
                new_log.set_database_id(db_id)
                app.add_food_water_log_from_meal_log(new_log)
                app.show_message(app.t("msg_meal_logged"))
            else:
                app.main_db.update_meal_log(
                    existing_log.id,
                    chosen_meal.id,
                    amount,
                    selected_unit_type,
                    timestamp or existing_log.timestamp,
                )
                app.current_user.meal_log_handler.update_log(
                    existing_log.id,
                    new_meal=chosen_meal,
                    new_amount=amount,
                    new_unit_type=selected_unit_type,
                    new_timestamp=timestamp or existing_log.timestamp,
                )
                app.show_message(app.t("msg_meal_log_updated"))

            close_dialog(app, dialog)
            app.render()
        except Exception as exc:
            app.show_message(str(exc), error=True)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(title),
        content=ft.Container(
            width=460,
            content=ft.Column(
                [
                    ft.Text(copy, color=app.surface_muted_color()),
                    meal_dropdown,
                    amount_field,
                    unit_control,
                    date_field,
                    time_field,
                ],
                tight=True,
            ),
        ),
        actions=[
            ft.TextButton(
                app.t("cancel"),
                on_click=lambda _: close_dialog(app, dialog),
            ),
            PrimaryButton(
                app.t("save"),
                on_click=save_log,
            ),
        ],
    )
    app.page.show_dialog(dialog)


def open_meal_log_details_dialog(app: "SedaGuiApp", meal_log):
    """Display Big Seven and nutrient summary values of one meal log. Partly AI-generated."""
    big_seven_controls = []
    labels = BIG_SEVEN_LABELS_DE if app.current_language == "de" else BIG_SEVEN_LABELS
    summary_labels = (
        NUTRIENT_SUMMARY_LABELS_DE
        if app.current_language == "de"
        else NUTRIENT_SUMMARY_LABELS
    )
    for nutrient_field in fields(BigSeven):
        value = getattr(meal_log.big_seven, nutrient_field.name)
        if value is None:
            continue
        big_seven_controls.append(
            LabelValueRow(
                app,
                labels.get(nutrient_field.name, nutrient_field.name),
                app.format_amount(value, "g"),
            )
        )

    summary_controls = []
    for nutrient_field in fields(NutrientSummary):
        value = getattr(meal_log.nutrient_summary, nutrient_field.name)
        if value is None:
            continue
        label = summary_labels.get(
            nutrient_field.name,
            nutrient_field.name.replace("_", " ").title(),
        )
        unit = NUTRIENT_SUMMARY_UNITS.get(nutrient_field.name, "")
        summary_controls.append(
            LabelValueRow(app, label, app.format_amount(value, unit))
        )

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(app.t("meal_log_details")),
        content=ft.Container(
            width=640,
            height=520,
            content=ft.Column(
                [
                    ft.Text(
                        f"{app.get_meal_display_name(meal_log.meal)} | "
                        f"{app.format_amount(meal_log.amount, meal_log.unit_type)}",
                        color=app.surface_muted_color(),
                    ),
                    SurfaceSection(
                        app,
                        app.t("big_seven"),
                        ft.Column(
                            big_seven_controls
                            or [ft.Text("-", color=app.surface_muted_color())],
                            spacing=8,
                        ),
                    ),
                    SurfaceSection(
                        app,
                        app.t("nutrient_summary"),
                        ft.Column(
                            summary_controls
                            or [ft.Text("-", color=app.surface_muted_color())],
                            spacing=8,
                            scroll=ft.ScrollMode.AUTO,
                        ),
                    ),
                ],
                spacing=12,
                scroll=ft.ScrollMode.AUTO,
            ),
        ),
        actions=[
            PrimaryButton(
                app.t("close"),
                on_click=lambda _: close_dialog(app, dialog),
            )
        ],
    )
    app.page.show_dialog(dialog)


def open_food_amount_dialog(app: "SedaGuiApp", food_row, mode):
    """Ask for an amount before adding a food to the builder or directly logging it. Partly AI-generated."""
    amount_field = ft.TextField(
        label=app.t("amount_g_ml"),
        keyboard_type=ft.KeyboardType.TEXT,
    )
    date_field = DatePickerField(app, app.t("date"), expand=True)
    time_field = TimePickerField(
        app,
        app.t("time"),
    )

    title = (
        app.t("single_food_form_title")
        if mode == "consume"
        else app.t("add_to_template")
    )
    copy = (
        app.t("single_food_form_copy") if mode == "consume" else app.t("builder_copy")
    )

    def confirm(_):
        """Apply the dialog result to the builder or a direct meal log."""
        try:
            amount = app.parse_required_float(amount_field.value)
            if mode == "consume":
                timestamp = app.combine_date_and_time(
                    date_field.selected_date,
                    time_field.selected_time,
                )
                single_food_meal = create_single_food_meal(
                    app.main_db,
                    app.current_user.user_id,
                    food_row,
                )
                new_log = app.current_user.meal_log_handler.create_log(
                    None,
                    single_food_meal,
                    amount,
                    food_row["unit_type"],
                    timestamp,
                )
                db_id = app.main_db.add_meal_log(
                    app.current_user.user_id,
                    single_food_meal.id,
                    amount,
                    food_row["unit_type"],
                    new_log.timestamp,
                )
                new_log.set_database_id(db_id)
                app.add_food_water_log_from_meal_log(new_log)
                app.show_message(app.t("msg_single_food_logged"))
            else:
                app.meal_builder_items.append(
                    create_food_instance_from_food_row(food_row, amount)
                )
                app.show_message(app.t("msg_food_added"))
            app.food_search_term = ""
            close_dialog(app, dialog)
            app.render()
        except Exception as exc:
            app.show_message(str(exc), error=True)

    dialog_controls = [
        ft.Text(copy, color=app.surface_muted_color()),
        amount_field,
    ]
    if mode == "consume":
        dialog_controls.extend([date_field, time_field])

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(title),
        content=ft.Container(
            width=420,
            content=ft.Column(dialog_controls, tight=True),
        ),
        actions=[
            ft.TextButton(
                app.t("cancel"),
                on_click=lambda _: close_dialog(app, dialog),
            ),
            PrimaryButton(
                app.t("save"),
                on_click=confirm,
            ),
        ],
    )
    app.page.show_dialog(dialog)
