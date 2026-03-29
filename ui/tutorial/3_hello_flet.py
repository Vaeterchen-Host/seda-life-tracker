# pylint: disable=all
import flet as ft


def main(page: ft.Page):
    # Set the browser tab title
    page.title = "Hello, Flet World!"
    # Add a text control to the page
    page.add(ft.Text("Your journey begins here.", size=18))


# Launch the app
ft.app(target=main)
