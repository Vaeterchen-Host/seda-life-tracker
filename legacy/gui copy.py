# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Graphical user interface for SEDA."""

# pylint: disable=all

import sys
from pathlib import Path

import flet as ft

# Search path for model imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.class_user import User
from application.builders import (
    create_user_instance_from_db,
)
from application.status_service import (
    get_today_calorie_status,
    get_today_water_status,
)
from application.user_service import (
    refresh_user_logs_from_db,
)
from model.database import Database


class SedaGuiApp:
    """Small GUI controller."""

    # ---------------------------
    # Setup
    # This part stores page state and prepares the first screen.
    # ---------------------------
    def __init__(self, page: ft.Page):
        """Store shared GUI state and configure the page."""
        self.page = page
        self.main_db = Database()
        self.current_user = None
        self.current_view = "dashboard"
        self.configure_page()
        self.load_current_user()

    def configure_page(self):
        """Apply the basic page settings."""
        self.page.title = "seda - your life tracker"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 16
        self.page.window.min_width = 380
        self.page.window.min_height = 720
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # ---------------------------
    # Small state helpers
    # These functions handle user loading, messages and navigation.
    # ---------------------------
    def show_message(self, message, color=ft.Colors.BLUE_GREY_700):
        """Show a short feedback message at the bottom of the page."""
        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(message),
                bgcolor=color,
            )
        )
        self.page.update()

    def load_current_user(self):
        """Load the first existing user from the database."""
        users = self.main_db.get_all_users()
        if not users:
            self.current_user = None
            return
        self.current_user = create_user_instance_from_db(self.main_db, users[0])
        refresh_user_logs_from_db(self.main_db, self.current_user)

    def navigate(self, view_name):
        """Switch the current view and redraw the page."""
        self.current_view = view_name
        self.render()

    def refresh_current_user_logs(self):
        """Reload the current user's logs from the database."""
        if self.current_user is not None:
            refresh_user_logs_from_db(self.main_db, self.current_user)

    # ---------------------------
    # Reusable UI helpers
    # These small builders keep the actual views shorter and easier to read.
    # ---------------------------
    def create_info_card(self, title, content):
        """Create a simple card-like section."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
                    content,
                ],
                spacing=12,
            ),
            padding=16,
            border_radius=12,
            bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.WHITE),
            border=ft.border.all(1, ft.Colors.with_opacity(0.12, ft.Colors.WHITE)),
        )

    def build_navigation(self):
        """Build the mobile-friendly bottom navigation."""
        selected_index = {
            "dashboard": 0,
            "water": 1,
            "profile": 2,
        }.get(self.current_view, 0)
        return ft.NavigationBar(
            selected_index=selected_index,
            on_change=lambda e: self.navigate(
                ["dashboard", "water", "profile"][e.control.selected_index]
            ),
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.DASHBOARD_OUTLINED,
                    selected_icon=ft.Icons.DASHBOARD,
                    label="Dashboard",
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.WATER_DROP_OUTLINED,
                    selected_icon=ft.Icons.WATER_DROP,
                    label="Water",
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.PERSON_OUTLINE,
                    selected_icon=ft.Icons.PERSON,
                    label="Profile",
                ),
            ],
        )

    # ---------------------------
    # User creation view
    # This is the landing page when the database has no user yet.
    # ---------------------------
    def build_create_user_view(self):
        """Build the landing page for creating the first user."""
        name_field = ft.TextField(label="Name", autofocus=True)
        birthdate_field = ft.TextField(label="Birthdate (YYYY-MM-DD)")
        height_field = ft.TextField(
            label="Height in cm",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        gender_field = ft.Dropdown(
            label="Gender",
            options=[
                ft.dropdown.Option("m", "Male"),
                ft.dropdown.Option("f", "Female"),
                ft.dropdown.Option("d", "Diverse"),
            ],
        )
        fitness_field = ft.Dropdown(
            label="Fitness level",
            value="beginner",
            options=[
                ft.dropdown.Option("beginner"),
                ft.dropdown.Option("intermediate"),
                ft.dropdown.Option("advanced"),
            ],
        )

        def save_user(_):
            """Create the first user and open the dashboard."""
            try:
                user_id = self.main_db.add_user(
                    name_field.value.strip(),
                    birthdate_field.value.strip(),
                    int(height_field.value),
                    gender_field.value,
                    fitness_field.value,
                )
                self.current_user = User(
                    user_id,
                    name_field.value.strip(),
                    birthdate_field.value.strip(),
                    int(height_field.value),
                    gender_field.value,
                    fitness_field.value,
                    [],
                    [],
                    [],
                    [],
                )
                self.current_view = "dashboard"
                self.show_message("User created successfully.")
                self.render()
            except Exception as ex:
                self.show_message(
                    f"Could not create user: {ex}",
                    ft.Colors.RED_700,
                )

        return ft.Container(
            width=420,
            content=ft.Column(
                [
                    ft.Text("Welcome to SEDA", size=28, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "Create your user profile to start tracking water, weight and nutrition.",
                        color=ft.Colors.GREY_400,
                    ),
                    self.create_info_card(
                        "Create user",
                        ft.Column(
                            [
                                name_field,
                                birthdate_field,
                                height_field,
                                gender_field,
                                fitness_field,
                                ft.ElevatedButton(
                                    "Create user",
                                    icon=ft.Icons.PERSON_ADD,
                                    on_click=save_user,
                                ),
                            ],
                            spacing=12,
                        ),
                    ),
                ],
                spacing=20,
            ),
        )

    # ---------------------------
    # Dashboard view
    # This view shows a small first overview and the most important values.
    # ---------------------------
    def build_quick_actions(self):
        """Build the quick action buttons for the dashboard."""
        return ft.ResponsiveRow(
            [
                ft.Container(
                    col={"xs": 6, "sm": 3},
                    content=ft.ElevatedButton(
                        "Add water",
                        icon=ft.Icons.WATER_DROP,
                        on_click=lambda _: self.navigate("water"),
                        width=float("inf"),
                    ),
                ),
                ft.Container(
                    col={"xs": 6, "sm": 3},
                    content=ft.ElevatedButton(
                        "Water logs",
                        icon=ft.Icons.LIST,
                        on_click=lambda _: self.navigate("water"),
                        width=float("inf"),
                    ),
                ),
            ],
            spacing=12,
            run_spacing=12,
        )

    def build_dashboard_view(self):
        """Build the first overview screen."""
        calorie_status = get_today_calorie_status(self.current_user)
        water_status = get_today_water_status(self.current_user)

        overview_row = ft.ResponsiveRow(
            [
                ft.Container(
                    col={"xs": 12, "sm": 6},
                    content=self.create_info_card(
                        "Water today",
                        ft.Column(
                            [
                                ft.Text(f"{water_status['intake']} ml"),
                                ft.ProgressBar(
                                    value=min(1, (water_status["progress"] or 0) / 100),
                                    color=ft.Colors.BLUE_400,
                                ),
                                ft.Text(
                                    f"Target: {water_status['target']} ml | Left: {water_status['difference']} ml"
                                ),
                            ],
                            spacing=8,
                        ),
                    ),
                ),
                ft.Container(
                    col={"xs": 12, "sm": 6},
                    content=self.create_info_card(
                        "Weight & BMI",
                        ft.Column(
                            [
                                ft.Text(
                                    f"Current weight: {self.current_user.latest_weight} kg"
                                    if self.current_user.latest_weight is not None
                                    else "No weight logged yet"
                                ),
                                ft.Text(
                                    f"BMI: {self.current_user.last_bmi}"
                                    if self.current_user.last_bmi is not None
                                    else "BMI not available yet"
                                ),
                            ],
                            spacing=8,
                        ),
                    ),
                ),
            ],
            spacing=12,
            run_spacing=12,
        )

        return ft.Column(
            [
                ft.Text(
                    f"Welcome back, {self.current_user.name}!",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "This is your first dashboard with the most important values.",
                    color=ft.Colors.GREY_400,
                ),
                self.create_info_card(
                    "Calorie balance today",
                    ft.Column(
                        [
                            ft.Text(f"Intake: {calorie_status['intake']} kcal"),
                            ft.Text(f"Burned: {calorie_status['burned']} kcal"),
                            ft.Text(f"Net: {calorie_status['net']} kcal"),
                            ft.Text(
                                f"Target: {calorie_status['target']} kcal"
                                if calorie_status["target"] is not None
                                else "Target available after first weight log"
                            ),
                        ],
                        spacing=8,
                    ),
                ),
                overview_row,
                self.create_info_card("Quick actions", self.build_quick_actions()),
            ],
            spacing=16,
        )

    # ---------------------------
    # Water view
    # This is the first fully interactive tracker screen in the GUI.
    # ---------------------------
    def build_water_log_list(self):
        """Build the list of the latest water entries."""

        def delete_water_entry(log_id):
            """Delete one water log."""
            self.main_db.delete_water_log(log_id)
            self.current_user.water_log_handler.delete_log(log_id)
            self.show_message("Water log deleted.")
            self.render()

        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(f"{log.amount_in_ml} ml", expand=1),
                        ft.Text(log.timestamp, size=12, color=ft.Colors.GREY_400),
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            icon_color=ft.Colors.RED_300,
                            on_click=lambda _, log_id=log.id: delete_water_entry(
                                log_id
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
                for log in self.current_user.water_log_handler.logs[-10:]
            ]
            or [ft.Text("No water logs yet.", color=ft.Colors.GREY_400)]
        )

    def build_add_water_section(self):
        """Build the small form for adding water logs."""
        water_amount_field = ft.TextField(
            label="Amount in ml",
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        def save_water_log(_):
            """Save a new water log and refresh the view."""
            try:
                amount_in_ml = int(water_amount_field.value)
                new_log = self.current_user.water_log_handler.create_log(
                    None, amount_in_ml, None
                )
                db_id = self.main_db.add_water_log(
                    self.current_user.user_id,
                    new_log.amount_in_ml,
                    new_log.timestamp,
                )
                new_log.set_database_id(db_id)
                water_amount_field.value = ""
                self.show_message("Water log added successfully.")
                self.render()
            except Exception as ex:
                self.show_message(
                    f"Could not save water log: {ex}",
                    ft.Colors.RED_700,
                )

        return self.create_info_card(
            "Add water",
            ft.Row(
                [
                    ft.Container(expand=1, content=water_amount_field),
                    ft.ElevatedButton(
                        "Save",
                        icon=ft.Icons.SAVE,
                        on_click=save_water_log,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.END,
            ),
        )

    def build_water_view(self):
        """Build the water tracking screen."""
        self.refresh_current_user_logs()
        water_status = get_today_water_status(self.current_user)

        return ft.Column(
            [
                ft.Text("Water tracker", size=28, weight=ft.FontWeight.BOLD),
                self.create_info_card(
                    "Today's status",
                    ft.Column(
                        [
                            ft.Text(
                                f"{water_status['intake']} of {water_status['target']} ml"
                            ),
                            ft.ProgressBar(
                                value=min(1, (water_status["progress"] or 0) / 100),
                                color=ft.Colors.BLUE_400,
                            ),
                            ft.Text(f"{water_status['difference']} ml to go"),
                        ],
                        spacing=8,
                    ),
                ),
                self.build_add_water_section(),
                self.create_info_card("Last entries", self.build_water_log_list()),
            ],
            spacing=16,
        )

    # ---------------------------
    # Profile view
    # This is a simple read-only screen for the first GUI version.
    # ---------------------------
    def build_profile_view(self):
        """Build a simple profile page as navigation target."""
        calorie_status = get_today_calorie_status(self.current_user)
        return ft.Column(
            [
                ft.Text("Profile", size=28, weight=ft.FontWeight.BOLD),
                self.create_info_card(
                    "Personal data",
                    ft.Column(
                        [
                            ft.Text(f"Name: {self.current_user.name}"),
                            ft.Text(f"Birthdate: {self.current_user.birthdate}"),
                            ft.Text(f"Height: {self.current_user.height_in_cm} cm"),
                            ft.Text(f"Gender: {self.current_user.gender}"),
                            ft.Text(f"Fitness level: {self.current_user.fitness_lvl}"),
                        ],
                        spacing=8,
                    ),
                ),
                self.create_info_card(
                    "Calculated values",
                    ft.Column(
                        [
                            ft.Text(
                                f"Daily calorie target: {calorie_status['target']} kcal"
                                if calorie_status["target"] is not None
                                else "Daily calorie target: not available yet"
                            ),
                            ft.Text(
                                f"Daily water target: {self.current_user.daily_water_target} ml"
                            ),
                        ],
                        spacing=8,
                    ),
                ),
            ],
            spacing=16,
        )

    # ---------------------------
    # Render logic
    # This part chooses the active view and redraws the whole page.
    # ---------------------------
    def build_current_view(self):
        """Choose the current content depending on app state."""
        if self.current_user is None:
            return self.build_create_user_view()
        if self.current_view == "water":
            return self.build_water_view()
        if self.current_view == "profile":
            return self.build_profile_view()
        return self.build_dashboard_view()

    def render(self):
        """Draw the whole page again."""
        self.page.clean()
        content = self.build_current_view()
        self.page.add(
            ft.SafeArea(
                content=ft.Column(
                    [
                        content,
                    ],
                    spacing=20,
                    width=900,
                ),
                expand=True,
            )
        )
        if self.current_user is not None:
            self.page.navigation_bar = self.build_navigation()
        else:
            self.page.navigation_bar = None
        self.page.update()

    def run(self):
        """Start the first render cycle."""
        self.render()


def main(page: ft.Page):
    """Start the GUI application."""
    app = SedaGuiApp(page)
    app.run()


if __name__ == "__main__":
    ft.app(target=main)
