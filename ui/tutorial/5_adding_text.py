# pylint: disable=all
import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Text("Heading", size=28, weight="bold", color="#1e40af"),
        ft.Text(
            "This is a paragraph of regular text that wraps nicely across lines.",
            size=16,
        ),
        ft.Text("Small caption text", size=12, color="gray600"),
        ft.Text("Selectable text", selectable=True, size=15),
    )


ft.app(target=main)
