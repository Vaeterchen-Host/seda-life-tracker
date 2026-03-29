# pylint: disable=all
import flet as ft


def main(page: ft.Page):
    username = ft.TextField(label="Username", icon=ft.Icons.PERSON, width=300)

    def login(e):
        if username.value:
            page.add(ft.Text(f"Welcome, {username.value}!"))
        else:
            username.error_text = "Please enter a username"
            page.update()

    page.add(username, ft.ElevatedButton("Login", on_click=login))


ft.app(target=main)
