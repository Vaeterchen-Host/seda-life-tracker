# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Graphical user interface for SEDA."""

# pylint: disable=all

import sys
from datetime import datetime
from pathlib import Path

import flet as ft

# Search path for model imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.class_user import User
from model.classes_food import Food, Meal
from model.classes_log import MealLog
from application.builders import (
    create_food_instance_from_food_row,
    create_meal_instances,
    create_user_instance_from_db,
)
from application.user_service import (
    refresh_user_logs_from_db,
)
from config import ASSETS_DIR
from model.database import Database, FoodDatabase
from ui.gui_components import PageShell
from ui.gui_theme import (
    SEDA_MINT,
    SEDA_RED,
    PAGE_BACKGROUND,
    SURFACE_BACKGROUND,
    SURFACE_BACKGROUND_ALT,
    SURFACE_BORDER,
    SURFACE_MUTED,
)
from ui.pages import (
    build_about_view,
    build_activity_view,
    build_create_user_view,
    build_dashboard_view,
    build_nutrition_view,
    build_profile_view,
    build_water_view,
)
from ui.translations import get_translation


class SedaGuiApp:
    """Desktop-first Flet GUI orchestrator for SEDA."""

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
        self.page.on_resize = self.handle_page_resize
        self.page.window.min_width = 1180
        self.page.window.min_height = 860

    def handle_page_resize(self, _):
        """Redraw the shell after page resizes so width limits stay accurate. AI-generated."""
        self.render()

    def t(self, key, **kwargs):
        """Return a translated GUI string for the current language."""
        return get_translation(self.current_language, key, **kwargs)

    def is_dark_mode(self):
        """Return whether the current page theme is dark."""
        return self.page.theme_mode in (ft.ThemeMode.DARK, "dark")

    def toggle_theme(self, _=None):
        """Switch between dark and light mode and redraw the desktop shell. Partly AI-generated."""
        self.page.theme_mode = (
            ft.ThemeMode.LIGHT if self.is_dark_mode() else ft.ThemeMode.DARK
        )
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
                bgcolor=SEDA_RED if error else SEDA_MINT,
            )
        )
        self.page.update()
        print(message)  # for debugging

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
        if suffix == "portion":
            suffix = self.t("portion")
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
        return [
            self.enrich_meal(meal)
            for meal in create_meal_instances(
                self.main_db,
                self.current_user.user_id,
                templates_only=True,
            )
        ]

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
        """Hydrate a meal template so nutrient summary data is complete in the GUI. Partly AI-generated."""
        return Meal(
            meal.id,
            meal.name,
            [self.enrich_food_item(food_item) for food_item in meal.food_items],
        )

    def enrich_meal_log(self, meal_log: MealLog):
        """Create a temporary GUI copy of one meal log with a fully hydrated meal. Partly AI-generated."""
        return MealLog(
            meal_log.id,
            meal_log.user_id,
            self.enrich_meal(meal_log.meal),
            meal_log.amount,
            meal_log.unit_type,
            meal_log.timestamp,
        )

    def get_current_weight_log(self):
        """Return the chronologically latest weight log based on its timestamp. Partly AI-generated."""
        if not self.current_user.weight_log_handler.logs:
            return None
        return max(
            self.current_user.weight_log_handler.logs,
            key=lambda log: log.timestamp or "",
        )

    def get_license_text(self):
        """Load the project license text once and reuse it for the about dialog."""
        if self.license_text_cache is None:
            license_path = Path(__file__).resolve().parents[1] / "LICENSE.md"
            self.license_text_cache = license_path.read_text(encoding="utf-8").strip()
        return self.license_text_cache

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

    def add_water_log(self, amount, timestamp=None, source_type="manual"):
        """Add one water entry and persist it immediately."""
        new_log = self.current_user.water_log_handler.create_log(
            None, amount, timestamp, source_type
        )
        db_id = self.main_db.add_water_log(
            self.current_user.user_id,
            new_log.amount_in_ml,
            new_log.timestamp,
            new_log.source_type,
        )
        new_log.set_database_id(db_id)
        if source_type == "manual":
            self.show_message(self.t("msg_water_saved"))
            self.render()
        return new_log

    def add_food_water_log_from_meal_log(self, meal_log):
        """Persist one derived water log from a meal log when food contains water. AI-generated."""
        water_amount = meal_log.nutrient_summary.water
        if water_amount is None:
            return None
        water_amount_in_ml = int(round(water_amount))
        if water_amount_in_ml <= 0:
            return None
        return self.add_water_log(
            water_amount_in_ml,
            meal_log.timestamp,
            source_type="food",
        )

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
            meal_id = self.main_db.add_meal(
                self.meal_builder_name.strip(),
                self.current_user.user_id,
            )
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
                self.current_user.user_id,
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
        deleted_rows = self.main_db.delete_meal(
            meal_id,
            self.current_user.user_id,
        )
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
    # Render logic
    # This part chooses the active page body and redraws the full desktop shell.
    # ---------------------------
    def build_current_view(self):
        """Choose the currently active page body."""
        if self.current_user is None:
            return PageShell(self, build_create_user_view(self))

        page_builders = {
            "nutrition": build_nutrition_view,
            "water": build_water_view,
            "activity": build_activity_view,
            "profile": build_profile_view,
            "about": build_about_view,
        }
        active_builder = page_builders.get(self.current_view, build_dashboard_view)
        return PageShell(self, active_builder(self))

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


def run_gui_app(view=None):
    """Start the SEDA GUI with the configured assets directory. AI-generated."""
    ft.app(target=main, assets_dir=str(ASSETS_DIR), view=view)


if __name__ == "__main__":
    run_gui_app(view=ft.AppView.WEB_BROWSER)
