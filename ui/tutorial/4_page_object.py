# pylint: disable=all
import flet as ft


def main(page: ft.Page):
    # Configure the page
    page.title = "Page Object Demo"
    page.theme_mode = "light"
    page.bgcolor = "#f0fdf4"
    # page.bgcolor = "#000000"
    page.padding = 20

    # Add content
    page.add(ft.Text("This page is fully customized!", size=20))

    # Log page properties (visible in terminal)
    print(f"Page title: {page.title}, Theme: {page.theme_mode}")


ft.app(target=main)
