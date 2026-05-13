# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Water page builder for the SEDA desktop GUI. AI-generated."""

# pylint: disable=all

from __future__ import annotations

from typing import TYPE_CHECKING

import flet as ft

from application.status_service import get_today_water_status
from ui.gui_components import PrimaryButton, SurfaceItem, SurfaceSection
from ui.gui_dialogs import close_dialog, open_confirm_dialog
from ui.gui_theme import SEDA_MINT, SEDA_RED

if TYPE_CHECKING:
    from ui.gui import SedaGuiApp


def build_water_view(app: "SedaGuiApp"):
    """Build the water page with status, add-form and entry list. Partly AI-generated."""
    app.refresh_current_user_logs()
    water_status = get_today_water_status(app.current_user)

    amount_field = ft.TextField(
        label=app.t("amount_ml"),
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True,
    )
    timestamp_field = ft.TextField(
        label=app.t("optional_timestamp"),
        helper=app.t("use_now_when_empty"),
        hint_text=app.timestamp_input_hint(),
        expand=True,
    )

    def submit_water(_):
        """Create one water log from the inline form."""
        try:
            amount = app.parse_required_int(amount_field.value)
            timestamp = app.parse_optional_timestamp(timestamp_field.value)
            app.add_water_log(amount, timestamp)
        except Exception as exc:
            app.show_message(str(exc), error=True)

    status_section = SurfaceSection(
        app,
        app.t("water_status"),
        ft.Column(
            [
                ft.Text(
                    app.t(
                        "water_progress",
                        intake=water_status["intake"],
                        target=water_status["target"],
                    ),
                    size=22,
                ),
                ft.ProgressBar(
                    value=min(1, (water_status["progress"] or 0) / 100),
                    color=SEDA_MINT,
                    bgcolor=app.surface_border_color(),
                ),
                ft.Text(
                    app.t("water_to_go", difference=water_status["difference"]),
                    color=app.surface_muted_color(),
                ),
            ],
            spacing=12,
        ),
    )

    add_section = SurfaceSection(
        app,
        app.t("add_water"),
        ft.Row(
            [
                amount_field,
                timestamp_field,
                PrimaryButton(
                    app.t("save"),
                    icon=ft.Icons.SAVE,
                    on_click=submit_water,
                ),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.END,
        ),
    )

    water_rows = []
    for water_log in app.sort_logs_desc(app.current_user.water_log_handler.logs):
        source_label = (
            app.t("water_source_food")
            if water_log.source_type == "food"
            else app.t("water_source_manual")
        )
        water_rows.append(
            SurfaceItem(
                app,
                ft.Row(
                    [
                        ft.Text(
                            app.format_amount(water_log.amount_in_ml, "ml"),
                            width=120,
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    app.format_timestamp(water_log.timestamp),
                                    color=app.surface_muted_color(),
                                ),
                                ft.Text(
                                    source_label,
                                    size=12,
                                    color=app.surface_muted_color(),
                                ),
                            ],
                            spacing=4,
                            expand=True,
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            icon_color=SEDA_RED,
                            on_click=lambda _, log_id=water_log.id: open_confirm_dialog(
                                app,
                                app.t("msg_confirm_delete_entry"),
                                app.t("water_today"),
                                lambda dialog, target_id=log_id: (
                                    close_dialog(app, dialog),
                                    app.delete_water_log(target_id),
                                ),
                            ),
                        ),
                    ]
                ),
            )
        )

    entries_section = SurfaceSection(
        app,
        app.t("last_entries"),
        ft.Column(
            water_rows
            or [ft.Text(app.t("no_water_logs"), color=app.surface_muted_color())],
            spacing=10,
        ),
    )

    return ft.Column([status_section, add_section, entries_section], spacing=20)
