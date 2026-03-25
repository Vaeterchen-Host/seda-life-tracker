#AI generated code, which has been adapted for workability purposes
#ISSUES TO SOLVE: falsche Eingabe abfangen (Buchstaben & Werte außerhalb der Range)

import sys
from pathlib import Path
import datetime
import flet as ft

# 1. Suchpfad für Model-Imports (Sicherstellen, dass 'model' gefunden wird)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from model.classes import User, WaterLog, WeightLog
from model.database import Database

def main(page: ft.Page):
    # Grundeinstellungen der Seite
    page.title = "seda - version 0.1."
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = "auto"
    page.padding = 20

    db = Database()

    
    # User laden (für V.0.1 den ersten aus der DB nehmen)
    db_users = db.get_all_users()
    if not db_users:
        page.add(ft.Text("Kein User in der Datenbank gefunden. Bitte erst via CLI anlegen."))
        return
    
    u = db_users[0]
    current_user = User(u[0], u[1], u[2], u[3], u[4], u[5], [], [], [], [])

    # --- DATEN-LOGIK ---

    def load_water_logs():
        water_list.controls.clear()
        logs = db.get_all_water_logs()
        for log in reversed(logs):
            if log[1] == current_user.id:
                water_list.controls.append(
                    ft.ListTile(
                        leading=ft.Text("💧"),
                        title=ft.Text(f"{log[2]} ml"),
                        subtitle=ft.Text(f"{log[3]}"),
                        trailing=ft.TextButton("Löschen", on_click=lambda e, lid=log[0]: delete_water(lid))
                    )
                )
        page.update()

    def add_water(e):
        if water_input.value:
            try:
                amount = int(water_input.value)
                ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                db.add_water_log(current_user.id, amount, ts)
                water_input.value = ""
                water_input.error_text = None
                load_water_logs()
            except ValueError:
                water_input.error_text = "Nur Zahlen!"
                page.update()

    def delete_water(log_id):
        delete_data["id"] = log_id
        delete_data["type"] = "water"
        confirm_dialog.open = True
        page.update() # das eigentliche Löschen findet weiter unten statt!

    def update_bmi_view():
        weights = db.get_all_weight_logs()
        current_user.weight_logs = [WeightLog(r[0], r[2], r[3]) for r in weights if r[1] == current_user.id]
        bmi = current_user.calculate_bmi()
        bmi_display.value = f"Aktueller BMI: {bmi:.2f}" if bmi else "BMI: --"
        page.update()

    def load_weight_logs():
        weight_list.controls.clear()
        logs = db.get_all_weight_logs()
        for log in reversed(logs):
            if log[1] == current_user.id:
                weight_list.controls.append(
                    ft.ListTile(
                        leading=ft.Text("⚖️"), # Emoji statt Icon
                        title=ft.Text(f"{log[2]} kg"),
                        subtitle=ft.Text(f"{log[3]}"),
                        trailing=ft.TextButton("Löschen", on_click=lambda e, lid=log[0]: delete_weight(lid))
                    )
                )
        update_bmi_view() # BMI wird hier direkt mit aktualisiert


    def add_weight(e):
        if weight_input.value:
            try:
                w = float(weight_input.value.replace(",", "."))
                ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                db.add_weight_log(current_user.id, w, ts)
                weight_input.value = ""
                weight_input.error_text = None
                load_weight_logs()
            except ValueError:
                weight_input.error_text = "Ungültig!"
                page.update()

    def delete_weight(log_id):
        delete_data["id"] = log_id
        delete_data["type"] = "weight"
        confirm_dialog.open = True
        page.update() # das eigentliche Löschen findet weiter unten statt!

    # --- UI ANSICHTEN (VIEWS) ---

    # 1. Profil Ansicht
    bmi_display = ft.Text("BMI: --", size=25, weight="bold", color="blue")
    user_card = ft.Card(
        content=ft.Container(
            padding=20,
            content=ft.Column([
                ft.Text("User Profil", size=25, weight="bold"),
                ft.Text(f"Name: {current_user.name}", size=18),
                ft.Text(f"Geburtstag: {current_user.birthdate}"),
                ft.Text(f"Größe: {current_user.height_in_cm} cm"),
                ft.Text(f"Geschlecht: {current_user.gender}"),
                ft.Text(f"Fitness: {current_user.fitness_lvl}"),
                ft.Divider(),
                ft.Button("Daten ändern", disabled=True)
            ])
        )
    )
    profil_view = ft.Column([user_card, bmi_display], horizontal_alignment="center", visible=True)

    # 2. Wasser Ansicht
    water_input = ft.TextField(label="Menge", suffix=ft.Text("ml"), width=150)
    water_list = ft.ListView(spacing=5, height=400, divider_thickness=1)
    wasser_view = ft.Column([
        ft.Text("Wasser-Tracker", size=25, weight="bold"),
        ft.Row([water_input, ft.Button("Hinzufügen", on_click=add_water)]),
        ft.Text("Verlauf:", weight="bold"),
        ft.Container(content=water_list, padding=10) # Container hilft beim Rendering
    ], visible=False)

    # 3. Gewicht Ansicht
    weight_input = ft.TextField(label="Gewicht", suffix=ft.Text("kg"), width=150)
    weight_list = ft.ListView(spacing=5, height=400, divider_thickness=1)
    gewicht_view = ft.Column([
        ft.Text("Gewichts-Tracker", size=25, weight="bold"),
        ft.Row([weight_input, 
            ft.Button("Hinzufügen", on_click=add_weight)]),
        ft.Text("Verlauf:", weight="bold"),
        ft.Container(content=weight_list, padding=10) # Container für stabiles Rendering
    ], visible=False)

    # --- NAVIGATIONSLOGIK ---

    def show_view(view_index):
        # Alle Ansichten verstecken
        profil_view.visible = False
        wasser_view.visible = False
        gewicht_view.visible = False
        
        # Nur die gewählte Ansicht zeigen
        if view_index == 0:
            profil_view.visible = True
        elif view_index == 1:
            wasser_view.visible = True
        elif view_index == 2:
            gewicht_view.visible = True
        
        page.update()

    # Menü-Leiste oben
    menu_bar = ft.Row(
        controls=[
            ft.Button("Profil", on_click=lambda _: show_view(0)),
            ft.Button("Wasser", on_click=lambda _: show_view(1)),
            ft.Button("Gewicht", on_click=lambda _: show_view(2)),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
    )


    # --- LÖSCH-DIALOG (Sicherheitsabfrage) ---
    
    # Speicher für die ID, die gelöscht werden soll
    delete_data = {"id": None, "type": None}

    def close_dlg(e):
        confirm_dialog.open = False
        page.update()

    def confirm_delete_action(e):
        if delete_data["type"] == "water":
            db.delete_water_log(delete_data["id"])
            load_water_logs()
        else:
            db.delete_weight_log(delete_data["id"])
            load_weight_logs()
        
        confirm_dialog.open = False
        page.update()

    # Den Dialog definieren
    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Eintrag löschen?"),
        content=ft.Text("Möchtest du diesen Eintrag wirklich dauerhaft entfernen?"),
        actions=[
            ft.TextButton(
                content=ft.Text("Ja, löschen", color="red", weight="bold"), 
                on_click=confirm_delete_action
            ),
            ft.TextButton(
                content=ft.Text("Abbrechen"), 
                on_click=close_dlg
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Den Dialog im Hintergrund der Seite registrieren
    page.overlay.append(confirm_dialog)


    # --- SEITEN-INHALT ZUSAMMENBAUEN ---
    
    page.add(
        menu_bar,
        ft.Divider(height=20),
        profil_view,
        wasser_view,
        gewicht_view
    )
    
    # Daten beim Start laden
    load_water_logs()
    load_weight_logs()
    
    # Finale Aktualisierung
    page.update()

if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER)