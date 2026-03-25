#this file is only for testing purposes and can be discarded 

#ai generated example to display a dashboard with Flet 

import flet as ft

def main(page: ft.Page):
    # main window
    page.title = "seda - version 0.1."
    page.bgcolor = "#f4f4f9"
    page.padding = 30

    # --- Daten ---
    daten = [
        ("Frühstück", 450),
        ("Mittag", 750),
        ("Snack", 200),
        ("Abendessen", 600)
    ]
    gesamt_kalorien = sum(d[1] for d in daten)

    # --- UI Komponenten ---

<<<<<<< HEAD
    # Überschrift 
    header = ft.Text("seda - version 0.1.", size=32, weight="bold")

    # Statistik-Anzeige
    stats = ft.Container(
=======
    # Header
    header = ft.Text(
        "Mein Ernährungs-Tracker", 
        size=32, 
        weight=ft.FontWeight.BOLD, 
        color=ft.Colors.BLUE_GREY_900
    )

    # Statistik-Karte
    stats_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Übersicht", size=20, weight=ft.FontWeight.W_500),
                ft.Divider(),
                ft.Text(
                    f"Heute konsumiert: {gesamt_kalorien} kcal", 
                    size=24, 
                    color=ft.Colors.GREEN_700,
                    weight=ft.FontWeight.BOLD
                ),
            ]),
            padding=20,
        ),
        elevation=2,
    )

    # Diagramm (Barchart)
    chart = ft.BarChart(
        bar_groups=[
            ft.BarChartGroup(
                x=i,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=val,
                        width=40,
                        color=ft.Colors.GREEN_400,
                        border_radius=5,
                    )
                ],
            ) for i, (label, val) in enumerate(daten)
        ],
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(value=i, label=ft.Text(label)) 
                for i, (label, val) in enumerate(daten)
            ]
        ),
        left_axis=ft.ChartAxis(title=ft.Text("kcal"), labels_size=40),
        max_y=1000,
        expand=True,
    )

    chart_container = ft.Container(
        content=ft.Column([
            ft.Text("Kalorien nach Mahlzeit", size=18, weight=ft.FontWeight.BOLD),
            ft.Container(chart, height=300, padding=10)
        ]),
        bgcolor=ft.Colors.WHITE,
>>>>>>> 8280f9cf4e1a104ab3d52c1e2bb86b74618c90a4
        padding=20,
        bgcolor="white",
        border_radius=10,
<<<<<<< HEAD
        content=ft.Text(f"Heute: {gesamt_kalorien} kcal", size=24, color="green", weight="bold")
=======
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12)
>>>>>>> 8280f9cf4e1a104ab3d52c1e2bb86b74618c90a4
    )

    # Balken-Diagramm
    balken_reihe = ft.Row(alignment="spaceEvenly", vertical_alignment="end")
    
    for label, wert in daten:
        # Wir bauen die Balken ganz simpel
        hoehe = (wert / 1000) * 200
        balken_reihe.controls.append(
            ft.Column([
                ft.Container(
                    width=50,
                    height=hoehe,
                    bgcolor="blue", # Blau ist immer sicher
                    border_radius=5
                ),
                ft.Text(label)
            ], horizontal_alignment="center")
        )

    # Layout zusammenfügen
    page.add(
        header,
<<<<<<< HEAD
        ft.Container(height=20),
        stats,
        ft.Container(height=20),
        ft.Text("Kalorien nach Mahlzeit", size=18, weight="bold"),
        ft.Container(content=balken_reihe, padding=20, bgcolor="white", border_radius=10)
=======
        ft.VerticalDivider(height=10, color=ft.Colors.TRANSPARENT),
        stats_card,
        ft.VerticalDivider(height=20, color=ft.Colors.TRANSPARENT),
        chart_container
>>>>>>> 8280f9cf4e1a104ab3d52c1e2bb86b74618c90a4
    )

#if __name__ == "__main__":
    #ft.app(target=main)


if __name__ == "__main__":
# Öffnet die App direkt in deinem Standard-Browser (Safari/Chrome/etc.)
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)