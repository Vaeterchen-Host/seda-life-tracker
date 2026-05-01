# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Graphical user interface for SEDA. This file is in this version mostly ai-generated."""

# pylint: disable=all

import sys
from dataclasses import fields
from datetime import datetime
from pathlib import Path

import flet as ft

# Search path for model imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.class_user import User
from model.classes_food import BigSeven, Food, Meal, NutrientSummary
from model.classes_log import MealLog
from model.controller import (
    create_food_instance_from_food_row,
    create_meal_instances,
    create_single_food_meal,
    create_user_instance_from_db,
    get_today_calorie_status,
    get_today_water_status,
    refresh_user_logs_from_db,
)
from model.database import Database, FoodDatabase
from ui.translations import get_translation

PAGE_BACKGROUND = "#111315"
SURFACE_BACKGROUND = "#171B21"
SURFACE_BACKGROUND_ALT = "#1C2626"
SURFACE_BORDER = "#3E4B5D"
SURFACE_MUTED = "#AAB5C3"
BRAND_MINT = "#00A69C"
BRAND_YELLOW = "#EBE46E"
BRAND_RED = "#EB6E85"

NAV_ITEMS = [
    ("dashboard", "nav_dashboard", ft.Icons.DASHBOARD_OUTLINED),
    ("nutrition", "nav_nutrition", ft.Icons.RESTAURANT_MENU),
    ("water", "nav_water", ft.Icons.WATER_DROP_OUTLINED),
    ("activity", "nav_activity", ft.Icons.DIRECTIONS_RUN),
    ("profile", "nav_profile", ft.Icons.PERSON_OUTLINE),
    ("about", "nav_about", ft.Icons.INFO_OUTLINE),
]

BIG_SEVEN_LABELS = {
    "fat": "Fat",
    "saturated_fat": "Saturated fat",
    "carbohydrate": "Carbohydrate",
    "fibre": "Fibre",
    "sugar": "Sugar",
    "protein": "Protein",
    "salt": "Salt",
}

BIG_SEVEN_LABELS_DE = {
    "fat": "Fett",
    "saturated_fat": "Gesättigte Fettsäuren",
    "carbohydrate": "Kohlenhydrate",
    "fibre": "Ballaststoffe",
    "sugar": "Zucker",
    "protein": "Eiweiß",
    "salt": "Salz",
}


class SedaGuiApp:
    """Desktop-first Flet GUI for the SEDA learning project."""

    # ---------------------------
    # Setup and state
    # This part stores shared page state and prepares the app shell.
    # ---------------------------
    def __init__(self, page: ft.Page):
        """Store app-wide state and load the currently active user."""
        self.page = page
        self.main_db = Database()
        self.food_db = FoodDatabase()

        self.current_user = None
        self.current_view = "dashboard"
        self.current_language = "en"

        self.status_message = get_translation("en", "status_ready")
        self.status_is_error = False

        self.food_search_term = ""
        self.food_search_results = []
        # Cache food DB rows so repeated redraws and language switches stay cheap.
        self.food_row_cache = {}
        self.license_text_cache = None
        self.meal_builder_name = ""
        self.meal_builder_items = []
        self.editing_meal_template_id = None

        self.configure_page()
        self.load_current_user()

    def configure_page(self):
        """Apply the fixed desktop page settings."""
        self.page.title = "seda - desktop gui"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.bgcolor = self.page_background_color()
        self.page.padding = 0
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.window.min_width = 1180
        self.page.window.min_height = 860

    def t(self, key, **kwargs):
        """Return a translated GUI string for the current language."""
        return get_translation(self.current_language, key, **kwargs)

    def is_dark_mode(self):
        """Return whether the current page theme is dark."""
        return self.page.theme_mode in (ft.ThemeMode.DARK, "dark")

    def toggle_theme(self, _=None):
        """Switch between dark and light mode and redraw the desktop shell."""
        self.page.theme_mode = (
            ft.ThemeMode.LIGHT if self.is_dark_mode() else ft.ThemeMode.DARK
        )  # refactored by ai
        self.page.bgcolor = self.page_background_color()
        self.render()

    def page_background_color(self):
        """Return the page background color for the active theme mode."""
        return PAGE_BACKGROUND if self.is_dark_mode() else "#EEF2F5"

    def surface_background_color(self):
        """Return the default card background for the active theme mode."""
        return SURFACE_BACKGROUND if self.is_dark_mode() else "#FFFFFF"

    def surface_background_alt_color(self):
        """Return the softer secondary background for the active theme mode."""
        return SURFACE_BACKGROUND_ALT if self.is_dark_mode() else "#F4F9F8"

    def surface_border_color(self):
        """Return the border color for framed desktop sections."""
        return SURFACE_BORDER if self.is_dark_mode() else "#C9D5DE"

    def surface_muted_color(self):
        """Return the muted helper text color for the active theme mode."""
        return SURFACE_MUTED if self.is_dark_mode() else "#5E6B78"

    def primary_text_color(self):
        """Return the main readable text color for the active theme mode."""
        return ft.Colors.WHITE if self.is_dark_mode() else "#18212B"

    def show_message(self, message, error=False):
        """Show short GUI feedback as a snack bar."""
        self.status_message = message
        self.status_is_error = error
        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(message),
                bgcolor=BRAND_RED if error else BRAND_MINT,
            )
        )
        self.page.update()

    def load_current_user(self):
        """Load the first available user and its logs into memory."""
        users = self.main_db.get_all_users()
        if not users:
            self.current_user = None
            return
        self.current_user = create_user_instance_from_db(self.main_db, users[0])
        refresh_user_logs_from_db(self.main_db, self.current_user)

    def refresh_current_user_logs(self):
        """Reload the current user's handlers from the database."""
        if self.current_user is not None:
            refresh_user_logs_from_db(self.main_db, self.current_user)

    def navigate(self, view_name):
        """Switch between the main GUI areas."""
        self.current_view = view_name
        self.render()

    def change_language(self, language):
        """Switch between English and German and redraw the page."""
        self.current_language = language
        self.show_message(self.t("msg_language_changed"))
        self.render()

    def reset_meal_builder(self):
        """Clear the temporary meal-template builder state."""
        self.meal_builder_name = ""
        self.meal_builder_items = []
        self.editing_meal_template_id = None

    def start_meal_template_edit(self, meal: Meal):
        """Load one template into the builder so it can be rebuilt visually."""
        self.editing_meal_template_id = meal.id
        self.meal_builder_name = meal.name
        self.meal_builder_items = list(meal.food_items)
        self.navigate("nutrition")

    # ---------------------------
    # Formatting and validation helpers
    # These helpers keep the action handlers shorter and easier to read.
    # ---------------------------
    def format_gender(self, gender_code):
        """Translate one stored gender code into a readable label."""
        mapping = {
            "m": self.t("gender_m"),
            "f": self.t("gender_f"),
            "d": self.t("gender_d"),
        }
        return mapping.get(gender_code, gender_code)

    def format_fitness(self, fitness_code):
        """Translate one stored fitness code into a readable label."""
        mapping = {
            "beginner": self.t("fitness_beginner"),
            "intermediate": self.t("fitness_intermediate"),
            "advanced": self.t("fitness_advanced"),
        }
        return mapping.get(fitness_code, fitness_code)

    def format_timestamp(self, timestamp):
        """Render stored ISO timestamps in the current frontend locale format."""
        if not timestamp:
            return "-"
        try:
            dt_value = datetime.fromisoformat(timestamp)
            if self.current_language == "de":
                return dt_value.strftime("%d.%m.%Y %H:%M")
            return dt_value.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            return str(timestamp)

    def format_birthdate(self, birthdate):
        """Render stored ISO birthdates in the current frontend locale format."""
        if not birthdate:
            return ""
        try:
            date_value = datetime.fromisoformat(birthdate)
            if self.current_language == "de":
                return date_value.strftime("%d.%m.%Y")
            return date_value.strftime("%Y-%m-%d")
        except ValueError:
            return str(birthdate)

    def birthdate_input_hint(self):
        """Return the locale-specific birthdate input hint for form fields."""
        return "TT.MM.JJJJ" if self.current_language == "de" else "YYYY-MM-DD"

    def timestamp_input_hint(self):
        """Return the locale-specific timestamp input hint for form fields."""
        return (
            "TT.MM.JJJJ HH:MM" if self.current_language == "de" else "YYYY-MM-DD HH:MM"
        )

    def format_amount(self, value, suffix=""):
        """Render numeric values without unnecessary trailing zeros."""
        if value is None:
            return "-"
        if isinstance(value, float):
            text = f"{value:.2f}".rstrip("0").rstrip(".")
        else:
            text = str(value)
        return f"{text} {suffix}".strip()

    def sort_logs_desc(self, logs):
        """Show logs newest first on screen regardless of internal list order."""
        return sorted(
            logs,
            key=lambda log: log.timestamp or "",
            reverse=True,
        )

    def parse_birthdate(self, raw_value):
        """Validate one localized date input and store it as ISO date text."""
        try:
            cleaned = raw_value.strip()
            if self.current_language == "de":
                return datetime.strptime(cleaned, "%d.%m.%Y").date().isoformat()
            return datetime.strptime(cleaned, "%Y-%m-%d").date().isoformat()
        except ValueError as exc:
            try:
                return datetime.fromisoformat(raw_value.strip()).date().isoformat()
            except ValueError:
                raise ValueError(self.t("msg_invalid_birthdate")) from exc

    def parse_required_int(self, raw_value):
        """Read one required integer field from a text input."""
        try:
            return int(raw_value)
        except (TypeError, ValueError) as exc:
            raise ValueError(self.t("msg_invalid_number")) from exc

    def parse_required_float(self, raw_value):
        """Read one required float field from a text input."""
        try:
            return float(raw_value)
        except (TypeError, ValueError) as exc:
            raise ValueError(self.t("msg_invalid_number")) from exc

    def parse_optional_float(self, raw_value):
        """Read one optional float field and return None for empty input."""
        if raw_value is None or str(raw_value).strip() == "":
            return None
        return self.parse_required_float(raw_value)

    def parse_optional_timestamp(self, raw_value):
        """Validate an optional localized timestamp input and return ISO text."""
        if raw_value is None or raw_value.strip() == "":
            return None
        try:
            cleaned = raw_value.strip()
            if self.current_language == "de":
                return datetime.strptime(cleaned, "%d.%m.%Y %H:%M").isoformat()
            return datetime.strptime(cleaned, "%Y-%m-%d %H:%M").isoformat()
        except ValueError as exc:
            try:
                return datetime.fromisoformat(raw_value.strip()).isoformat()
            except ValueError:
                raise ValueError(self.t("msg_invalid_timestamp")) from exc

    def get_meal_templates(self):
        """Build all meal templates from DB rows into Meal objects."""
        return [self.enrich_meal(meal) for meal in create_meal_instances(self.main_db)]

    def get_food_name(self, food_row):
        """Choose the best available display name from one food DB row."""
        if self.current_language == "de":
            return food_row["name_de"] or food_row["name_en"]
        return food_row["name_en"] or food_row["name_de"]

    def get_food_row_by_id(self, food_id):
        """Read one food DB row once and reuse it across GUI redraws."""
        # The nutrition view can show the same food many times (search, builder,
        # templates, meal logs), so we keep the fetched row in memory here.
        if food_id not in self.food_row_cache:
            self.food_row_cache[food_id] = self.food_db.get_food_by_id(food_id)
        return self.food_row_cache[food_id]

    def get_food_item_display_name(self, food_item: Food):
        """Return one food-item label in the currently selected GUI language."""
        # Food objects keep one stored name, so the GUI re-reads the DB label here
        # to switch cleanly between German and English without changing the model.
        food_row = self.get_food_row_by_id(food_item.id)
        if food_row is None:
            return food_item.name
        return self.get_food_name(food_row)

    def get_meal_display_name(self, meal: Meal):
        """Return a localized meal title without overwriting custom template names."""
        if len(meal.food_items) != 1:
            return meal.name

        food_row = self.get_food_row_by_id(meal.food_items[0].id)
        if food_row is None:
            return meal.name

        # Only auto-localize one-food meals that were created from a plain food name.
        # Custom template names should stay exactly as the user entered them.
        known_food_names = {
            food_row["name_de"] or food_row["name_en"],
            food_row["name_en"] or food_row["name_de"],
        }
        if meal.name not in known_food_names:
            return meal.name
        return self.get_food_name(food_row)

    def enrich_food_item(self, food_item: Food):
        """Hydrate one stored meal item with full nutrient data from the food DB."""
        food_row = self.get_food_row_by_id(food_item.id)
        if food_row is None:
            return food_item
        return create_food_instance_from_food_row(food_row, food_item.amount)

    def enrich_meal(self, meal: Meal):
        """Hydrate a meal template so nutrient summary data is complete in the GUI."""
        return Meal(
            meal.id,
            meal.name,
            [self.enrich_food_item(food_item) for food_item in meal.food_items],
        )  # refactored by ai

    def enrich_meal_log(self, meal_log: MealLog):
        """Create a temporary GUI copy of one meal log with a fully hydrated meal."""
        return MealLog(
            meal_log.id,
            meal_log.user_id,
            self.enrich_meal(meal_log.meal),
            meal_log.amount,
            meal_log.unit_type,
            meal_log.timestamp,
        )  # refactored by ai

    def get_current_weight_log(self):
        """Return the chronologically latest weight log based on its timestamp."""
        if not self.current_user.weight_log_handler.logs:
            return None
        return max(
            self.current_user.weight_log_handler.logs,
            key=lambda log: log.timestamp or "",
        )  # refactored by ai

    def get_license_text(self):
        """Load the project license text once and reuse it for the about dialog."""
        if self.license_text_cache is None:
            license_path = Path(__file__).resolve().parents[1] / "LICENSE.md"
            self.license_text_cache = license_path.read_text(encoding="utf-8").strip()
        return self.license_text_cache

    # ---------------------------
    # Dialog helpers
    # The GUI uses small dialogs for confirmations and edit flows.
    # ---------------------------
    def close_dialog(self, dialog):
        """Close one currently visible dialog."""
        dialog.open = False
        self.page.update()

    def open_confirm_dialog(self, title, content, on_confirm):
        """Show a reusable yes/no confirmation dialog."""
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
        """Show the full license text in a readable scrollable dialog."""
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
        """Edit one activity entry in-place without leaving the activity page."""
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
        """Create or edit one meal log via a small dialog."""
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
        """Display Big Seven and nutrient summary values of one meal log."""
        big_seven_controls = []
        labels = (
            BIG_SEVEN_LABELS_DE if self.current_language == "de" else BIG_SEVEN_LABELS
        )
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
        """Ask for an amount before adding a food to the builder or directly logging it."""
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
            self.t("single_food_form_copy")
            if mode == "consume"
            else self.t("builder_copy")
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

    # ---------------------------
    # DB-backed action handlers
    # These functions connect button clicks to the existing model/database logic.
    # ---------------------------
    def create_user(self, name, birthdate, height, gender, fitness_lvl):
        """Create the first user from the landing page form."""
        user_id = self.main_db.add_user(name, birthdate, height, gender, fitness_lvl)
        self.current_user = User(
            user_id,
            name,
            birthdate,
            height,
            gender,
            fitness_lvl,
            [],
            [],
            [],
            [],
        )
        self.current_view = "dashboard"
        self.show_message(self.t("msg_user_created"))
        self.render()

    def save_profile(self, name, birthdate, height, gender, fitness_lvl):
        """Persist updated biometrical user data."""
        self.current_user.name = name
        self.current_user.update_biometrical_data(
            birthdate=birthdate,
            height_in_cm=height,
            gender=gender,
            fitness_lvl=fitness_lvl,
        )
        self.main_db.update_user(
            self.current_user.user_id,
            self.current_user.name,
            self.current_user.birthdate,
            self.current_user.height_in_cm,
            self.current_user.gender,
            self.current_user.fitness_lvl,
        )
        self.show_message(self.t("msg_profile_saved"))
        self.render()

    def add_weight_log(self, weight, timestamp=None):
        """Add one new weight entry for the current user."""
        new_log = self.current_user.weight_log_handler.create_log(
            None,
            weight,
            self.current_user.height_in_cm,
            timestamp,
        )
        db_id = self.main_db.add_weight_log(
            self.current_user.user_id,
            new_log.weight_in_kg,
            new_log.height_in_cm,
            new_log.timestamp,
        )
        new_log.set_database_id(db_id)
        self.show_message(self.t("msg_weight_saved"))
        self.render()

    def delete_weight_log(self, weight_log_id):
        """Delete one weight entry from DB and handler state."""
        deleted_rows = self.main_db.delete_weight_log(weight_log_id)
        if deleted_rows:
            self.current_user.weight_log_handler.delete_log(weight_log_id)
            self.show_message(self.t("msg_weight_deleted"))
            self.render()

    def add_water_log(self, amount, timestamp=None):
        """Add one water entry and persist it immediately."""
        new_log = self.current_user.water_log_handler.create_log(
            None, amount, timestamp
        )
        db_id = self.main_db.add_water_log(
            self.current_user.user_id,
            new_log.amount_in_ml,
            new_log.timestamp,
        )
        new_log.set_database_id(db_id)
        self.show_message(self.t("msg_water_saved"))
        self.render()

    def delete_water_log(self, water_log_id):
        """Delete one water log entry."""
        deleted_rows = self.main_db.delete_water_log(water_log_id)
        if deleted_rows:
            self.current_user.water_log_handler.delete_log(water_log_id)
            self.show_message(self.t("msg_water_deleted"))
            self.render()

    def add_activity_log(
        self, activity_name, calories_burned, duration, timestamp=None
    ):
        """Add one burned-calorie activity entry."""
        new_log = self.current_user.activity_log_handler.create_log(
            None,
            activity_name,
            calories_burned,
            duration,
            "minutes",
            timestamp,
        )
        db_id = self.main_db.add_activity_log(
            self.current_user.user_id,
            new_log.activity_name,
            new_log.calories_burned,
            new_log.activity_value,
            new_log.unit_type,
            new_log.timestamp,
        )
        new_log.set_database_id(db_id)
        self.show_message(self.t("msg_activity_saved"))
        self.render()

    def delete_activity_log(self, activity_log_id):
        """Delete one activity entry."""
        deleted_rows = self.main_db.delete_activity_log(activity_log_id)
        if deleted_rows:
            self.current_user.activity_log_handler.delete_log(activity_log_id)
            self.show_message(self.t("msg_activity_deleted"))
            self.render()

    def search_foods(self):
        """Search the external food DB and store the result list in GUI state."""
        if not self.food_search_term.strip():
            self.show_message(self.t("msg_search_empty"), error=True)
            return
        self.food_search_results = self.food_db.search_foods(
            self.food_search_term.strip()
        )
        self.render()

    def save_meal_template(self):
        """Create a new meal template or update the currently edited one."""
        if not self.meal_builder_name.strip():
            raise ValueError(self.t("msg_template_name_required"))
        if not self.meal_builder_items:
            raise ValueError(self.t("msg_select_items_first"))

        if self.editing_meal_template_id is None:
            meal_id = self.main_db.add_meal(self.meal_builder_name.strip())
            for food_item in self.meal_builder_items:
                self.main_db.add_meal_food_item(
                    meal_id,
                    food_item.id,
                    food_item.amount,
                    food_item.unit_type,
                )
            self.show_message(self.t("msg_template_saved"))
        else:
            self.main_db.update_meal(
                self.editing_meal_template_id,
                self.meal_builder_name.strip(),
            )
            self.main_db.delete_meal_food_items(self.editing_meal_template_id)
            for food_item in self.meal_builder_items:
                self.main_db.add_meal_food_item(
                    self.editing_meal_template_id,
                    food_item.id,
                    food_item.amount,
                    food_item.unit_type,
                )
            self.show_message(self.t("msg_template_updated"))

        self.reset_meal_builder()
        self.render()

    def delete_meal_template(self, meal_id):
        """Delete one saved meal template."""
        deleted_rows = self.main_db.delete_meal(meal_id)
        if deleted_rows:
            if self.editing_meal_template_id == meal_id:
                self.reset_meal_builder()
            self.show_message(self.t("msg_template_deleted"))
            self.render()

    def delete_meal_log(self, meal_log_id):
        """Delete one meal consumption entry."""
        deleted_rows = self.main_db.delete_meal_log(meal_log_id)
        if deleted_rows:
            self.current_user.meal_log_handler.delete_log(meal_log_id)
            self.show_message(self.t("msg_meal_log_deleted"))
            self.render()

    def delete_current_user(self):
        """Delete the current account and return to the landing page."""
        deleted_rows = self.main_db.delete_user_by_id(self.current_user.user_id)
        if deleted_rows:
            self.current_user = None
            self.reset_meal_builder()
            self.food_search_results = []
            self.food_search_term = ""
            self.current_view = "dashboard"
            self.show_message(self.t("msg_user_deleted"))
            self.render()

    # ---------------------------
    # Reusable UI builders
    # These helpers create the shared desktop shell and smaller UI fragments.
    # ---------------------------
    def build_surface_section(self, title, content, subtitle=None, trailing=None):
        """Wrap one logical area in a consistent desktop section style."""
        header_controls = [
            ft.Column(
                [
                    ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
                    (
                        ft.Text(subtitle, size=12, color=self.surface_muted_color())
                        if subtitle
                        else ft.Container()
                    ),
                ],
                spacing=4,
                tight=True,
                expand=True,
            )
        ]
        if trailing is not None:
            header_controls.append(trailing)

        return ft.Container(
            padding=20,
            border_radius=8,
            bgcolor=self.surface_background_color(),
            border=ft.border.all(1, self.surface_border_color()),
            content=ft.Column(
                [
                    ft.Row(
                        header_controls, alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    content,
                ],
                spacing=14,
            ),
        )

    def build_label_value_row(self, label, value):
        """Render one compact label/value pair."""
        return ft.Row(
            [
                ft.Text(label, color=self.surface_muted_color(), expand=1),
                ft.Text(value, weight=ft.FontWeight.W_500),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def build_metric_chip(self, label, value, accent=BRAND_MINT):
        """Render one compact dashboard metric as a small framed block."""
        return ft.Container(
            padding=12,
            border_radius=8,
            bgcolor=self.surface_background_alt_color(),
            border=ft.border.all(1, self.surface_border_color()),
            content=ft.Column(
                [
                    ft.Text(label, size=12, color=self.surface_muted_color()),
                    ft.Text(value, size=18, weight=ft.FontWeight.BOLD, color=accent),
                ],
                spacing=4,
                tight=True,
            ),
        )

    def build_primary_nav(self):
        """Build the top navigation row in the style of the desktop mockups."""
        buttons = []
        for view_name, label_key, icon in NAV_ITEMS:
            active = self.current_view == view_name
            button = (
                ft.FilledButton(
                    content=self.t(label_key),
                    icon=icon,
                    style=ft.ButtonStyle(
                        bgcolor=BRAND_YELLOW,
                        color=ft.Colors.BLACK,
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=lambda _, target=view_name: self.navigate(target),
                )
                if active
                else ft.OutlinedButton(
                    content=self.t(label_key),
                    icon=icon,
                    style=ft.ButtonStyle(
                        color=self.primary_text_color(),
                        side=ft.BorderSide(1, BRAND_MINT),
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=lambda _, target=view_name: self.navigate(target),
                )
            )
            buttons.append(button)

        return ft.Row(buttons, wrap=True, spacing=10, run_spacing=10)

    def build_header(self):
        """Build the persistent desktop header with branding and active user."""
        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(
                                    f"{self.t('app_title')} v0.5",
                                    size=12,
                                    color=self.surface_muted_color(),
                                ),
                                ft.Text(
                                    self.t("app_subtitle"),
                                    size=30,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                            spacing=2,
                            tight=True,
                        ),
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.SUNNY,
                            icon_color=(
                                BRAND_YELLOW if self.is_dark_mode() else BRAND_MINT
                            ),
                            bgcolor=self.surface_background_alt_color(),
                            tooltip=self.t("toggle_theme"),
                            on_click=self.toggle_theme,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                (
                    self.build_primary_nav()
                    if self.current_user is not None
                    else ft.Container()
                ),
            ],
            spacing=18,
        )

    def build_page_shell(self, content):
        """Assemble the persistent desktop shell around the current page body."""
        return ft.SafeArea(
            expand=True,
            content=ft.Container(
                expand=True,
                padding=24,
                content=ft.Column(
                    [
                        self.build_header(),
                        ft.Container(content=content, expand=True),
                    ],
                    spacing=20,
                ),
                alignment=ft.Alignment.TOP_CENTER,
            ),
        )

    # ---------------------------
    # Landing view
    # This screen is shown until the first user account exists.
    # ---------------------------
    def build_create_user_view(self):
        """Build the account-creation landing page."""
        name_field = ft.TextField(label=self.t("name"), autofocus=True)
        birthdate_field = ft.TextField(
            label=self.t("birthdate"),
            hint_text=self.birthdate_input_hint(),
        )
        height_field = ft.TextField(
            label=self.t("height_cm"),
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        gender_dropdown = ft.Dropdown(
            label=self.t("gender"),
            value="m",
            options=[
                ft.DropdownOption(key="m", text=self.t("gender_m")),
                ft.DropdownOption(key="f", text=self.t("gender_f")),
                ft.DropdownOption(key="d", text=self.t("gender_d")),
            ],
        )
        fitness_dropdown = ft.Dropdown(
            label=self.t("fitness_level"),
            value="beginner",
            options=[
                ft.DropdownOption(key="beginner", text=self.t("fitness_beginner")),
                ft.DropdownOption(
                    key="intermediate", text=self.t("fitness_intermediate")
                ),
                ft.DropdownOption(key="advanced", text=self.t("fitness_advanced")),
            ],
        )

        def submit_user(_):
            """Validate the landing-page form and create the first user."""
            try:
                name = name_field.value.strip()
                birthdate = self.parse_birthdate(birthdate_field.value)
                height = self.parse_required_int(height_field.value)
                if not name:
                    raise ValueError(self.t("name"))
                self.create_user(
                    name,
                    birthdate,
                    height,
                    gender_dropdown.value,
                    fitness_dropdown.value,
                )
            except Exception as exc:
                self.show_message(str(exc), error=True)

        form = self.build_surface_section(
            self.t("create_user"),
            ft.Column(
                [
                    name_field,
                    birthdate_field,
                    height_field,
                    gender_dropdown,
                    fitness_dropdown,
                    ft.FilledButton(
                        self.t("create_user"),
                        icon=ft.Icons.PERSON_ADD,
                        style=ft.ButtonStyle(
                            bgcolor=BRAND_YELLOW,
                            color=ft.Colors.BLACK,
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                        on_click=submit_user,
                    ),
                ],
                spacing=12,
            ),
        )

        content = ft.Row(
            [
                ft.Container(
                    expand=1,
                    content=ft.Column(
                        [
                            ft.Text(
                                self.t("landing_title"),
                                size=36,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                self.t("landing_copy"),
                                size=16,
                                color=self.surface_muted_color(),
                            ),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.only(right=24),
                ),
                ft.Container(width=420, content=form),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        return self.build_page_shell(content)

    # ---------------------------
    # Dashboard
    # This page mirrors the first overview idea of the mockups.
    # ---------------------------
    def build_dashboard_view(self):
        """Build the first overview page with water, calories and quick actions."""
        calorie_status = get_today_calorie_status(self.current_user)
        water_status = get_today_water_status(self.current_user)
        current_weight_log = self.get_current_weight_log()

        hero = ft.Row(
            [
                ft.Container(
                    width=96,
                    height=96,
                    border_radius=8,
                    border=ft.border.all(1, self.surface_border_color()),
                    content=ft.Icon(ft.Icons.MONITOR_HEART_OUTLINED, size=42),
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Column(
                    [
                        ft.Text(
                            self.t("welcome_back", name=self.current_user.name),
                            size=34,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            self.t("dashboard_intro"),
                            size=16,
                            color=self.surface_muted_color(),
                        ),
                    ],
                    spacing=8,
                    expand=True,
                ),
            ],
            spacing=20,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        calorie_card = self.build_surface_section(
            self.t("calorie_balance_today"),
            ft.Row(
                [
                    ft.Column(
                        [
                            self.build_label_value_row(
                                self.t("calories_eaten"),
                                self.format_amount(calorie_status["intake"], "kcal"),
                            ),
                            self.build_label_value_row(
                                self.t("calories_burned_label"),
                                self.format_amount(calorie_status["burned"], "kcal"),
                            ),
                            self.build_label_value_row(
                                self.t("calorie_balance_label"),
                                self.format_amount(calorie_status["net"], "kcal"),
                            ),
                            self.build_label_value_row(
                                self.t("calorie_goal"),
                                self.format_amount(calorie_status["target"], "kcal"),
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
                                    color=BRAND_MINT,
                                    bgcolor=self.surface_border_color(),
                                ),
                                ft.Text(
                                    f"{self.t('remaining_to_goal')}: {self.format_amount(calorie_status['difference'], 'kcal')}",
                                    color=self.surface_muted_color(),
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
                    content=self.build_surface_section(
                        self.t("water_today"),
                        ft.Column(
                            [
                                ft.Text(
                                    self.t(
                                        "water_progress",
                                        intake=water_status["intake"],
                                        target=water_status["target"],
                                    ),
                                    size=20,
                                ),
                                ft.ProgressBar(
                                    value=min(1, (water_status["progress"] or 0) / 100),
                                    color=BRAND_MINT,
                                    bgcolor=self.surface_border_color(),
                                ),
                                ft.Text(
                                    self.t(
                                        "water_to_go",
                                        difference=water_status["difference"],
                                    ),
                                    color=self.surface_muted_color(),
                                ),
                            ],
                            spacing=12,
                        ),
                    ),
                ),
                ft.Container(
                    col={"md": 6},
                    content=self.build_surface_section(
                        self.t("weight_bmi"),
                        ft.Column(
                            [
                                self.build_label_value_row(
                                    self.t("current_weight"),
                                    (
                                        self.format_amount(
                                            current_weight_log.weight_in_kg, "kg"
                                        )
                                        if current_weight_log is not None
                                        else self.t("no_weight_logged")
                                    ),
                                ),
                                self.build_label_value_row(
                                    self.t("bmi"),
                                    (
                                        self.format_amount(current_weight_log.bmi)
                                        if current_weight_log is not None
                                        and current_weight_log.bmi is not None
                                        else self.t("bmi_not_available")
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

        quick_actions = self.build_surface_section(
            self.t("quick_actions"),
            ft.ResponsiveRow(
                [
                    ft.Container(
                        col={"md": 3},
                        content=ft.FilledButton(
                            self.t("add_water"),
                            icon=ft.Icons.WATER_DROP,
                            style=ft.ButtonStyle(
                                bgcolor=BRAND_MINT,
                                color=ft.Colors.WHITE,
                            ),
                            expand=True,
                            on_click=lambda _: self.navigate("water"),
                        ),
                    ),
                    ft.Container(
                        col={"md": 3},
                        content=ft.FilledButton(
                            self.t("log_meal"),
                            icon=ft.Icons.RESTAURANT,
                            style=ft.ButtonStyle(
                                bgcolor=BRAND_MINT,
                                color=ft.Colors.WHITE,
                            ),
                            expand=True,
                            on_click=lambda _: self.navigate("nutrition"),
                        ),
                    ),
                    ft.Container(
                        col={"md": 3},
                        content=ft.FilledButton(
                            self.t("add_activity"),
                            icon=ft.Icons.DIRECTIONS_RUN,
                            style=ft.ButtonStyle(
                                bgcolor=BRAND_MINT,
                                color=ft.Colors.WHITE,
                            ),
                            expand=True,
                            on_click=lambda _: self.navigate("activity"),
                        ),
                    ),
                    ft.Container(
                        col={"md": 3},
                        content=ft.FilledButton(
                            self.t("go_to_profile"),
                            icon=ft.Icons.PERSON,
                            style=ft.ButtonStyle(
                                bgcolor=BRAND_MINT,
                                color=ft.Colors.WHITE,
                            ),
                            expand=True,
                            on_click=lambda _: self.navigate("profile"),
                        ),
                    ),
                ],
                spacing=12,
                run_spacing=12,
            ),
        )

        return ft.Column([hero, calorie_card, cards_row, quick_actions], spacing=20)

    # ---------------------------
    # Water page
    # This page covers the water-related V0.1 tracking flow.
    # ---------------------------
    def build_water_view(self):
        """Build the water page with status, add-form and entry list."""
        self.refresh_current_user_logs()
        water_status = get_today_water_status(self.current_user)

        amount_field = ft.TextField(
            label=self.t("amount_ml"),
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
        )
        timestamp_field = ft.TextField(
            label=self.t("optional_timestamp"),
            helper=self.t("use_now_when_empty"),
            hint_text=self.timestamp_input_hint(),
            expand=True,
        )

        def submit_water(_):
            """Create one water log from the inline form."""
            try:
                amount = self.parse_required_int(amount_field.value)
                timestamp = self.parse_optional_timestamp(timestamp_field.value)
                self.add_water_log(amount, timestamp)
            except Exception as exc:
                self.show_message(str(exc), error=True)

        status_section = self.build_surface_section(
            self.t("water_status"),
            ft.Column(
                [
                    ft.Text(
                        self.t(
                            "water_progress",
                            intake=water_status["intake"],
                            target=water_status["target"],
                        ),
                        size=22,
                    ),
                    ft.ProgressBar(
                        value=min(1, (water_status["progress"] or 0) / 100),
                        color=BRAND_MINT,
                        bgcolor=self.surface_border_color(),
                    ),
                    ft.Text(
                        self.t("water_to_go", difference=water_status["difference"]),
                        color=self.surface_muted_color(),
                    ),
                ],
                spacing=12,
            ),
        )

        add_section = self.build_surface_section(
            self.t("add_water"),
            ft.Row(
                [
                    amount_field,
                    timestamp_field,
                    ft.FilledButton(
                        self.t("save"),
                        icon=ft.Icons.SAVE,
                        on_click=submit_water,
                    ),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.END,
            ),
        )

        water_rows = []
        for water_log in self.sort_logs_desc(self.current_user.water_log_handler.logs):
            water_rows.append(
                ft.Container(
                    padding=12,
                    border_radius=8,
                    bgcolor=self.surface_background_alt_color(),
                    border=ft.border.all(1, self.surface_border_color()),
                    content=ft.Row(
                        [
                            ft.Text(
                                self.format_amount(water_log.amount_in_ml, "ml"),
                                width=120,
                            ),
                            ft.Text(
                                self.format_timestamp(water_log.timestamp),
                                expand=True,
                                color=self.surface_muted_color(),
                            ),
                            ft.IconButton(
                                ft.Icons.DELETE_OUTLINE,
                                icon_color=BRAND_RED,
                                on_click=lambda _, log_id=water_log.id: self.open_confirm_dialog(
                                    self.t("msg_confirm_delete_entry"),
                                    self.t("water_today"),
                                    lambda dialog, target_id=log_id: (
                                        self.close_dialog(dialog),
                                        self.delete_water_log(target_id),
                                    ),
                                ),
                            ),
                        ]
                    ),
                )
            )

        entries_section = self.build_surface_section(
            self.t("last_entries"),
            ft.Column(
                water_rows
                or [ft.Text(self.t("no_water_logs"), color=self.surface_muted_color())],
                spacing=10,
            ),
        )

        return ft.Column([status_section, add_section, entries_section], spacing=20)

    # ---------------------------
    # Activity page
    # This page covers add/show/update/delete for burned-calorie entries.
    # ---------------------------
    def build_activity_view(self):
        """Build the activity page with add form and editable entries."""
        self.refresh_current_user_logs()

        name_field = ft.TextField(label=self.t("activity_name"), expand=True)
        calories_field = ft.TextField(
            label=self.t("calories_burned"),
            keyboard_type=ft.KeyboardType.NUMBER,
            width=180,
        )
        duration_field = ft.TextField(
            label=self.t("duration_minutes"),
            keyboard_type=ft.KeyboardType.NUMBER,
            width=180,
        )
        timestamp_field = ft.TextField(
            label=self.t("optional_timestamp"),
            helper=self.t("use_now_when_empty"),
            hint_text=self.timestamp_input_hint(),
            expand=True,
        )

        def submit_activity(_):
            """Create one activity entry from the inline desktop form."""
            try:
                activity_name = name_field.value.strip()
                calories = self.parse_required_float(calories_field.value)
                duration = self.parse_optional_float(duration_field.value)
                timestamp = self.parse_optional_timestamp(timestamp_field.value)
                self.add_activity_log(activity_name, calories, duration, timestamp)
            except Exception as exc:
                self.show_message(str(exc), error=True)

        add_section = self.build_surface_section(
            self.t("add_activity"),
            ft.Column(
                [
                    ft.Row([name_field, calories_field, duration_field], spacing=12),
                    ft.Row(
                        [
                            timestamp_field,
                            ft.FilledButton(
                                self.t("save"),
                                icon=ft.Icons.SAVE,
                                on_click=submit_activity,
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                    ),
                ],
                spacing=12,
            ),
            subtitle=self.t("activity_copy"),
        )

        activity_rows = []
        for activity_log in self.sort_logs_desc(
            self.current_user.activity_log_handler.logs
        ):
            activity_rows.append(
                ft.Container(
                    padding=12,
                    border_radius=8,
                    bgcolor=self.surface_background_alt_color(),
                    border=ft.border.all(1, self.surface_border_color()),
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        activity_log.activity_name,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        f"{self.format_amount(activity_log.calories_burned, 'kcal')} | "
                                        f"{self.format_amount(activity_log.activity_value, 'minutes')}",
                                        color=self.surface_muted_color(),
                                    ),
                                ],
                                spacing=4,
                                expand=True,
                            ),
                            ft.Text(
                                self.format_timestamp(activity_log.timestamp),
                                color=self.surface_muted_color(),
                                width=170,
                            ),
                            ft.IconButton(
                                ft.Icons.EDIT_OUTLINED,
                                icon_color=BRAND_MINT,
                                on_click=lambda _, log=activity_log: self.open_activity_edit_dialog(
                                    log
                                ),
                            ),
                            ft.IconButton(
                                ft.Icons.DELETE_OUTLINE,
                                icon_color=BRAND_RED,
                                on_click=lambda _, log_id=activity_log.id: self.open_confirm_dialog(
                                    self.t("msg_confirm_delete_entry"),
                                    activity_log.activity_name,
                                    lambda dialog, target_id=log_id: (
                                        self.close_dialog(dialog),
                                        self.delete_activity_log(target_id),
                                    ),
                                ),
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                )
            )

        entries_section = self.build_surface_section(
            self.t("activity_logs"),
            ft.Column(
                activity_rows
                or [
                    ft.Text(
                        self.t("no_activity_logs"), color=self.surface_muted_color()
                    )
                ],
                spacing=10,
            ),
        )

        return ft.Column([add_section, entries_section], spacing=20)

    # ---------------------------
    # Nutrition page
    # This page brings together search, meal templates and meal logs.
    # ---------------------------
    def build_nutrition_view(self):
        """Build the nutrition page with the full meal-management workflow."""
        self.refresh_current_user_logs()
        calorie_status = get_today_calorie_status(self.current_user)

        search_field = ft.TextField(
            label=self.t("search_term"),
            value=self.food_search_term,
            expand=True,
            on_change=lambda e: setattr(self, "food_search_term", e.control.value),
        )

        calorie_section = self.build_surface_section(
            self.t("calorie_status_today"),
            ft.Row(
                [
                    self.build_metric_chip(
                        self.t("calories_eaten"),
                        self.format_amount(calorie_status["intake"], "kcal"),
                        accent=BRAND_MINT,
                    ),
                    self.build_metric_chip(
                        self.t("calories_burned_label"),
                        self.format_amount(calorie_status["burned"], "kcal"),
                        accent=BRAND_YELLOW,
                    ),
                    self.build_metric_chip(
                        self.t("calorie_balance_label"),
                        self.format_amount(calorie_status["net"], "kcal"),
                        accent=self.primary_text_color(),
                    ),
                    self.build_metric_chip(
                        self.t("calorie_goal"),
                        self.format_amount(calorie_status["target"], "kcal"),
                        accent=BRAND_MINT,
                    ),
                    self.build_metric_chip(
                        self.t("remaining_to_goal"),
                        self.format_amount(calorie_status["difference"], "kcal"),
                        accent=BRAND_YELLOW,
                    ),
                ],
                wrap=True,
                spacing=12,
            ),
        )

        search_rows = []
        for food_row in self.food_search_results:
            search_rows.append(
                ft.Container(
                    padding=12,
                    border_radius=8,
                    bgcolor=self.surface_background_alt_color(),
                    border=ft.border.all(1, self.surface_border_color()),
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        self.get_food_name(food_row),
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        f"{self.format_amount(food_row['kcal'], 'kcal')} / 100 {food_row['unit_type']}",
                                        color=self.surface_muted_color(),
                                    ),
                                ],
                                spacing=4,
                                expand=True,
                            ),
                            ft.FilledButton(
                                self.t("consume"),
                                on_click=lambda _, row=food_row: self.open_food_amount_dialog(
                                    row, "consume"
                                ),
                            ),
                            ft.OutlinedButton(
                                self.t("add_to_template"),
                                on_click=lambda _, row=food_row: self.open_food_amount_dialog(
                                    row, "template"
                                ),
                            ),
                        ],
                        spacing=12,
                    ),
                )
            )

        search_section = self.build_surface_section(
            self.t("food_search"),
            ft.Column(
                [
                    ft.Text(
                        self.t("food_search_copy"), color=self.surface_muted_color()
                    ),
                    ft.Row(
                        [
                            search_field,
                            ft.FilledButton(
                                self.t("search"),
                                icon=ft.Icons.SEARCH,
                                on_click=lambda _: self.search_foods(),
                            ),
                        ],
                        spacing=12,
                    ),
                    ft.Column(
                        search_rows
                        or [
                            ft.Text(
                                self.t("no_food_results"),
                                color=self.surface_muted_color(),
                            )
                        ],
                        spacing=10,
                    ),
                ],
                spacing=12,
            ),
        )

        builder_name_field = ft.TextField(
            label=self.t("template_name"),
            value=self.meal_builder_name,
            on_change=lambda e: setattr(self, "meal_builder_name", e.control.value),
        )

        builder_rows = []
        for index, food_item in enumerate(self.meal_builder_items):
            builder_rows.append(
                ft.Container(
                    padding=12,
                    border_radius=8,
                    bgcolor=self.surface_background_alt_color(),
                    border=ft.border.all(1, self.surface_border_color()),
                    content=ft.Row(
                        [
                            ft.Text(
                                self.get_food_item_display_name(food_item), expand=True
                            ),
                            ft.Text(
                                self.format_amount(
                                    food_item.amount, food_item.unit_type
                                ),
                                width=110,
                            ),
                            ft.IconButton(
                                ft.Icons.DELETE_OUTLINE,
                                icon_color=BRAND_RED,
                                on_click=lambda _, item_index=index: (
                                    self.meal_builder_items.pop(item_index),
                                    self.render(),
                                ),
                            ),
                        ]
                    ),
                )
            )

        builder_section = self.build_surface_section(
            self.t("meal_template_builder"),
            ft.Column(
                [
                    ft.Text(self.t("builder_copy"), color=self.surface_muted_color()),
                    builder_name_field,
                    ft.Text(self.t("selected_items"), weight=ft.FontWeight.BOLD),
                    ft.Column(
                        builder_rows
                        or [
                            ft.Text(
                                self.t("builder_empty"),
                                color=self.surface_muted_color(),
                            )
                        ],
                        spacing=10,
                    ),
                    ft.Row(
                        [
                            ft.FilledButton(
                                self.t(
                                    "update_template"
                                    if self.editing_meal_template_id is not None
                                    else "save_template"
                                ),
                                icon=ft.Icons.SAVE,
                                on_click=lambda _: self.handle_save_meal_template(),
                            ),
                            ft.OutlinedButton(
                                self.t("reset_builder"),
                                icon=ft.Icons.RESTART_ALT,
                                on_click=lambda _: self.handle_reset_builder(),
                            ),
                        ],
                        spacing=12,
                    ),
                ],
                spacing=12,
            ),
        )

        template_rows = []
        for meal in self.get_meal_templates():
            template_rows.append(
                ft.Container(
                    padding=12,
                    border_radius=8,
                    bgcolor=self.surface_background_alt_color(),
                    border=ft.border.all(1, self.surface_border_color()),
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(
                                        self.get_meal_display_name(meal),
                                        weight=ft.FontWeight.BOLD,
                                        expand=True,
                                    ),
                                    ft.Text(
                                        self.format_amount(meal.calories, "kcal"),
                                        color=self.surface_muted_color(),
                                    ),
                                ]
                            ),
                            ft.Text(
                                ", ".join(
                                    [
                                        f"{self.get_food_item_display_name(item)} "
                                        f"({self.format_amount(item.amount, item.unit_type)})"
                                        for item in meal.food_items
                                    ]
                                ),
                                color=self.surface_muted_color(),
                            ),
                            ft.Row(
                                [
                                    ft.FilledButton(
                                        self.t("log_meal"),
                                        icon=ft.Icons.ADD_TASK,
                                        on_click=lambda _, selected_meal=meal: self.open_meal_log_dialog(
                                            meal=selected_meal
                                        ),
                                    ),
                                    ft.OutlinedButton(
                                        self.t("edit_template"),
                                        icon=ft.Icons.EDIT,
                                        on_click=lambda _, selected_meal=meal: (
                                            self.start_meal_template_edit(selected_meal)
                                        ),
                                    ),
                                    ft.OutlinedButton(
                                        self.t("delete"),
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        style=ft.ButtonStyle(color=BRAND_RED),
                                        on_click=lambda _, selected_meal=meal: self.open_confirm_dialog(
                                            self.t("msg_confirm_delete_template"),
                                            self.get_meal_display_name(selected_meal),
                                            lambda dialog, meal_id=selected_meal.id: (
                                                self.close_dialog(dialog),
                                                self.delete_meal_template(meal_id),
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

        templates_section = self.build_surface_section(
            self.t("meal_templates"),
            ft.Column(
                template_rows
                or [
                    ft.Text(
                        self.t("no_meal_templates"), color=self.surface_muted_color()
                    )
                ],
                spacing=10,
            ),
        )

        meal_log_rows = []
        for meal_log in self.sort_logs_desc(self.current_user.meal_log_handler.logs):
            enriched_log = self.enrich_meal_log(meal_log)
            meal_log_rows.append(
                ft.Container(
                    padding=12,
                    border_radius=8,
                    bgcolor=self.surface_background_alt_color(),
                    border=ft.border.all(1, self.surface_border_color()),
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Column(
                                        [
                                            ft.Text(
                                                self.get_meal_display_name(
                                                    enriched_log.meal
                                                ),
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            ft.Text(
                                                f"{self.format_amount(enriched_log.amount, enriched_log.unit_type)} | "
                                                f"{self.format_amount(enriched_log.calories, 'kcal')}",
                                                color=self.surface_muted_color(),
                                            ),
                                        ],
                                        spacing=4,
                                        expand=True,
                                    ),
                                    ft.Text(
                                        self.format_timestamp(meal_log.timestamp),
                                        color=self.surface_muted_color(),
                                    ),
                                ]
                            ),
                            ft.Row(
                                [
                                    ft.FilledButton(
                                        self.t("show_details"),
                                        icon=ft.Icons.ARTICLE_OUTLINED,
                                        on_click=lambda _, log=enriched_log: self.open_meal_log_details_dialog(
                                            log
                                        ),
                                    ),
                                    ft.OutlinedButton(
                                        self.t("edit_log"),
                                        icon=ft.Icons.EDIT,
                                        on_click=lambda _, log=meal_log: self.open_meal_log_dialog(
                                            existing_log=log
                                        ),
                                    ),
                                    ft.OutlinedButton(
                                        self.t("delete"),
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        style=ft.ButtonStyle(color=BRAND_RED),
                                        on_click=lambda _, log_id=meal_log.id: self.open_confirm_dialog(
                                            self.t("msg_confirm_delete_entry"),
                                            self.get_meal_display_name(
                                                enriched_log.meal
                                            ),
                                            lambda dialog, target_id=log_id: (
                                                self.close_dialog(dialog),
                                                self.delete_meal_log(target_id),
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

        meal_logs_section = self.build_surface_section(
            self.t("meal_logs"),
            ft.Column(
                meal_log_rows
                or [ft.Text(self.t("no_meal_logs"), color=self.surface_muted_color())],
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

    def handle_save_meal_template(self):
        """Wrap meal-template saving so UI errors end up in the footer."""
        try:
            self.save_meal_template()
        except Exception as exc:
            self.show_message(str(exc), error=True)

    def handle_reset_builder(self):
        """Reset the meal-template builder and show a small confirmation."""
        self.reset_meal_builder()
        self.show_message(self.t("msg_builder_reset"))
        self.render()

    # ---------------------------
    # Profile page
    # This page holds biometrical data, weight logs, settings and account actions.
    # ---------------------------
    def build_profile_view(self):
        """Build the profile page with inline forms and calculated values."""
        self.refresh_current_user_logs()
        calorie_status = get_today_calorie_status(self.current_user)
        current_weight_log = self.get_current_weight_log()

        name_field = ft.TextField(label=self.t("name"), value=self.current_user.name)
        birthdate_field = ft.TextField(
            label=self.t("birthdate"),
            value=self.format_birthdate(self.current_user.birthdate),
            hint_text=self.birthdate_input_hint(),
        )
        height_field = ft.TextField(
            label=self.t("height_cm"),
            value=str(self.current_user.height_in_cm),
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        gender_dropdown = ft.Dropdown(
            label=self.t("gender"),
            value=self.current_user.gender,
            options=[
                ft.DropdownOption(key="m", text=self.t("gender_m")),
                ft.DropdownOption(key="f", text=self.t("gender_f")),
                ft.DropdownOption(key="d", text=self.t("gender_d")),
            ],
        )
        fitness_dropdown = ft.Dropdown(
            label=self.t("fitness_level"),
            value=self.current_user.fitness_lvl,
            options=[
                ft.DropdownOption(key="beginner", text=self.t("fitness_beginner")),
                ft.DropdownOption(
                    key="intermediate", text=self.t("fitness_intermediate")
                ),
                ft.DropdownOption(key="advanced", text=self.t("fitness_advanced")),
            ],
        )

        def submit_profile(_):
            """Validate and persist personal data edits."""
            try:
                self.save_profile(
                    name_field.value.strip(),
                    self.parse_birthdate(birthdate_field.value),
                    self.parse_required_int(height_field.value),
                    gender_dropdown.value,
                    fitness_dropdown.value,
                )
            except Exception as exc:
                self.show_message(str(exc), error=True)

        personal_section = self.build_surface_section(
            self.t("personal_data"),
            ft.Column(
                [
                    ft.Row([name_field, birthdate_field], spacing=12),
                    ft.Row(
                        [height_field, gender_dropdown, fitness_dropdown], spacing=12
                    ),
                    ft.Row(
                        [
                            ft.Container(expand=True),
                            ft.FilledButton(
                                self.t("save"),
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
            label=self.t("weight_kg"),
            keyboard_type=ft.KeyboardType.NUMBER,
            width=200,
        )
        weight_timestamp_field = ft.TextField(
            label=self.t("optional_timestamp"),
            helper=self.t("use_now_when_empty"),
            hint_text=self.timestamp_input_hint(),
            expand=True,
        )

        def submit_weight(_):
            """Create one new weight log from the profile page."""
            try:
                weight = self.parse_required_float(weight_field.value)
                timestamp = self.parse_optional_timestamp(weight_timestamp_field.value)
                self.add_weight_log(weight, timestamp)
            except Exception as exc:
                self.show_message(str(exc), error=True)

        weight_rows = []
        for weight_log in self.sort_logs_desc(
            self.current_user.weight_log_handler.logs
        ):
            weight_rows.append(
                ft.Container(
                    padding=12,
                    border_radius=8,
                    bgcolor=self.surface_background_alt_color(),
                    border=ft.border.all(1, self.surface_border_color()),
                    content=ft.Row(
                        [
                            ft.Text(
                                self.format_amount(weight_log.weight_in_kg, "kg"),
                                width=110,
                            ),
                            ft.Text(
                                self.format_amount(weight_log.bmi),
                                width=100,
                                color=self.surface_muted_color(),
                            ),
                            ft.Text(
                                self.format_timestamp(weight_log.timestamp),
                                expand=True,
                                color=self.surface_muted_color(),
                            ),
                            ft.IconButton(
                                ft.Icons.DELETE_OUTLINE,
                                icon_color=BRAND_RED,
                                on_click=lambda _, log_id=weight_log.id: self.open_confirm_dialog(
                                    self.t("msg_confirm_delete_entry"),
                                    self.t("weight_bmi"),
                                    lambda dialog, target_id=log_id: (
                                        self.close_dialog(dialog),
                                        self.delete_weight_log(target_id),
                                    ),
                                ),
                            ),
                        ]
                    ),
                )
            )

        body_section = self.build_surface_section(
            self.t("body_statistics"),
            ft.Column(
                [
                    self.build_label_value_row(
                        self.t("latest_weight"),
                        (
                            self.format_amount(current_weight_log.weight_in_kg, "kg")
                            if current_weight_log is not None
                            else self.t("no_weight_logged")
                        ),
                    ),
                    self.build_label_value_row(
                        self.t("bmi"),
                        (
                            self.format_amount(current_weight_log.bmi)
                            if current_weight_log is not None
                            and current_weight_log.bmi is not None
                            else self.t("bmi_not_available")
                        ),
                    ),
                    ft.Row(
                        [
                            weight_field,
                            weight_timestamp_field,
                            ft.FilledButton(
                                self.t("add_weight_log"),
                                icon=ft.Icons.MONITOR_WEIGHT_OUTLINED,
                                on_click=submit_weight,
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                    ),
                    ft.Text(self.t("weight_logs"), weight=ft.FontWeight.BOLD),
                    ft.Column(
                        weight_rows
                        or [
                            ft.Text(
                                self.t("no_weight_logs"),
                                color=self.surface_muted_color(),
                            )
                        ],
                        spacing=10,
                    ),
                ],
                spacing=12,
            ),
        )

        calculated_section = self.build_surface_section(
            self.t("calculated_values"),
            ft.Column(
                [
                    self.build_label_value_row(
                        self.t("daily_calorie_target"),
                        self.format_amount(calorie_status["target"], "kcal"),
                    ),
                    self.build_label_value_row(
                        self.t("daily_water_target"),
                        self.format_amount(self.current_user.daily_water_target, "ml"),
                    ),
                    self.build_label_value_row(
                        self.t("bmi"),
                        (
                            self.format_amount(current_weight_log.bmi)
                            if current_weight_log is not None
                            and current_weight_log.bmi is not None
                            else self.t("bmi_not_available")
                        ),
                    ),
                ],
                spacing=10,
            ),
        )

        language_dropdown = ft.Dropdown(
            label=self.t("language"),
            value=self.current_language,
            options=[
                ft.DropdownOption(key="en", text=self.t("language_en")),
                ft.DropdownOption(key="de", text=self.t("language_de")),
            ],
            on_select=lambda e: self.change_language(e.control.value),
            width=220,
        )

        settings_section = self.build_surface_section(
            self.t("application_settings"),
            ft.Column([language_dropdown], spacing=12),
        )

        account_section = self.build_surface_section(
            self.t("delete_account"),
            ft.Column(
                [
                    ft.Text(
                        self.t("delete_account_copy"), color=self.surface_muted_color()
                    ),
                    ft.Row(
                        [
                            ft.FilledButton(
                                self.t("delete_account"),
                                icon=ft.Icons.DELETE_FOREVER_OUTLINED,
                                style=ft.ButtonStyle(bgcolor=BRAND_RED),
                                on_click=lambda _: self.open_confirm_dialog(
                                    self.t("delete_account_confirm_title"),
                                    self.t(
                                        "delete_account_confirm_copy",
                                        name=self.current_user.name,
                                    ),
                                    lambda dialog: (
                                        self.close_dialog(dialog),
                                        self.delete_current_user(),
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

    # ---------------------------
    # About page
    # This keeps one simple place for app context and status information.
    # ---------------------------
    def build_about_view(self):
        """Build a lightweight about page connected to the live app state."""
        feature_section = self.build_surface_section(
            self.t("feature_overview"),
            ft.Text(self.t("feature_overview_copy"), color=self.surface_muted_color()),
        )

        about_section = self.build_surface_section(
            self.t("about_title"),
            ft.Column(
                [
                    ft.Text(self.t("about_copy"), color=self.surface_muted_color()),
                    self.build_label_value_row(
                        self.t("database_status"),
                        self.t("database_ready"),
                    ),
                    self.build_label_value_row(
                        self.t("developers_label"),
                        self.t("developers_value"),
                    ),
                ],
                spacing=10,
            ),
        )

        license_section = self.build_surface_section(
            self.t("license_title"),
            ft.Column(
                [
                    ft.Text(
                        self.t("license_copy"), color=self.surface_muted_color()
                    ),
                    self.build_label_value_row(
                        self.t("license_name_label"),
                        self.t("license_name_value"),
                    ),
                    self.build_label_value_row(
                        self.t("license_spdx_label"),
                        "GPL-3.0-or-later",
                    ),
                    self.build_label_value_row(
                        self.t("license_copyright_label"),
                        self.t("license_copyright_value"),
                    ),
                    self.build_label_value_row(
                        self.t("license_file_label"),
                        "LICENSE.md",
                    ),
                    ft.FilledButton(
                        self.t("show_full_license"),
                        icon=ft.Icons.GAVEL_OUTLINED,
                        on_click=self.open_license_dialog,
                    ),
                ],
                spacing=10,
            ),
        )

        return ft.Column(
            [about_section, feature_section, license_section], spacing=20
        )

    # ---------------------------
    # Render logic
    # This part chooses the active page body and redraws the full desktop shell.
    # ---------------------------
    def build_current_view(self):
        """Choose the currently active page body."""
        if self.current_user is None:
            return self.build_create_user_view()
        if self.current_view == "nutrition":
            return self.build_page_shell(self.build_nutrition_view())
        if self.current_view == "water":
            return self.build_page_shell(self.build_water_view())
        if self.current_view == "activity":
            return self.build_page_shell(self.build_activity_view())
        if self.current_view == "profile":
            return self.build_page_shell(self.build_profile_view())
        if self.current_view == "about":
            return self.build_page_shell(self.build_about_view())
        return self.build_page_shell(self.build_dashboard_view())

    def render(self):
        """Redraw the whole page from current state."""
        self.page.bgcolor = self.page_background_color()
        self.page.clean()
        self.page.add(self.build_current_view())
        self.page.update()

    def run(self):
        """Start the GUI by rendering the current state once."""
        self.render()


def main(page: ft.Page):
    """Start the SEDA desktop GUI."""
    SedaGuiApp(page).run()


if __name__ == "__main__":
    ft.app(target=main)
