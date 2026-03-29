# pylint: disable=all
# https://fletbuilder.com/flet-documents/flet-getting-started.html
import flet as ft


def main(page: ft.Page):
    page.title = "My First Flet App"
    page.add(ft.Text("Hello from Flet! 🐍✨", size=20, weight="bold"))


ft.app(target=main)
