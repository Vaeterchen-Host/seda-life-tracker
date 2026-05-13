# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Activity page builder for the SEDA desktop GUI. AI-generated."""

# pylint: disable=all

from __future__ import annotations

from typing import TYPE_CHECKING

import flet as ft

from ui.gui_components import PrimaryButton, SurfaceItem, SurfaceSection
from ui.gui_dialogs import close_dialog, open_activity_edit_dialog, open_confirm_dialog
from ui.gui_theme import SEDA_MINT, SEDA_RED

if TYPE_CHECKING:
    from ui.gui import SedaGuiApp


def build_activity_view(app: "SedaGuiApp"):
    """Build the activity page with add form and editable entries. Partly AI-generated."""
    app.refresh_current_user_logs()

    name_field = ft.TextField(label=app.t("activity_name"), expand=True)
    calories_field = ft.TextField(
        label=app.t("calories_burned"),
        keyboard_type=ft.KeyboardType.NUMBER,
        width=180,
    )
    duration_field = ft.TextField(
        label=app.t("duration_minutes"),
        keyboard_type=ft.KeyboardType.NUMBER,
        width=180,
    )
    timestamp_field = ft.TextField(
        label=app.t("optional_timestamp"),
        helper=app.t("use_now_when_empty"),
        hint_text=app.timestamp_input_hint(),
        expand=True,
    )

    def submit_activity(_):
        """Create one activity entry from the inline desktop form."""
        try:
            activity_name = name_field.value.strip()
            calories = app.parse_required_float(calories_field.value)
            duration = app.parse_optional_float(duration_field.value)
            timestamp = app.parse_optional_timestamp(timestamp_field.value)
            app.add_activity_log(activity_name, calories, duration, timestamp)
        except Exception as exc:
            app.show_message(str(exc), error=True)

    add_section = SurfaceSection(
        app,
        app.t("add_activity"),
        ft.Column(
            [
                ft.Row([name_field, calories_field, duration_field], spacing=12),
                ft.Row(
                    [
                        timestamp_field,
                        PrimaryButton(
                            app.t("save"),
                            icon=ft.Icons.SAVE,
                            on_click=submit_activity,
                        ),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                ),
            ],
            spacing=12,
        ),
        subtitle=app.t("activity_copy"),
    )

    activity_rows = []
    for activity_log in app.sort_logs_desc(app.current_user.activity_log_handler.logs):
        activity_rows.append(
            SurfaceItem(
                app,
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(
                                    activity_log.activity_name,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    f"{app.format_amount(activity_log.calories_burned, 'kcal')} | "
                                    f"{app.format_amount(activity_log.activity_value, 'minutes')}",
                                    color=app.surface_muted_color(),
                                ),
                            ],
                            spacing=4,
                            expand=True,
                        ),
                        ft.Text(
                            app.format_timestamp(activity_log.timestamp),
                            color=app.surface_muted_color(),
                            width=170,
                        ),
                        ft.IconButton(
                            ft.Icons.EDIT_OUTLINED,
                            icon_color=SEDA_MINT,
                            on_click=lambda _, log=activity_log: open_activity_edit_dialog(
                                app,
                                log,
                            ),
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            icon_color=SEDA_RED,
                            on_click=lambda _, log_id=activity_log.id: open_confirm_dialog(
                                app,
                                app.t("msg_confirm_delete_entry"),
                                activity_log.activity_name,
                                lambda dialog, target_id=log_id: (
                                    close_dialog(app, dialog),
                                    app.delete_activity_log(target_id),
                                ),
                            ),
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )
        )

    entries_section = SurfaceSection(
        app,
        app.t("activity_logs"),
        ft.Column(
            activity_rows
            or [ft.Text(app.t("no_activity_logs"), color=app.surface_muted_color())],
            spacing=10,
        ),
    )

    return ft.Column([add_section, entries_section], spacing=20)
