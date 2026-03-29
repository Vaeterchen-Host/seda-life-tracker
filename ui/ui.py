# AI generated code, which has been adapted for workability purposes
# ISSUES TO SOLVE: Bestätigung nach Änderung der biometischen Daten; Fenster für Tracking-Ergebnisse verlängern

import sys
from pathlib import Path
import datetime
import flet as ft

# Suchpfad für Model-Imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.classes import User, WaterLog, WeightLog
from model.database import Database


def main(page: ft.Page):
    page.title = "seda - Personal Fitness Assistant"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    db = Database()
    db.connect()

    # --- "SNACKBAR" (= Balken unten) FÜR FEHLERMELDUNGEN ---
    def show_error(message):
        snack = ft.SnackBar(content=ft.Text(message), bgcolor="red")
        page.overlay.append(snack)
        snack.open = True
        page.update()

    # --- INITIALISIERUNG (LOGIK AUS CONTROLLER.PY) ---

    def get_full_user():
        db_users = db.get_all_users()
        if not db_users:
            return None

        u = db_users[0]  # Wir arbeiten mit dem ersten User

        # Logs aus DB holen und Instanzen erstellen (wie im Controller)
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
        page.add(ft.Text("Kein User gefunden. Bitte in der CLI anlegen."))
        return

    # --- UI ELEMENTE DEFINITION (Zuerst definieren, damit Funktionen darauf zugreifen können) ---

    # Einfache Begrüßung und Version definieren
    welcome_text = ft.Text(
        "Willkommen bei deiner Fitness-App!", size=40, weight="bold", color="blue"
    )
    version_text = ft.Text(
        "Version 0.1.| By Tobias Mignat & Sabine Steverding", size=10, color="grey500"
    )

    # Profil / Dashboard Elemente
    bmi_display = ft.Text("BMI: --", size=25, weight="bold", color="blue")
    water_today_display = ft.Text(
        "Heute getrunken: 0 ml", size=25, weight="bold", color="blue"
    )

    user_info_column = ft.Column(
        [
            ft.Text(f"Name: {current_user.name}", size=18),
            ft.Text(f"Geburtstag: {current_user.birthdate}"),
            ft.Text(f"Größe: {current_user.height_in_cm} cm"),
            ft.Text(f"Geschlecht: {current_user.gender}"),
            ft.Text(f"Fitness: {current_user.fitness_lvl}"),
        ]
    )

    # Wasser Elemente
    water_input = ft.TextField(label="Menge in ml", width=150)
    water_today_text = ft.Text(
        "Heute getrunken: 0 ml", size=18, weight="bold", color="blue"
    )
    water_list = ft.ListView(spacing=5, height=300, divider_thickness=1)

    # Gewicht Elemente
    weight_input = ft.TextField(label="Gewicht in kg", width=150)
    weight_list = ft.ListView(spacing=5, height=300, divider_thickness=1)

    # --- DATEN-LOGIK FUNKTIONEN ---

    def update_bmi_view():
        """Aktualisiert die BMI Anzeige auf dem Dashboard."""
        bmi = current_user.calculate_bmi()
        if isinstance(bmi, (int, float)):
            bmi_display.value = f"Aktueller BMI: {bmi:.2f}"
        else:
            bmi_display.value = "BMI: --"
        page.update()

    def load_water_logs():
        water_list.controls.clear()
        # Logik aus Controller: Refresh der Instanz-Daten
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
                        "Löschen", on_click=lambda e, lid=log.id: delete_water(lid)
                    ),
                )
            )
        # Update der Anzeige für "Heute getrunken" (Dashboard & Wasser-Tab)
        today_val = f"Heute getrunken: {current_user.water_intake_today()} ml"
        water_today_text.value = today_val
        water_today_display.value = today_val
        page.update()

    def add_water(e):
        if not water_input.value:
            return
        try:
            amount = int(water_input.value)
            # Wir lassen die Klasse prüfen (wirft ValueError wenn > 2000)
            test_log = WaterLog(0, amount, "2024-01-01 12:00")

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
                        "Löschen", on_click=lambda e, lid=log.id: delete_weight(lid)
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

            # Validierung durch die Klasse erzwingen
            test_log = WeightLog(0, w, ts)

            db.add_weight_log(current_user.id, w, ts)
            weight_input.value = ""
            load_weight_logs()
        except ValueError as ex:
            show_error(str(ex))

    # --- DIALOG FÜR BIOMETRISCHE DATEN ---

    edit_name = ft.TextField(label="Name", value=current_user.name)
    edit_height = ft.TextField(label="Größe (cm)", value=str(current_user.height_in_cm))
    edit_gender = ft.Dropdown(
        label="Geschlecht",
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

            # Validierung via Setter in classes.py
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

            # UI im Dashboard aktualisieren
            user_info_column.controls[0].value = f"Name: {current_user.name}"
            user_info_column.controls[2].value = (
                f"Größe: {current_user.height_in_cm} cm"
            )
            user_info_column.controls[3].value = f"Geschlecht: {current_user.gender}"
            user_info_column.controls[4].value = f"Fitness: {current_user.fitness_lvl}"

            update_bmi_view()
            edit_dialog.open = False
            page.update()
        except ValueError as ex:
            show_error(str(ex))

    edit_dialog = ft.AlertDialog(
        title=ft.Text("Daten bearbeiten"),
        content=ft.Column(
            [edit_name, edit_height, edit_gender, edit_fitness], tight=True
        ),
        actions=[
            ft.Button("Speichern", on_click=save_biometrical_data),
            ft.TextButton(
                "Abbrechen",
                on_click=lambda _: (setattr(edit_dialog, "open", False), page.update()),
            ),
        ],
    )
    page.overlay.append(edit_dialog)

    def open_edit_dialog(e):
        edit_dialog.open = True
        page.update()

    # --- VIEWS ZUSAMMENBAUEN ---

    profil_view = ft.Column(
        [
            ft.Card(
                content=ft.Container(
                    padding=20,
                    content=ft.Column(
                        [
                            ft.Text("User Profil", size=25, weight="bold"),
                            user_info_column,
                            ft.Divider(),
                            water_today_display,
                            bmi_display,
                            ft.Divider(),
                            ft.Button(
                                "Biometrische Daten ändern", on_click=open_edit_dialog
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
            ft.Text("Wasser-Tracker", size=25, weight="bold"),
            water_today_text,
            ft.Row([water_input, ft.Button("Hinzufügen", on_click=add_water)]),
            ft.Text("Verlauf:"),
            water_list,
        ],
        visible=False,
    )

    gewicht_view = ft.Column(
        [
            ft.Text("Gewichts-Tracker", size=25, weight="bold"),
            ft.Row([weight_input, ft.Button("Hinzufügen", on_click=add_weight)]),
            ft.Text("Verlauf:"),
            weight_list,
        ],
        visible=False,
    )

    # --- NAVIGATION & LÖSCH-LOGIK ---

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
        title=ft.Text("Löschen bestätigen"),
        content=ft.Text("Diesen Eintrag wirklich löschen?"),
        actions=[
            ft.TextButton("Ja", on_click=confirm_delete_action),
            ft.TextButton(
                "Abbrechen",
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
        page.update()

    menu_bar = ft.Row(
        [
            ft.Button("Profil", on_click=lambda _: show_view(0)),
            ft.Button("Wasser-Tracker", on_click=lambda _: show_view(1)),
            ft.Button("Gewichts-Tracker", on_click=lambda _: show_view(2)),
        ],
        alignment="center",
    )

    # Definition der Reihenfolge
    page.add(
        menu_bar,
        ft.Divider(),
        ft.Container(content=welcome_text, alignment=ft.Alignment(0, 0)),
        profil_view,
        wasser_view,
        gewicht_view,
        ft.Divider(),
        ft.Row([version_text], alignment="center"),
    )

    # Start-Daten laden
    load_water_logs()
    load_weight_logs()


# Web-Browser didn't worked on my (Tobias) machine, so I use the default view (desktop app)
if __name__ == "__main__":
    ft.run(main)  # ,view=ft.AppView.WEB_BROWSER)
