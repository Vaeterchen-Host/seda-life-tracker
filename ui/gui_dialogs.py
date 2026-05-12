# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Dialog helpers extracted from ui.gui."""

# pylint: disable=all

from dataclasses import fields

import flet as ft

from model.classes_food import BigSeven, Meal, NutrientSummary
from application.builders import (
    create_food_instance_from_food_row,
)
from application.meal_service import (
    create_single_food_meal,
)
from ui.gui_theme import (
    BIG_SEVEN_LABELS,
    BIG_SEVEN_LABELS_DE,
    BRAND_MINT,
    BRAND_RED,
)


# ---------------------------
# Dialog helpers
# The GUI uses small dialogs for confirmations and edit flows.
# ---------------------------
def close_dialog(self, dialog):
    """Close one currently visible dialog. Partly AI-generated."""
    dialog.open = False
    self.page.update()


def open_confirm_dialog(self, title, content, on_confirm):
    """Show a reusable yes/no confirmation dialog. Partly AI-generated."""
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(title),
        content=ft.Text(content),
        actions=[
            ft.TextButton(
                self.t("no_keep"),
                on_click=lambda _: self.close_dialog(dialog),
            ),
            ft.FilledButton(
                self.t("yes_delete"),
                style=ft.ButtonStyle(bgcolor=BRAND_RED),
                on_click=lambda _: on_confirm(dialog),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    self.page.show_dialog(dialog)


def open_license_dialog(self, _=None):
    """Show the full license text in a readable scrollable dialog. Partly AI-generated."""
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(self.t("license_dialog_title")),
        content=ft.Container(
            width=760,
            height=560,
            content=ft.Column(
                [
                    ft.Text(
                        self.get_license_text(),
                        selectable=True,
                        color=self.primary_text_color(),
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
            ),
        ),
        actions=[
            ft.FilledButton(
                self.t("close"),
                on_click=lambda _: self.close_dialog(dialog),
            )
        ],
    )
    self.page.show_dialog(dialog)


def open_activity_edit_dialog(self, activity_log):
    """Edit one activity entry in-place without leaving the activity page. Partly AI-generated."""
    name_field = ft.TextField(
        label=self.t("activity_name"),
        value=activity_log.activity_name,
    )
    calories_field = ft.TextField(
        label=self.t("calories_burned"),
        value=str(activity_log.calories_burned),
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    duration_field = ft.TextField(
        label=self.t("duration_minutes"),
        value=(
            ""
            if activity_log.activity_value is None
            else str(activity_log.activity_value)
        ),
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    timestamp_field = ft.TextField(
        label=self.t("optional_timestamp"),
        value=self.format_timestamp(activity_log.timestamp),
        helper=self.t("use_now_when_empty"),
        hint_text=self.timestamp_input_hint(),
    )

    def save_changes(_):
        """Persist the dialog values to DB and in-memory state."""
        try:
            new_activity_name = name_field.value.strip()
            new_calories = self.parse_required_float(calories_field.value)
            new_duration = self.parse_optional_float(duration_field.value)
            new_timestamp = self.parse_optional_timestamp(timestamp_field.value)
            if new_timestamp is None:
                new_timestamp = activity_log.timestamp

            self.main_db.update_activity_log(
                activity_log.id,
                new_activity_name,
                new_calories,
                new_duration,
                activity_log.unit_type,
                new_timestamp,
            )
            self.current_user.activity_log_handler.update_log(
                activity_log.id,
                new_activity_name=new_activity_name,
                new_calories_burned=new_calories,
                new_activity_value=new_duration,
                new_timestamp=new_timestamp,
            )
            self.close_dialog(dialog)
            self.show_message(self.t("msg_activity_updated"))
            self.render()
        except Exception as exc:
            self.show_message(str(exc), error=True)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(self.t("edit_log")),
        content=ft.Container(
            width=440,
            content=ft.Column(
                [
                    name_field,
                    calories_field,
                    duration_field,
                    timestamp_field,
                ],
                tight=True,
            ),
        ),
        actions=[
            ft.TextButton(
                self.t("cancel"),
                on_click=lambda _: self.close_dialog(dialog),
            ),
            ft.FilledButton(self.t("save"), on_click=save_changes),
        ],
    )
    self.page.show_dialog(dialog)


def open_meal_log_dialog(self, meal: Meal = None, existing_log=None):
    """Create or edit one meal log via a small dialog. Partly AI-generated."""
    meal_templates = self.get_meal_templates()
    selected_meal = meal if meal is not None else existing_log.meal
    meal_dropdown = ft.Dropdown(
        label=self.t("meal_templates"),
        value=str(selected_meal.id) if selected_meal is not None else None,
        options=[
            ft.DropdownOption(
                key=str(template.id), text=self.get_meal_display_name(template)
            )
            for template in meal_templates
        ],
    )
    amount_field = ft.TextField(
        label=self.t("consumed_amount"),
        value="" if existing_log is None else str(existing_log.amount),
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    unit_dropdown = ft.Dropdown(
        label=self.t("unit_type"),
        value="g" if existing_log is None else existing_log.unit_type,
        options=[
            ft.DropdownOption(key="g", text="g"),
            ft.DropdownOption(key="ml", text="ml"),
        ],
    )
    timestamp_field = ft.TextField(
        label=self.t("optional_timestamp"),
        value=(
            ""
            if existing_log is None
            else self.format_timestamp(existing_log.timestamp)
        ),
        helper=self.t("use_now_when_empty"),
        hint_text=self.timestamp_input_hint(),
    )

    title = (
        self.t("edit_log")
        if existing_log is not None
        else (
            self.t("meal_log_form_title")
            if meal is not None
            else self.t("single_food_form_title")
        )
    )
    copy = (
        self.t("meal_log_form_copy")
        if meal is not None or existing_log is not None
        else self.t("single_food_form_copy")
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
                raise ValueError(self.t("msg_no_template_selected"))

            amount = self.parse_required_float(amount_field.value)
            timestamp = self.parse_optional_timestamp(timestamp_field.value)

            if existing_log is None:
                new_log = self.current_user.meal_log_handler.create_log(
                    None,
                    chosen_meal,
                    amount,
                    unit_dropdown.value,
                    timestamp,
                )
                db_id = self.main_db.add_meal_log(
                    self.current_user.user_id,
                    chosen_meal.id,
                    amount,
                    unit_dropdown.value,
                    new_log.timestamp,
                )
                new_log.set_database_id(db_id)
                self.show_message(self.t("msg_meal_logged"))
            else:
                self.main_db.update_meal_log(
                    existing_log.id,
                    chosen_meal.id,
                    amount,
                    unit_dropdown.value,
                    timestamp or existing_log.timestamp,
                )
                self.current_user.meal_log_handler.update_log(
                    existing_log.id,
                    new_meal=chosen_meal,
                    new_amount=amount,
                    new_unit_type=unit_dropdown.value,
                    new_timestamp=timestamp or existing_log.timestamp,
                )
                self.show_message(self.t("msg_meal_log_updated"))

            self.close_dialog(dialog)
            self.render()
        except Exception as exc:
            self.show_message(str(exc), error=True)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(title),
        content=ft.Container(
            width=460,
            content=ft.Column(
                [
                    ft.Text(copy, color=self.surface_muted_color()),
                    meal_dropdown,
                    amount_field,
                    unit_dropdown,
                    timestamp_field,
                ],
                tight=True,
            ),
        ),
        actions=[
            ft.TextButton(
                self.t("cancel"),
                on_click=lambda _: self.close_dialog(dialog),
            ),
            ft.FilledButton(self.t("save"), on_click=save_log),
        ],
    )
    self.page.show_dialog(dialog)


def open_meal_log_details_dialog(self, meal_log):
    """Display Big Seven and nutrient summary values of one meal log. Partly AI-generated."""
    big_seven_controls = []
    labels = BIG_SEVEN_LABELS_DE if self.current_language == "de" else BIG_SEVEN_LABELS
    for nutrient_field in fields(BigSeven):
        value = getattr(meal_log.big_seven, nutrient_field.name)
        if value is None:
            continue
        big_seven_controls.append(
            self.build_label_value_row(
                labels.get(nutrient_field.name, nutrient_field.name),
                self.format_amount(value, "g"),
            )
        )

    summary_controls = []
    for nutrient_field in fields(NutrientSummary):
        value = getattr(meal_log.nutrient_summary, nutrient_field.name)
        if value is None:
            continue
        label = nutrient_field.name.replace("_", " ").title()
        summary_controls.append(
            self.build_label_value_row(label, self.format_amount(value))
        )

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(self.t("meal_log_details")),
        content=ft.Container(
            width=640,
            height=520,
            content=ft.Column(
                [
                    ft.Text(
                        f"{self.get_meal_display_name(meal_log.meal)} | "
                        f"{self.format_amount(meal_log.amount, meal_log.unit_type)}",
                        color=self.surface_muted_color(),
                    ),
                    self.build_surface_section(
                        self.t("big_seven"),
                        ft.Column(
                            big_seven_controls
                            or [ft.Text("-", color=self.surface_muted_color())],
                            spacing=8,
                        ),
                    ),
                    self.build_surface_section(
                        self.t("nutrient_summary"),
                        ft.Column(
                            summary_controls
                            or [ft.Text("-", color=self.surface_muted_color())],
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
            ft.FilledButton(
                self.t("close"),
                on_click=lambda _: self.close_dialog(dialog),
            )
        ],
    )
    self.page.show_dialog(dialog)


def open_food_amount_dialog(self, food_row, mode):
    """Ask for an amount before adding a food to the builder or directly logging it. Partly AI-generated."""
    amount_field = ft.TextField(
        label=self.t("amount_g_ml"),
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    timestamp_field = ft.TextField(
        label=self.t("optional_timestamp"),
        helper=self.t("use_now_when_empty"),
        hint_text=self.timestamp_input_hint(),
    )

    title = (
        self.t("single_food_form_title")
        if mode == "consume"
        else self.t("add_to_template")
    )
    copy = (
        self.t("single_food_form_copy") if mode == "consume" else self.t("builder_copy")
    )

    def confirm(_):
        """Apply the dialog result to the builder or a direct meal log."""
        try:
            amount = self.parse_required_float(amount_field.value)
            if mode == "consume":
                timestamp = self.parse_optional_timestamp(timestamp_field.value)
                single_food_meal = create_single_food_meal(self.main_db, food_row)
                new_log = self.current_user.meal_log_handler.create_log(
                    None,
                    single_food_meal,
                    amount,
                    food_row["unit_type"],
                    timestamp,
                )
                db_id = self.main_db.add_meal_log(
                    self.current_user.user_id,
                    single_food_meal.id,
                    amount,
                    food_row["unit_type"],
                    new_log.timestamp,
                )
                new_log.set_database_id(db_id)
                self.show_message(self.t("msg_single_food_logged"))
            else:
                self.meal_builder_items.append(
                    create_food_instance_from_food_row(food_row, amount)
                )
                self.show_message(self.t("msg_food_added"))
            self.close_dialog(dialog)
            self.render()
        except Exception as exc:
            self.show_message(str(exc), error=True)

    dialog_controls = [
        ft.Text(copy, color=self.surface_muted_color()),
        amount_field,
    ]
    if mode == "consume":
        dialog_controls.append(timestamp_field)

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(title),
        content=ft.Container(
            width=420,
            content=ft.Column(dialog_controls, tight=True),
        ),
        actions=[
            ft.TextButton(
                self.t("cancel"),
                on_click=lambda _: self.close_dialog(dialog),
            ),
            ft.FilledButton(self.t("save"), on_click=confirm),
        ],
    )
    self.page.show_dialog(dialog)
