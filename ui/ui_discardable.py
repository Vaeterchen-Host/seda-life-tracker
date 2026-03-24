#this file is only for testing purposes and can be discarded 

#ai generated example to display a dashboar d with matplotlib in tkinter

import flet as ft

def main(page: ft.Page):
    page.title = "Health Dashboard 2026"
    page.window_width = 800
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.bgcolor = "#f0f0f0"

    # --- Daten ---
    daten = [
        ("Frühstück", 450),
        ("Mittag", 750),
        ("Snack", 200),
        ("Abendessen", 600),
    ]
    gesamt_kalorien = sum(d[1] for d in daten)

    # --- Komponenten ---

    # Header
    header = ft.Text(
        "Mein Ernährungs-Tracker", 
        size=32, 
        weight=ft.FontWeight.BOLD, 
        color=ft.colors.BLUE_GREY_900
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
                    color=ft.colors.GREEN_700,
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
                        color=ft.colors.GREEN_400,
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
        bgcolor=ft.colors.WHITE,
        padding=20,
        border_radius=10,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.BLACK12)
    )

    # Layout zur Seite hinzufügen
    page.add(
        header,
        ft.VerticalDivider(height=10, color=ft.colors.TRANSPARENT),
        stats_card,
        ft.VerticalDivider(height=20, color=ft.colors.TRANSPARENT),
        chart_container
    )

if __name__ == "__main__":
    ft.app(target=main)