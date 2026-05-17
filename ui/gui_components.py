# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Reusable Flet GUI controls for SEDA. Partly AI-generated."""

# pylint: disable=all

from __future__ import annotations

from datetime import date, datetime, time
from typing import TYPE_CHECKING

import flet as ft

from ui.gui_theme import NAV_ITEMS, SEDA_MINT, SEDA_YELLOW

if TYPE_CHECKING:
    from ui.gui import SedaGuiApp


MAX_CONTENT_WIDTH = 1320
PAGE_SHELL_PADDING = 24
HEADER_ACTIONS_MIN_WIDTH = 900


def _current_logo_asset_path(is_dark_mode: bool) -> str:
    """Return the theme-matching horizontal SEDA logo asset path. AI-generated."""
    return (
        "/darkmode_logo_horizontal.svg"
        if is_dark_mode
        else "/brightmode_logo_horizontal.svg"
    )


def _resolve_content_width(app: "SedaGuiApp") -> int | None:
    """Resolve the centered max content width for the current page size. AI-generated."""
    viewport_width = int(app.page.width or app.page.window.width or 0)
    if viewport_width <= 0:
        return MAX_CONTENT_WIDTH

    available_width = max(360, viewport_width - (PAGE_SHELL_PADDING * 2))
    return min(available_width, MAX_CONTENT_WIDTH)


def _show_header_actions(app: "SedaGuiApp") -> bool:
    """Return whether the desktop header should show language/theme buttons. AI-generated."""
    if app.current_user is None:
        return True
    viewport_width = int(app.page.width or app.page.window.width or 0)
    if viewport_width <= 0:
        return True
    return viewport_width >= HEADER_ACTIONS_MIN_WIDTH


class SedaLogo(ft.Image):
    """Render one theme-aware horizontal SEDA logo. AI-generated."""

    def __init__(self, is_dark_mode: bool, width: int = 220):
        super().__init__(
            src=_current_logo_asset_path(is_dark_mode),
            width=width,
            fit=ft.BoxFit.CONTAIN,
        )


class PrimaryButton(ft.FilledButton):
    """Render one primary action button in seda-mint. AI-generated."""

    def __init__(self, text: str, icon=None, on_click=None, expand: bool = False):
        super().__init__(
            content=text,
            icon=icon,
            expand=expand,
            on_click=on_click,
            style=ft.ButtonStyle(
                bgcolor=SEDA_MINT,
                color=ft.Colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        )


class SurfaceSection(ft.Container):
    """Wrap one logical area in a consistent desktop section style. AI-generated."""

    def __init__(
        self,
        app: "SedaGuiApp",
        title: str,
        content,
        subtitle: str | None = None,
        trailing=None,
    ):
        header_controls = [
            ft.Column(
                [
                    ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
                    (
                        ft.Text(subtitle, size=12, color=app.surface_muted_color())
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

        super().__init__(
            padding=20,
            border_radius=8,
            bgcolor=app.surface_background_color(),
            border=ft.border.all(1, app.surface_border_color()),
            content=ft.Column(
                [
                    ft.Row(
                        header_controls,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    content,
                ],
                spacing=14,
            ),
        )


class SurfaceItem(ft.Container):
    """Render one secondary framed item on top of the alternate surface. AI-generated."""

    def __init__(self, app: "SedaGuiApp", content):
        super().__init__(
            padding=12,
            border_radius=8,
            bgcolor=app.surface_background_alt_color(),
            border=ft.border.all(1, app.surface_border_color()),
            content=content,
        )


class LabelValueRow(ft.Row):
    """Render one compact label/value pair. AI-generated."""

    def __init__(self, app: "SedaGuiApp", label: str, value: str):
        super().__init__(
            [
                ft.Text(label, color=app.surface_muted_color(), expand=1),
                ft.Text(value, weight=ft.FontWeight.W_500),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )


class MetricChip(ft.Container):
    """Render one compact dashboard metric in a framed block. AI-generated."""

    def __init__(self, app: "SedaGuiApp", label: str, value: str, accent=SEDA_MINT):
        super().__init__(
            padding=12,
            border_radius=8,
            bgcolor=app.surface_background_alt_color(),
            border=ft.border.all(1, app.surface_border_color()),
            content=ft.Column(
                [
                    ft.Text(label, size=12, color=app.surface_muted_color()),
                    ft.Text(value, size=18, weight=ft.FontWeight.BOLD, color=accent),
                ],
                spacing=4,
                tight=True,
            ),
        )


class DatePickerField(ft.Row):
    """Render one read-only date field backed by a Flet DatePicker. AI-generated."""

    def __init__(
        self,
        app: "SedaGuiApp",
        label: str,
        value: date | None = None,
        width: int | None = None,
        expand: bool = False,
    ):
        self.app = app
        self.selected_date = value or datetime.now().date()
        self._field = ft.TextField(
            label=label,
            value=app.format_picker_date(self.selected_date),
            read_only=True,
            can_request_focus=False,
            always_call_on_tap=True,
            on_click=self._open_picker,
            suffix_icon=ft.Icons.CALENDAR_MONTH,
            width=width,
            expand=expand,
        )
        self._picker = ft.DatePicker(
            value=datetime.combine(self.selected_date, time.min),
            first_date=datetime(year=1900, month=1, day=1),
            last_date=datetime(year=2100, month=12, day=31),
            locale=app.current_locale(),
            on_change=self._handle_change,
        )
        super().__init__([self._field], vertical_alignment=ft.CrossAxisAlignment.END)

    def _open_picker(self, _):
        """Open the date picker with the currently selected date. AI-generated."""
        self._picker.value = datetime.combine(self.selected_date, time.min)
        self.app.page.show_dialog(self._picker)

    def _handle_change(self, e):
        """Persist the selected date in the read-only field. AI-generated."""
        self.selected_date = e.control.value.date()
        self._field.value = self.app.format_picker_date(self.selected_date)
        self.app.page.update()


class TimePickerField(ft.Row):
    """Render one read-only time field backed by a Flet TimePicker. AI-generated."""

    def __init__(
        self,
        app: "SedaGuiApp",
        label: str,
        value: time | None = None,
        width: int | None = None,
        expand: bool = False,
    ):
        self.app = app
        self.selected_time = value or datetime.now().replace(second=0, microsecond=0).time()
        self._field = ft.TextField(
            label=label,
            value=app.format_picker_time(self.selected_time),
            read_only=True,
            can_request_focus=False,
            always_call_on_tap=True,
            on_click=self._open_picker,
            suffix_icon=ft.Icons.ACCESS_TIME,
            width=width,
            expand=expand,
        )
        self._picker = ft.TimePicker(
            value=self.selected_time,
            entry_mode=ft.TimePickerEntryMode.DIAL,
            locale=app.current_locale(),
            on_change=self._handle_change,
        )
        super().__init__([self._field], vertical_alignment=ft.CrossAxisAlignment.END)

    def _open_picker(self, _):
        """Open the time picker with the current selection. AI-generated."""
        self._picker.value = self.selected_time
        self.app.page.show_dialog(self._picker)

    def _handle_change(self, e):
        """Store the selected time and update the read-only display. AI-generated."""
        self.selected_time = e.control.value
        self._field.value = self.app.format_picker_time(self.selected_time)
        self.app.page.update()


class PrimaryNav(ft.Row):
    """Build the persistent primary navigation row for the desktop shell. AI-generated."""

    def __init__(self, app: "SedaGuiApp"):
        buttons = []
        for view_name, label_key, icon in NAV_ITEMS:
            active = app.current_view == view_name
            button = (
                ft.FilledButton(
                    content=app.t(label_key),
                    icon=icon,
                    style=ft.ButtonStyle(
                        bgcolor=SEDA_YELLOW,
                        color=ft.Colors.BLACK,
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=lambda _, target=view_name: app.navigate(target),
                )
                if active
                else ft.OutlinedButton(
                    content=app.t(label_key),
                    icon=icon,
                    style=ft.ButtonStyle(
                        color=app.primary_text_color(),
                        side=ft.BorderSide(1, SEDA_MINT),
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=lambda _, target=view_name: app.navigate(target),
                )
            )
            buttons.append(button)

        super().__init__(buttons, wrap=True, spacing=10, run_spacing=10)


class DesktopHeader(ft.Column):
    """Build the persistent desktop header with branding and shell actions. AI-generated."""

    def __init__(self, app: "SedaGuiApp"):
        show_brand_logo = app.current_user is not None
        shell_actions = (
            ft.Row(
                [
                    ft.PopupMenuButton(
                        icon=ft.Icons.LANGUAGE,
                        tooltip=app.t("language"),
                        icon_color=SEDA_YELLOW if app.is_dark_mode() else SEDA_MINT,
                        items=[
                            ft.PopupMenuItem(
                                content=app.t("language_en"),
                                on_click=lambda _: app.change_language("en"),
                            ),
                            ft.PopupMenuItem(
                                content=app.t("language_de"),
                                on_click=lambda _: app.change_language("de"),
                            ),
                        ],
                    ),
                    ft.IconButton(
                        icon=ft.Icons.SUNNY,
                        icon_color=SEDA_YELLOW if app.is_dark_mode() else SEDA_MINT,
                        bgcolor=app.surface_background_alt_color(),
                        tooltip=app.t("toggle_theme"),
                        on_click=app.toggle_theme,
                    ),
                ],
                spacing=8,
            )
            if _show_header_actions(app)
            else ft.Container()
        )

        header_row = ft.Row(
            [
                SedaLogo(app.is_dark_mode(), width=220)
                if show_brand_logo
                else ft.Container(),
                ft.Container(expand=True),
                shell_actions,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

        super().__init__(
            [header_row, PrimaryNav(app)] if app.current_user is not None else [header_row],
            spacing=18,
        )


class PageShell(ft.SafeArea):
    """Wrap one page body in the standard centered desktop shell. AI-generated."""

    def __init__(self, app: "SedaGuiApp", content):
        resolved_width = _resolve_content_width(app)
        page_column = ft.Column(
            [
                DesktopHeader(app),
                ft.Container(content=content, expand=True),
            ],
            spacing=20,
        )
        page_container = ft.Container(
            content=page_column,
            padding=PAGE_SHELL_PADDING,
            width=resolved_width,
        )

        super().__init__(
            expand=True,
            content=ft.Container(
                expand=True,
                alignment=ft.Alignment.TOP_CENTER,
                content=page_container,
            ),
        )
