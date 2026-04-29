# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Graphical user interface for SEDA."""

# pylint: disable=all
# AI generated code, which has been adapted for workability purposes
# ISSUES TO SOLVE: Confirmation after changing biometrical data; make window for tracking results longer

import sys
from pathlib import Path
import datetime
import flet as ft


# Search path for model imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.classes import User, WaterLog, WeightLog
from model.database import Database
from config import DEVS, LICENSE_PATH, VERSION


def main(page: ft.Page):
    page.title = "seda - Personal Fitness Assistant"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    license_text = (
        LICENSE_PATH.read_text(encoding="utf-8")
        if LICENSE_PATH.exists()
        else "LICENSE.md not found."
    )

    db = Database()
    db.connect()

    # --- "SNACKBAR" (= bar at the bottom) FOR ERROR MESSAGES ---
    def show_error(message):
        snack = ft.SnackBar(content=ft.Text(message), bgcolor="red")
        page.overlay.append(snack)
        snack.open = True
        page.update()

    # --- INITIALIZATION (LOGIC FROM CONTROLLER.PY) ---

    def get_full_user():
        db_users = db.get_all_users()
        if not db_users:
            return None

        u = db_users[0]  # We work with the first user

        # Get logs from DB and create instances (like in controller)
        water_logs = [
            WaterLog(l[0], l[2], l[3]) for l in db.get_all_water_logs() if l[1] == u[0]
        ]
        weight_logs = [
            WeightLog(l[0], l[2], l[3])
            for l in db.get_all_weight_logs()
            if l[1] == u[0]
        ]

        return User(u[0], u[1], u[2], u[3], u[4], u[5], water_logs, weight_logs, [], [])

    current_user = get_full_user()

    if not current_user:
        page.add(ft.Text("No user found. Please create one in CLI."))
        return

    # --- UI ELEMENTS DEFINITION (Define first, so functions can access them) ---

    # Define simple greeting and version
    welcome_text = ft.Text(
        "Welcome to your fitness app!", size=40, weight="bold", color="blue"
    )
    version_text = ft.Text(f"Version {VERSION} | By {DEVS}", size=10, color="grey500")

    # Profile / Dashboard elements
    bmi_display = ft.Text("BMI: --", size=25, weight="bold", color="blue")
    water_today_display = ft.Text(
        "Drunk today: 0 ml", size=25, weight="bold", color="blue"
    )

    user_info_column = ft.Column(
        [
            ft.Text(f"Name: {current_user.name}", size=18),
            ft.Text(f"Birthday: {current_user.birthdate}"),
            ft.Text(f"Height: {current_user.height_in_cm} cm"),
            ft.Text(f"Gender: {current_user.gender}"),
            ft.Text(f"Fitness: {current_user.fitness_lvl}"),
        ]
    )

    # Water elements
    water_input = ft.TextField(label="Amount in ml", width=150)
    water_today_text = ft.Text(
        "Drunk today: 0 ml", size=18, weight="bold", color="blue"
    )
    water_list = ft.ListView(spacing=5, height=300, divider_thickness=1)

    # Weight elements
    weight_input = ft.TextField(label="Weight in kg", width=150)
    weight_list = ft.ListView(spacing=5, height=300, divider_thickness=1)

    # --- DATA LOGIC FUNCTIONS ---

    def update_bmi_view():
        """Updates the BMI display on the dashboard."""
        bmi = current_user.calculate_bmi()
        if isinstance(bmi, (int, float)):
            bmi_display.value = f"Current BMI: {bmi:.2f}"
        else:
            bmi_display.value = "BMI: --"
        page.update()

    def load_water_logs():
        water_list.controls.clear()
        # Logic from controller: refresh of instance data
        current_user.water_logs = [
            WaterLog(l[0], l[2], l[3])
            for l in db.get_all_water_logs()
            if l[1] == current_user.id
        ]

        for log in reversed(current_user.water_logs):
            water_list.controls.append(
                ft.ListTile(
                    leading=ft.Text("💧"),
                    title=ft.Text(f"{log.amount_in_ml} ml"),
                    subtitle=ft.Text(f"{log.timestamp}"),
                    trailing=ft.TextButton(
                        "Delete", on_click=lambda e, lid=log.id: delete_water(lid)
                    ),
                )
            )
        # Update display for "Drunk today" (dashboard & water tab)
        today_val = f"Drunk today: {current_user.water_intake_today()} ml"
        water_today_text.value = today_val
        water_today_display.value = today_val
        page.update()

    def add_water(e):
        if not water_input.value:
            return
        try:
            amount = int(water_input.value)
            # Let the class validate (raises ValueError if > 2000)
            # test_log = WaterLog(0, amount, "2024-01-01 12:00")

            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            db.add_water_log(current_user.id, amount, ts)
            water_input.value = ""
            load_water_logs()
        except ValueError as ex:
            show_error(str(ex))

    def load_weight_logs():
        weight_list.controls.clear()
        current_user.weight_logs = [
            WeightLog(l[0], l[2], l[3])
            for l in db.get_all_weight_logs()
            if l[1] == current_user.id
        ]

        for log in reversed(current_user.weight_logs):
            weight_list.controls.append(
                ft.ListTile(
                    leading=ft.Text("⚖️"),
                    title=ft.Text(f"{log.weight_in_kg} kg"),
                    subtitle=ft.Text(f"{log.timestamp}"),
                    trailing=ft.TextButton(
                        "Delete", on_click=lambda e, lid=log.id: delete_weight(lid)
                    ),
                )
            )
        update_bmi_view()

    def add_weight(e):
        if not weight_input.value:
            return
        try:
            val = weight_input.value.replace(",", ".")
            w = float(val)
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

            # Force validation by class
            # test_log = WeightLog(0, w, ts)

            db.add_weight_log(current_user.id, w, None, ts)
            weight_input.value = ""
            load_weight_logs()
        except ValueError as ex:
            show_error(str(ex))

    # --- DIALOG FOR BIOMETRICAL DATA ---

    edit_name = ft.TextField(label="Name", value=current_user.name)
    edit_height = ft.TextField(
        label="Height (cm)", value=str(current_user.height_in_cm)
    )
    edit_gender = ft.Dropdown(
        label="Gender",
        options=[
            ft.dropdown.Option("m"),
            ft.dropdown.Option("f"),
            ft.dropdown.Option("d"),
        ],
        value=current_user.gender,
    )
    edit_fitness = ft.Dropdown(
        label="Fitness Level",
        options=[
            ft.dropdown.Option("beginner"),
            ft.dropdown.Option("intermediate"),
            ft.dropdown.Option("advanced"),
        ],
        value=current_user.fitness_lvl,
    )

    def save_biometrical_data(e):
        try:
            new_name = edit_name.value
            new_height = int(edit_height.value)
            new_gender = edit_gender.value
            new_fitness = edit_fitness.value

            # Validation by setter in classes.py
            current_user.name = new_name
            current_user.update_biometrical_data(
                height_in_cm=new_height, gender=new_gender, fitness_lvl=new_fitness
            )

            db.update_user(
                current_user.id,
                current_user.name,
                current_user.birthdate,
                current_user.height_in_cm,
                current_user.gender,
                current_user.fitness_lvl,
            )

            # Update UI in dashboard
            user_info_column.controls[0].value = f"Name: {current_user.name}"
            user_info_column.controls[2].value = (
                f"Height: {current_user.height_in_cm} cm"
            )
            user_info_column.controls[3].value = f"Gender: {current_user.gender}"
            user_info_column.controls[4].value = f"Fitness: {current_user.fitness_lvl}"

            update_bmi_view()
            edit_dialog.open = False
            page.update()
        except ValueError as ex:
            show_error(str(ex))

    edit_dialog = ft.AlertDialog(
        title=ft.Text("Edit data"),
        content=ft.Column(
            [edit_name, edit_height, edit_gender, edit_fitness], tight=True
        ),
        actions=[
            ft.Button("Save", on_click=save_biometrical_data),
            ft.TextButton(
                "Cancel",
                on_click=lambda _: (setattr(edit_dialog, "open", False), page.update()),
            ),
        ],
    )
    page.overlay.append(edit_dialog)

    def open_edit_dialog(e):
        edit_dialog.open = True
        page.update()

    # --- BUILD VIEWS ---

    profil_view = ft.Column(
        [
            ft.Card(
                content=ft.Container(
                    padding=20,
                    content=ft.Column(
                        [
                            ft.Text("User profile", size=25, weight="bold"),
                            user_info_column,
                            ft.Divider(),
                            water_today_display,
                            bmi_display,
                            ft.Divider(),
                            ft.Button(
                                "Change biometrical data", on_click=open_edit_dialog
                            ),
                        ]
                    ),
                )
            ),
        ],
        horizontal_alignment="center",
        visible=True,
    )

    wasser_view = ft.Column(
        [
            ft.Text("Water tracker", size=25, weight="bold"),
            water_today_text,
            ft.Row([water_input, ft.Button("Add", on_click=add_water)]),
            ft.Text("History:"),
            water_list,
        ],
        visible=False,
    )

    gewicht_view = ft.Column(
        [
            ft.Text("Weight tracker", size=25, weight="bold"),
            ft.Row([weight_input, ft.Button("Add", on_click=add_weight)]),
            ft.Text("History:"),
            weight_list,
        ],
        visible=False,
    )

    # AI-generated content: about view with embedded license text.
    about_view = ft.Column(
        [
            ft.Card(
                content=ft.Container(
                    padding=20,
                    content=ft.Column(
                        [
                            ft.Text("About", size=25, weight="bold"),
                            ft.Text(
                                f"SEDA version {VERSION}",
                                size=18,
                                weight="bold",
                                color="blue",
                            ),
                            ft.Text(f"Developed by {DEVS}"),
                            ft.Text(
                                "SEDA is a personal fitness assistant with tracking for water intake and weight."
                            ),
                            ft.Divider(),
                            ft.Text("License", size=20, weight="bold"),
                            ft.Container(
                                content=ft.Column(
                                    [ft.Text(license_text, selectable=True)],
                                    scroll=ft.ScrollMode.AUTO,
                                ),
                                height=420,
                                padding=10,
                                border=ft.border.all(1, "grey400"),
                                border_radius=8,
                                bgcolor="grey50",
                            ),
                        ]
                    ),
                )
            )
        ],
        visible=False,
    )

    # --- NAVIGATION & DELETE LOGIC ---

    delete_data = {"id": None, "type": None}

    def confirm_delete_action(e):
        if delete_data["type"] == "water":
            db.delete_water_log(delete_data["id"])
            load_water_logs()
        else:
            db.delete_weight_log(delete_data["id"])
            load_weight_logs()
        confirm_dialog.open = False
        page.update()

    confirm_dialog = ft.AlertDialog(
        title=ft.Text("Confirm delete"),
        content=ft.Text("Really delete this entry?"),
        actions=[
            ft.TextButton("Yes", on_click=confirm_delete_action),
            ft.TextButton(
                "Cancel",
                on_click=lambda _: (
                    setattr(confirm_dialog, "open", False),
                    page.update(),
                ),
            ),
        ],
    )
    page.overlay.append(confirm_dialog)

    def delete_water(log_id):
        delete_data.update({"id": log_id, "type": "water"})
        confirm_dialog.open = True
        page.update()

    def delete_weight(log_id):
        delete_data.update({"id": log_id, "type": "weight"})
        confirm_dialog.open = True
        page.update()

    def show_view(idx):
        profil_view.visible = idx == 0
        wasser_view.visible = idx == 1
        gewicht_view.visible = idx == 2
        about_view.visible = idx == 3
        page.update()

    menu_bar = ft.Row(
        [
            ft.Button("Profile", on_click=lambda _: show_view(0)),
            ft.Button("Water tracker", on_click=lambda _: show_view(1)),
            ft.Button("Weight tracker", on_click=lambda _: show_view(2)),
            ft.Button("About", on_click=lambda _: show_view(3)),
        ],
        alignment="center",
    )

    # Define order
    page.add(
        menu_bar,
        ft.Divider(),
        ft.Container(content=welcome_text, alignment=ft.Alignment(0, 0)),
        profil_view,
        wasser_view,
        gewicht_view,
        about_view,
        ft.Divider(),
        ft.Row([version_text], alignment="center"),
    )

    # Load start data
    load_water_logs()
    load_weight_logs()


# Web browser did not work on my (Tobias) machine, so I use the default view (desktop app)
if __name__ == "__main__":
    ft.run(main)  # ,view=ft.AppView.WEB_BROWSER)
