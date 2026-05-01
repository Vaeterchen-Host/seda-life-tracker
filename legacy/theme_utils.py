"""This module provides utility functions for managing themes in a Flet application."""

# pylint: disable=all
import flet as ft


# ui/theme_utils.py
import flet as ft


def toggle_theme(page):
    page.theme_mode = "dark" if page.theme_mode == "light" else "light"
    page.update()


def create_theme_button(page):
    return ft.IconButton(
        icon=ft.Icons.SUNNY,
        on_click=lambda e: toggle_theme(page),
    )
