# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Reusable Flet GUI components extracted from ui.gui."""

# pylint: disable=all

import flet as ft

from config import VERSION
from ui.gui_theme import BRAND_MINT, BRAND_YELLOW, NAV_ITEMS


# ---------------------------
# Reusable UI builders
# These helpers create the shared desktop shell and smaller UI fragments.
# ---------------------------
def build_surface_section(self, title, content, subtitle=None, trailing=None):
    """Wrap one logical area in a consistent desktop section style. Partly AI-generated."""
    header_controls = [
        ft.Column(
            [
                ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
                (
                    ft.Text(subtitle, size=12, color=self.surface_muted_color())
                    if subtitle
                    else ft.Container()
                ),
            ],
            spacing=4,
            tight=True,
            expand=True,
        )
    ]
    if trailing is not None:
        header_controls.append(trailing)

    return ft.Container(
        padding=20,
        border_radius=8,
        bgcolor=self.surface_background_color(),
        border=ft.border.all(1, self.surface_border_color()),
        content=ft.Column(
            [
                ft.Row(header_controls, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                content,
            ],
            spacing=14,
        ),
    )


def build_label_value_row(self, label, value):
    """Render one compact label/value pair. Partly AI-generated."""
    return ft.Row(
        [
            ft.Text(label, color=self.surface_muted_color(), expand=1),
            ft.Text(value, weight=ft.FontWeight.W_500),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )


def build_metric_chip(self, label, value, accent=BRAND_MINT):
    """Render one compact dashboard metric as a small framed block. Partly AI-generated."""
    return ft.Container(
        padding=12,
        border_radius=8,
        bgcolor=self.surface_background_alt_color(),
        border=ft.border.all(1, self.surface_border_color()),
        content=ft.Column(
            [
                ft.Text(label, size=12, color=self.surface_muted_color()),
                ft.Text(value, size=18, weight=ft.FontWeight.BOLD, color=accent),
            ],
            spacing=4,
            tight=True,
        ),
    )


def build_primary_nav(self):
    """Build the top navigation row in the style of the desktop mockups. Partly AI-generated."""
    buttons = []
    for view_name, label_key, icon in NAV_ITEMS:
        active = self.current_view == view_name
        button = (
            ft.FilledButton(
                content=self.t(label_key),
                icon=icon,
                style=ft.ButtonStyle(
                    bgcolor=BRAND_YELLOW,
                    color=ft.Colors.BLACK,
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
                on_click=lambda _, target=view_name: self.navigate(target),
            )
            if active
            else ft.OutlinedButton(
                content=self.t(label_key),
                icon=icon,
                style=ft.ButtonStyle(
                    color=self.primary_text_color(),
                    side=ft.BorderSide(1, BRAND_MINT),
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
                on_click=lambda _, target=view_name: self.navigate(target),
            )
        )
        buttons.append(button)

    return ft.Row(buttons, wrap=True, spacing=10, run_spacing=10)


def build_header(self):
    """Build the persistent desktop header with branding and active user. Partly AI-generated."""
    return ft.Column(
        [
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(
                                f"{self.t('app_title')} v{VERSION}",
                                size=12,
                                color=self.surface_muted_color(),
                            ),
                            ft.Text(
                                self.t("app_subtitle"),
                                size=30,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=2,
                        tight=True,
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.SUNNY,
                        icon_color=BRAND_YELLOW if self.is_dark_mode() else BRAND_MINT,
                        bgcolor=self.surface_background_alt_color(),
                        tooltip=self.t("toggle_theme"),
                        on_click=self.toggle_theme,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            (
                self.build_primary_nav()
                if self.current_user is not None
                else ft.Container()
            ),
        ],
        spacing=18,
    )


def build_page_shell(self, content):
    """Assemble the persistent desktop shell around the current page body. Partly AI-generated."""
    return ft.SafeArea(
        expand=True,
        content=ft.Container(
            expand=True,
            padding=24,
            content=ft.Column(
                [
                    self.build_header(),
                    ft.Container(content=content, expand=True),
                ],
                spacing=20,
            ),
            alignment=ft.Alignment.TOP_CENTER,
        ),
    )
