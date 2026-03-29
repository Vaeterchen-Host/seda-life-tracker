# pylint: disable=all
import flet as ft


def main(page: ft.Page):
    def handle_click(e):
        page.add(ft.Text("You clicked a button! 🎉"))

    page.add(
        ft.ElevatedButton("Primary Action", on_click=handle_click, icon=ft.Icons.SEND),
        ft.TextButton("Secondary Action", on_click=handle_click),
        ft.OutlinedButton("Medium Emphasis", on_click=handle_click),
    )


ft.app(target=main)
