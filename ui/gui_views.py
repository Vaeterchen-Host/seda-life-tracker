# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""GUI page builders extracted from ui.gui."""

# pylint: disable=all

import flet as ft

from config import DEVS
from application.status_service import get_today_calorie_status, get_today_water_status
from ui.gui_theme import SEDA_MINT, SEDA_RED, SEDA_YELLOW


# ---------------------------
# Landing view
# This screen is shown until the first user account exists.
# ---------------------------
def build_create_user_view(self):
    """Build the account-creation landing page. Partly AI-generated."""
    name_field = ft.TextField(label=self.t("name"), autofocus=True)
    birthdate_field = ft.TextField(
        label=self.t("birthdate"),
        hint_text=self.birthdate_input_hint(),
    )
    height_field = ft.TextField(
        label=self.t("height_cm"),
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    gender_dropdown = ft.Dropdown(
        label=self.t("gender"),
        value="m",
        options=[
            ft.DropdownOption(key="m", text=self.t("gender_m")),
            ft.DropdownOption(key="f", text=self.t("gender_f")),
            ft.DropdownOption(key="d", text=self.t("gender_d")),
        ],
    )
    fitness_dropdown = ft.Dropdown(
        label=self.t("fitness_level"),
        value="beginner",
        options=[
            ft.DropdownOption(key="beginner", text=self.t("fitness_beginner")),
            ft.DropdownOption(key="intermediate", text=self.t("fitness_intermediate")),
            ft.DropdownOption(key="advanced", text=self.t("fitness_advanced")),
        ],
    )

    def submit_user(_):
        """Validate the landing-page form and create the first user."""
        try:
            name = name_field.value.strip()
            birthdate = self.parse_birthdate(birthdate_field.value)
            height = self.parse_required_int(height_field.value)
            if not name:
                raise ValueError(self.t("name"))
            self.create_user(
                name,
                birthdate,
                height,
                gender_dropdown.value,
                fitness_dropdown.value,
            )
        except Exception as exc:
            self.show_message(str(exc), error=True)

    form = self.build_surface_section(
        self.t("create_user"),
        ft.Column(
            [
                name_field,
                birthdate_field,
                height_field,
                gender_dropdown,
                fitness_dropdown,
                ft.FilledButton(
                    self.t("create_user"),
                    icon=ft.Icons.PERSON_ADD,
                    style=ft.ButtonStyle(
                        bgcolor=SEDA_YELLOW,
                        color=ft.Colors.BLACK,
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=submit_user,
                ),
            ],
            spacing=12,
        ),
    )

    content = ft.Row(
        [
            ft.Container(
                expand=1,
                content=ft.Column(
                    [
                        ft.Text(
                            self.t("landing_title"),
                            size=36,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            self.t("landing_copy"),
                            size=16,
                            color=self.surface_muted_color(),
                        ),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=ft.padding.only(right=24),
            ),
            ft.Container(width=420, content=form),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return self.build_page_shell(content)


# ---------------------------
# Dashboard
# This page mirrors the first overview idea of the mockups.
# ---------------------------
def build_dashboard_view(self):
    """Build the first overview page with water, calories and quick actions. Partly AI-generated."""
    calorie_status = get_today_calorie_status(self.current_user)
    water_status = get_today_water_status(self.current_user)
    current_weight_log = self.get_current_weight_log()

    hero = ft.Row(
        [
            ft.Container(
                width=96,
                height=96,
                border_radius=8,
                border=ft.border.all(1, self.surface_border_color()),
                content=ft.Icon(ft.Icons.MONITOR_HEART_OUTLINED, size=42),
                alignment=ft.Alignment.CENTER,
            ),
            ft.Column(
                [
                    ft.Text(
                        self.t("welcome_back", name=self.current_user.name),
                        size=34,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        self.t("dashboard_intro"),
                        size=16,
                        color=self.surface_muted_color(),
                    ),
                ],
                spacing=8,
                expand=True,
            ),
        ],
        spacing=20,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    calorie_card = self.build_surface_section(
        self.t("calorie_balance_today"),
        ft.Row(
            [
                ft.Column(
                    [
                        self.build_label_value_row(
                            self.t("calories_eaten"),
                            self.format_amount(calorie_status["intake"], "kcal"),
                        ),
                        self.build_label_value_row(
                            self.t("calories_burned_label"),
                            self.format_amount(calorie_status["burned"], "kcal"),
                        ),
                        self.build_label_value_row(
                            self.t("calorie_balance_label"),
                            self.format_amount(calorie_status["net"], "kcal"),
                        ),
                        self.build_label_value_row(
                            self.t("calorie_goal"),
                            self.format_amount(calorie_status["target"], "kcal"),
                        ),
                    ],
                    spacing=10,
                    expand=1,
                ),
                ft.Container(
                    width=340,
                    content=ft.Column(
                        [
                            ft.ProgressBar(
                                value=(
                                    0
                                    if not calorie_status["target"]
                                    else min(
                                        1,
                                        calorie_status["intake"]
                                        / calorie_status["target"],
                                    )
                                ),
                                color=SEDA_MINT,
                                bgcolor=self.surface_border_color(),
                            ),
                            ft.Text(
                                f"{self.t('remaining_to_goal')}: {self.format_amount(calorie_status['difference'], 'kcal')}",
                                color=self.surface_muted_color(),
                            ),
                        ],
                        spacing=10,
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )

    cards_row = ft.ResponsiveRow(
        [
            ft.Container(
                col={"md": 6},
                content=self.build_surface_section(
                    self.t("water_today"),
                    ft.Column(
                        [
                            ft.Text(
                                self.t(
                                    "water_progress",
                                    intake=water_status["intake"],
                                    target=water_status["target"],
                                ),
                                size=20,
                            ),
                            ft.ProgressBar(
                                value=min(1, (water_status["progress"] or 0) / 100),
                                color=SEDA_MINT,
                                bgcolor=self.surface_border_color(),
                            ),
                            ft.Text(
                                self.t(
                                    "water_to_go",
                                    difference=water_status["difference"],
                                ),
                                color=self.surface_muted_color(),
                            ),
                        ],
                        spacing=12,
                    ),
                ),
            ),
            ft.Container(
                col={"md": 6},
                content=self.build_surface_section(
                    self.t("weight_bmi"),
                    ft.Column(
                        [
                            self.build_label_value_row(
                                self.t("current_weight"),
                                (
                                    self.format_amount(
                                        current_weight_log.weight_in_kg, "kg"
                                    )
                                    if current_weight_log is not None
                                    else self.t("no_weight_logged")
                                ),
                            ),
                            self.build_label_value_row(
                                self.t("bmi"),
                                (
                                    self.format_amount(current_weight_log.bmi)
                                    if current_weight_log is not None
                                    and current_weight_log.bmi is not None
                                    else self.t("bmi_not_available")
                                ),
                            ),
                        ],
                        spacing=12,
                    ),
                ),
            ),
        ],
        run_spacing=16,
        spacing=16,
    )

    quick_actions = self.build_surface_section(
        self.t("quick_actions"),
        ft.ResponsiveRow(
            [
                ft.Container(
                    col={"md": 3},
                    content=ft.FilledButton(
                        self.t("add_water"),
                        icon=ft.Icons.WATER_DROP,
                        style=ft.ButtonStyle(
                            bgcolor=SEDA_MINT,
                            color=ft.Colors.WHITE,
                        ),
                        expand=True,
                        on_click=lambda _: self.navigate("water"),
                    ),
                ),
                ft.Container(
                    col={"md": 3},
                    content=ft.FilledButton(
                        self.t("log_meal"),
                        icon=ft.Icons.RESTAURANT,
                        style=ft.ButtonStyle(
                            bgcolor=SEDA_MINT,
                            color=ft.Colors.WHITE,
                        ),
                        expand=True,
                        on_click=lambda _: self.navigate("nutrition"),
                    ),
                ),
                ft.Container(
                    col={"md": 3},
                    content=ft.FilledButton(
                        self.t("add_activity"),
                        icon=ft.Icons.DIRECTIONS_RUN,
                        style=ft.ButtonStyle(
                            bgcolor=SEDA_MINT,
                            color=ft.Colors.WHITE,
                        ),
                        expand=True,
                        on_click=lambda _: self.navigate("activity"),
                    ),
                ),
                ft.Container(
                    col={"md": 3},
                    content=ft.FilledButton(
                        self.t("go_to_profile"),
                        icon=ft.Icons.PERSON,
                        style=ft.ButtonStyle(
                            bgcolor=SEDA_MINT,
                            color=ft.Colors.WHITE,
                        ),
                        expand=True,
                        on_click=lambda _: self.navigate("profile"),
                    ),
                ),
            ],
            spacing=12,
            run_spacing=12,
        ),
    )

    return ft.Column([hero, calorie_card, cards_row, quick_actions], spacing=20)


# ---------------------------
# Water page
# This page covers the water-related V0.1 tracking flow.
# ---------------------------
def build_water_view(self):
    """Build the water page with status, add-form and entry list. Partly AI-generated."""
    self.refresh_current_user_logs()
    water_status = get_today_water_status(self.current_user)

    amount_field = ft.TextField(
        label=self.t("amount_ml"),
        keyboard_type=ft.KeyboardType.NUMBER,
        expand=True,
    )
    timestamp_field = ft.TextField(
        label=self.t("optional_timestamp"),
        helper=self.t("use_now_when_empty"),
        hint_text=self.timestamp_input_hint(),
        expand=True,
    )

    def submit_water(_):
        """Create one water log from the inline form."""
        try:
            amount = self.parse_required_int(amount_field.value)
            timestamp = self.parse_optional_timestamp(timestamp_field.value)
            self.add_water_log(amount, timestamp)
        except Exception as exc:
            self.show_message(str(exc), error=True)

    status_section = self.build_surface_section(
        self.t("water_status"),
        ft.Column(
            [
                ft.Text(
                    self.t(
                        "water_progress",
                        intake=water_status["intake"],
                        target=water_status["target"],
                    ),
                    size=22,
                ),
                ft.ProgressBar(
                    value=min(1, (water_status["progress"] or 0) / 100),
                    color=SEDA_MINT,
                    bgcolor=self.surface_border_color(),
                ),
                ft.Text(
                    self.t("water_to_go", difference=water_status["difference"]),
                    color=self.surface_muted_color(),
                ),
            ],
            spacing=12,
        ),
    )

    add_section = self.build_surface_section(
        self.t("add_water"),
        ft.Row(
            [
                amount_field,
                timestamp_field,
                ft.FilledButton(
                    self.t("save"),
                    icon=ft.Icons.SAVE,
                    style=self.primary_filled_button_style(),
                    on_click=submit_water,
                ),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.END,
        ),
    )

    water_rows = []
    for water_log in self.sort_logs_desc(self.current_user.water_log_handler.logs):
        water_rows.append(
            ft.Container(
                padding=12,
                border_radius=8,
                bgcolor=self.surface_background_alt_color(),
                border=ft.border.all(1, self.surface_border_color()),
                content=ft.Row(
                    [
                        ft.Text(
                            self.format_amount(water_log.amount_in_ml, "ml"),
                            width=120,
                        ),
                        ft.Text(
                            self.format_timestamp(water_log.timestamp),
                            expand=True,
                            color=self.surface_muted_color(),
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            icon_color=SEDA_RED,
                            on_click=lambda _, log_id=water_log.id: self.open_confirm_dialog(
                                self.t("msg_confirm_delete_entry"),
                                self.t("water_today"),
                                lambda dialog, target_id=log_id: (
                                    self.close_dialog(dialog),
                                    self.delete_water_log(target_id),
                                ),
                            ),
                        ),
                    ]
                ),
            )
        )

    entries_section = self.build_surface_section(
        self.t("last_entries"),
        ft.Column(
            water_rows
            or [ft.Text(self.t("no_water_logs"), color=self.surface_muted_color())],
            spacing=10,
        ),
    )

    return ft.Column([status_section, add_section, entries_section], spacing=20)


# ---------------------------
# Activity page
# This page covers add/show/update/delete for burned-calorie entries.
# ---------------------------
def build_activity_view(self):
    """Build the activity page with add form and editable entries. Partly AI-generated."""
    self.refresh_current_user_logs()

    name_field = ft.TextField(label=self.t("activity_name"), expand=True)
    calories_field = ft.TextField(
        label=self.t("calories_burned"),
        keyboard_type=ft.KeyboardType.NUMBER,
        width=180,
    )
    duration_field = ft.TextField(
        label=self.t("duration_minutes"),
        keyboard_type=ft.KeyboardType.NUMBER,
        width=180,
    )
    timestamp_field = ft.TextField(
        label=self.t("optional_timestamp"),
        helper=self.t("use_now_when_empty"),
        hint_text=self.timestamp_input_hint(),
        expand=True,
    )

    def submit_activity(_):
        """Create one activity entry from the inline desktop form."""
        try:
            activity_name = name_field.value.strip()
            calories = self.parse_required_float(calories_field.value)
            duration = self.parse_optional_float(duration_field.value)
            timestamp = self.parse_optional_timestamp(timestamp_field.value)
            self.add_activity_log(activity_name, calories, duration, timestamp)
        except Exception as exc:
            self.show_message(str(exc), error=True)

    add_section = self.build_surface_section(
        self.t("add_activity"),
        ft.Column(
            [
                ft.Row([name_field, calories_field, duration_field], spacing=12),
                ft.Row(
                    [
                        timestamp_field,
                        ft.FilledButton(
                            self.t("save"),
                            icon=ft.Icons.SAVE,
                            style=self.primary_filled_button_style(),
                            on_click=submit_activity,
                        ),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                ),
            ],
            spacing=12,
        ),
        subtitle=self.t("activity_copy"),
    )

    activity_rows = []
    for activity_log in self.sort_logs_desc(
        self.current_user.activity_log_handler.logs
    ):
        activity_rows.append(
            ft.Container(
                padding=12,
                border_radius=8,
                bgcolor=self.surface_background_alt_color(),
                border=ft.border.all(1, self.surface_border_color()),
                content=ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(
                                    activity_log.activity_name,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    f"{self.format_amount(activity_log.calories_burned, 'kcal')} | "
                                    f"{self.format_amount(activity_log.activity_value, 'minutes')}",
                                    color=self.surface_muted_color(),
                                ),
                            ],
                            spacing=4,
                            expand=True,
                        ),
                        ft.Text(
                            self.format_timestamp(activity_log.timestamp),
                            color=self.surface_muted_color(),
                            width=170,
                        ),
                        ft.IconButton(
                            ft.Icons.EDIT_OUTLINED,
                            icon_color=SEDA_MINT,
                            on_click=lambda _, log=activity_log: self.open_activity_edit_dialog(
                                log
                            ),
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            icon_color=SEDA_RED,
                            on_click=lambda _, log_id=activity_log.id: self.open_confirm_dialog(
                                self.t("msg_confirm_delete_entry"),
                                activity_log.activity_name,
                                lambda dialog, target_id=log_id: (
                                    self.close_dialog(dialog),
                                    self.delete_activity_log(target_id),
                                ),
                            ),
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )
        )

    entries_section = self.build_surface_section(
        self.t("activity_logs"),
        ft.Column(
            activity_rows
            or [ft.Text(self.t("no_activity_logs"), color=self.surface_muted_color())],
            spacing=10,
        ),
    )

    return ft.Column([add_section, entries_section], spacing=20)


# ---------------------------
# Nutrition page
# This page brings together search, meal templates and meal logs.
# ---------------------------
def build_nutrition_view(self):
    """Build the nutrition page with the full meal-management workflow. Partly AI-generated."""
    self.refresh_current_user_logs()
    calorie_status = get_today_calorie_status(self.current_user)

    search_field = ft.TextField(
        label=self.t("search_term"),
        value=self.food_search_term,
        expand=True,
        on_change=lambda e: setattr(self, "food_search_term", e.control.value),
    )

    calorie_section = self.build_surface_section(
        self.t("calorie_status_today"),
        ft.Row(
            [
                self.build_metric_chip(
                    self.t("calories_eaten"),
                    self.format_amount(calorie_status["intake"], "kcal"),
                    accent=SEDA_MINT,
                ),
                self.build_metric_chip(
                    self.t("calories_burned_label"),
                    self.format_amount(calorie_status["burned"], "kcal"),
                    accent=SEDA_YELLOW,
                ),
                self.build_metric_chip(
                    self.t("calorie_balance_label"),
                    self.format_amount(calorie_status["net"], "kcal"),
                    accent=self.primary_text_color(),
                ),
                self.build_metric_chip(
                    self.t("calorie_goal"),
                    self.format_amount(calorie_status["target"], "kcal"),
                    accent=SEDA_MINT,
                ),
                self.build_metric_chip(
                    self.t("remaining_to_goal"),
                    self.format_amount(calorie_status["difference"], "kcal"),
                    accent=SEDA_YELLOW,
                ),
            ],
            wrap=True,
            spacing=12,
        ),
    )

    search_rows = []
    for food_row in self.food_search_results:
        search_rows.append(
            ft.Container(
                padding=12,
                border_radius=8,
                bgcolor=self.surface_background_alt_color(),
                border=ft.border.all(1, self.surface_border_color()),
                content=ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(
                                    self.get_food_name(food_row),
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    f"{self.format_amount(food_row['kcal'], 'kcal')} / 100 {food_row['unit_type']}",
                                    color=self.surface_muted_color(),
                                ),
                            ],
                            spacing=4,
                            expand=True,
                        ),
                        ft.FilledButton(
                            self.t("consume"),
                            style=self.primary_filled_button_style(),
                            on_click=lambda _, row=food_row: self.open_food_amount_dialog(
                                row, "consume"
                            ),
                        ),
                        ft.OutlinedButton(
                            self.t("add_to_template"),
                            on_click=lambda _, row=food_row: self.open_food_amount_dialog(
                                row, "template"
                            ),
                        ),
                    ],
                    spacing=12,
                ),
            )
        )

    search_section = self.build_surface_section(
        self.t("food_search"),
        ft.Column(
            [
                ft.Text(self.t("food_search_copy"), color=self.surface_muted_color()),
                ft.Row(
                    [
                        search_field,
                        ft.FilledButton(
                            self.t("search"),
                            icon=ft.Icons.SEARCH,
                            style=self.primary_filled_button_style(),
                            on_click=lambda _: self.search_foods(),
                        ),
                    ],
                    spacing=12,
                ),
                ft.Column(
                    search_rows
                    or [
                        ft.Text(
                            self.t("no_food_results"),
                            color=self.surface_muted_color(),
                        )
                    ],
                    spacing=10,
                ),
            ],
            spacing=12,
        ),
    )

    builder_name_field = ft.TextField(
        label=self.t("template_name"),
        value=self.meal_builder_name,
        on_change=lambda e: setattr(self, "meal_builder_name", e.control.value),
    )

    builder_rows = []
    for index, food_item in enumerate(self.meal_builder_items):
        builder_rows.append(
            ft.Container(
                padding=12,
                border_radius=8,
                bgcolor=self.surface_background_alt_color(),
                border=ft.border.all(1, self.surface_border_color()),
                content=ft.Row(
                    [
                        ft.Text(
                            self.get_food_item_display_name(food_item), expand=True
                        ),
                        ft.Text(
                            self.format_amount(food_item.amount, food_item.unit_type),
                            width=110,
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            icon_color=SEDA_RED,
                            on_click=lambda _, item_index=index: (
                                self.meal_builder_items.pop(item_index),
                                self.render(),
                            ),
                        ),
                    ]
                ),
            )
        )

    builder_section = self.build_surface_section(
        self.t("meal_template_builder"),
        ft.Column(
            [
                ft.Text(self.t("builder_copy"), color=self.surface_muted_color()),
                builder_name_field,
                ft.Text(self.t("selected_items"), weight=ft.FontWeight.BOLD),
                ft.Column(
                    builder_rows
                    or [
                        ft.Text(
                            self.t("builder_empty"),
                            color=self.surface_muted_color(),
                        )
                    ],
                    spacing=10,
                ),
                ft.Row(
                    [
                        ft.FilledButton(
                            self.t(
                                "update_template"
                                if self.editing_meal_template_id is not None
                                else "save_template"
                            ),
                            icon=ft.Icons.SAVE,
                            style=self.primary_filled_button_style(),
                            on_click=lambda _: self.handle_save_meal_template(),
                        ),
                        ft.OutlinedButton(
                            self.t("reset_builder"),
                            icon=ft.Icons.RESTART_ALT,
                            on_click=lambda _: self.handle_reset_builder(),
                        ),
                    ],
                    spacing=12,
                ),
            ],
            spacing=12,
        ),
    )

    template_rows = []
    for meal in self.get_meal_templates():
        template_rows.append(
            ft.Container(
                padding=12,
                border_radius=8,
                bgcolor=self.surface_background_alt_color(),
                border=ft.border.all(1, self.surface_border_color()),
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    self.get_meal_display_name(meal),
                                    weight=ft.FontWeight.BOLD,
                                    expand=True,
                                ),
                                ft.Text(
                                    self.format_amount(meal.calories, "kcal"),
                                    color=self.surface_muted_color(),
                                ),
                            ]
                        ),
                        ft.Text(
                            ", ".join(
                                [
                                    f"{self.get_food_item_display_name(item)} "
                                    f"({self.format_amount(item.amount, item.unit_type)})"
                                    for item in meal.food_items
                                ]
                            ),
                            color=self.surface_muted_color(),
                        ),
                        ft.Row(
                            [
                                ft.FilledButton(
                                    self.t("log_meal"),
                                    icon=ft.Icons.ADD_TASK,
                                    style=self.primary_filled_button_style(),
                                    on_click=lambda _, selected_meal=meal: self.open_meal_log_dialog(
                                        meal=selected_meal
                                    ),
                                ),
                                ft.OutlinedButton(
                                    self.t("edit_template"),
                                    icon=ft.Icons.EDIT,
                                    on_click=lambda _, selected_meal=meal: (
                                        self.start_meal_template_edit(selected_meal)
                                    ),
                                ),
                                ft.OutlinedButton(
                                    self.t("delete"),
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    style=ft.ButtonStyle(color=SEDA_RED),
                                    on_click=lambda _, selected_meal=meal: self.open_confirm_dialog(
                                        self.t("msg_confirm_delete_template"),
                                        self.get_meal_display_name(selected_meal),
                                        lambda dialog, meal_id=selected_meal.id: (
                                            self.close_dialog(dialog),
                                            self.delete_meal_template(meal_id),
                                        ),
                                    ),
                                ),
                            ],
                            spacing=10,
                            wrap=True,
                        ),
                    ],
                    spacing=10,
                ),
            )
        )

    templates_section = self.build_surface_section(
        self.t("meal_templates"),
        ft.Column(
            template_rows
            or [ft.Text(self.t("no_meal_templates"), color=self.surface_muted_color())],
            spacing=10,
        ),
    )

    meal_log_rows = []
    for meal_log in self.sort_logs_desc(self.current_user.meal_log_handler.logs):
        enriched_log = self.enrich_meal_log(meal_log)
        meal_log_rows.append(
            ft.Container(
                padding=12,
                border_radius=8,
                bgcolor=self.surface_background_alt_color(),
                border=ft.border.all(1, self.surface_border_color()),
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text(
                                            self.get_meal_display_name(
                                                enriched_log.meal
                                            ),
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(
                                            f"{self.format_amount(enriched_log.amount, enriched_log.unit_type)} | "
                                            f"{self.format_amount(enriched_log.calories, 'kcal')}",
                                            color=self.surface_muted_color(),
                                        ),
                                    ],
                                    spacing=4,
                                    expand=True,
                                ),
                                ft.Text(
                                    self.format_timestamp(meal_log.timestamp),
                                    color=self.surface_muted_color(),
                                ),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.FilledButton(
                                    self.t("show_details"),
                                    icon=ft.Icons.ARTICLE_OUTLINED,
                                    style=self.primary_filled_button_style(),
                                    on_click=lambda _, log=enriched_log: self.open_meal_log_details_dialog(
                                        log
                                    ),
                                ),
                                ft.OutlinedButton(
                                    self.t("edit_log"),
                                    icon=ft.Icons.EDIT,
                                    on_click=lambda _, log=meal_log: self.open_meal_log_dialog(
                                        existing_log=log
                                    ),
                                ),
                                ft.OutlinedButton(
                                    self.t("delete"),
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    style=ft.ButtonStyle(color=SEDA_RED),
                                    on_click=lambda _, log_id=meal_log.id: self.open_confirm_dialog(
                                        self.t("msg_confirm_delete_entry"),
                                        self.get_meal_display_name(enriched_log.meal),
                                        lambda dialog, target_id=log_id: (
                                            self.close_dialog(dialog),
                                            self.delete_meal_log(target_id),
                                        ),
                                    ),
                                ),
                            ],
                            spacing=10,
                            wrap=True,
                        ),
                    ],
                    spacing=10,
                ),
            )
        )

    meal_logs_section = self.build_surface_section(
        self.t("meal_logs"),
        ft.Column(
            meal_log_rows
            or [ft.Text(self.t("no_meal_logs"), color=self.surface_muted_color())],
            spacing=10,
        ),
    )

    return ft.Column(
        [
            calorie_section,
            search_section,
            builder_section,
            templates_section,
            meal_logs_section,
        ],
        spacing=20,
    )


def handle_save_meal_template(self):
    """Wrap meal-template saving so UI errors end up in the footer. Partly AI-generated."""
    try:
        self.save_meal_template()
    except Exception as exc:
        self.show_message(str(exc), error=True)


def handle_reset_builder(self):
    """Reset the meal-template builder and show a small confirmation. Partly AI-generated."""
    self.reset_meal_builder()
    self.show_message(self.t("msg_builder_reset"))
    self.render()


# ---------------------------
# Profile page
# This page holds biometrical data, weight logs, settings and account actions.
# ---------------------------
def build_profile_view(self):
    """Build the profile page with inline forms and calculated values. Partly AI-generated."""
    self.refresh_current_user_logs()
    calorie_status = get_today_calorie_status(self.current_user)
    current_weight_log = self.get_current_weight_log()

    name_field = ft.TextField(label=self.t("name"), value=self.current_user.name)
    birthdate_field = ft.TextField(
        label=self.t("birthdate"),
        value=self.format_birthdate(self.current_user.birthdate),
        hint_text=self.birthdate_input_hint(),
    )
    height_field = ft.TextField(
        label=self.t("height_cm"),
        value=str(self.current_user.height_in_cm),
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    gender_dropdown = ft.Dropdown(
        label=self.t("gender"),
        value=self.current_user.gender,
        options=[
            ft.DropdownOption(key="m", text=self.t("gender_m")),
            ft.DropdownOption(key="f", text=self.t("gender_f")),
            ft.DropdownOption(key="d", text=self.t("gender_d")),
        ],
    )
    fitness_dropdown = ft.Dropdown(
        label=self.t("fitness_level"),
        value=self.current_user.fitness_lvl,
        options=[
            ft.DropdownOption(key="beginner", text=self.t("fitness_beginner")),
            ft.DropdownOption(key="intermediate", text=self.t("fitness_intermediate")),
            ft.DropdownOption(key="advanced", text=self.t("fitness_advanced")),
        ],
    )

    def submit_profile(_):
        """Validate and persist personal data edits."""
        try:
            self.save_profile(
                name_field.value.strip(),
                self.parse_birthdate(birthdate_field.value),
                self.parse_required_int(height_field.value),
                gender_dropdown.value,
                fitness_dropdown.value,
            )
        except Exception as exc:
            self.show_message(str(exc), error=True)

    personal_section = self.build_surface_section(
        self.t("personal_data"),
        ft.Column(
            [
                ft.Row([name_field, birthdate_field], spacing=12),
                ft.Row([height_field, gender_dropdown, fitness_dropdown], spacing=12),
                ft.Row(
                    [
                        ft.Container(expand=True),
                        ft.FilledButton(
                            self.t("save"),
                            icon=ft.Icons.SAVE,
                            style=self.primary_filled_button_style(),
                            on_click=submit_profile,
                        ),
                    ]
                ),
            ],
            spacing=12,
        ),
    )

    weight_field = ft.TextField(
        label=self.t("weight_kg"),
        keyboard_type=ft.KeyboardType.NUMBER,
        width=200,
    )
    weight_timestamp_field = ft.TextField(
        label=self.t("optional_timestamp"),
        helper=self.t("use_now_when_empty"),
        hint_text=self.timestamp_input_hint(),
        expand=True,
    )

    def submit_weight(_):
        """Create one new weight log from the profile page."""
        try:
            weight = self.parse_required_float(weight_field.value)
            timestamp = self.parse_optional_timestamp(weight_timestamp_field.value)
            self.add_weight_log(weight, timestamp)
        except Exception as exc:
            self.show_message(str(exc), error=True)

    weight_rows = []
    for weight_log in self.sort_logs_desc(self.current_user.weight_log_handler.logs):
        weight_rows.append(
            ft.Container(
                padding=12,
                border_radius=8,
                bgcolor=self.surface_background_alt_color(),
                border=ft.border.all(1, self.surface_border_color()),
                content=ft.Row(
                    [
                        ft.Text(
                            self.format_amount(weight_log.weight_in_kg, "kg"),
                            width=110,
                        ),
                        ft.Text(
                            self.format_amount(weight_log.bmi),
                            width=100,
                            color=self.surface_muted_color(),
                        ),
                        ft.Text(
                            self.format_timestamp(weight_log.timestamp),
                            expand=True,
                            color=self.surface_muted_color(),
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            icon_color=SEDA_RED,
                            on_click=lambda _, log_id=weight_log.id: self.open_confirm_dialog(
                                self.t("msg_confirm_delete_entry"),
                                self.t("weight_bmi"),
                                lambda dialog, target_id=log_id: (
                                    self.close_dialog(dialog),
                                    self.delete_weight_log(target_id),
                                ),
                            ),
                        ),
                    ]
                ),
            )
        )

    body_section = self.build_surface_section(
        self.t("body_statistics"),
        ft.Column(
            [
                self.build_label_value_row(
                    self.t("latest_weight"),
                    (
                        self.format_amount(current_weight_log.weight_in_kg, "kg")
                        if current_weight_log is not None
                        else self.t("no_weight_logged")
                    ),
                ),
                self.build_label_value_row(
                    self.t("bmi"),
                    (
                        self.format_amount(current_weight_log.bmi)
                        if current_weight_log is not None
                        and current_weight_log.bmi is not None
                        else self.t("bmi_not_available")
                    ),
                ),
                ft.Row(
                    [
                        weight_field,
                        weight_timestamp_field,
                        ft.FilledButton(
                            self.t("add_weight_log"),
                            icon=ft.Icons.MONITOR_WEIGHT_OUTLINED,
                            style=self.primary_filled_button_style(),
                            on_click=submit_weight,
                        ),
                    ],
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                ),
                ft.Text(self.t("weight_logs"), weight=ft.FontWeight.BOLD),
                ft.Column(
                    weight_rows
                    or [
                        ft.Text(
                            self.t("no_weight_logs"),
                            color=self.surface_muted_color(),
                        )
                    ],
                    spacing=10,
                ),
            ],
            spacing=12,
        ),
    )

    calculated_section = self.build_surface_section(
        self.t("calculated_values"),
        ft.Column(
            [
                self.build_label_value_row(
                    self.t("daily_calorie_target"),
                    self.format_amount(calorie_status["target"], "kcal"),
                ),
                self.build_label_value_row(
                    self.t("daily_water_target"),
                    self.format_amount(self.current_user.daily_water_target, "ml"),
                ),
                self.build_label_value_row(
                    self.t("bmi"),
                    (
                        self.format_amount(current_weight_log.bmi)
                        if current_weight_log is not None
                        and current_weight_log.bmi is not None
                        else self.t("bmi_not_available")
                    ),
                ),
            ],
            spacing=10,
        ),
    )

    language_dropdown = ft.Dropdown(
        label=self.t("language"),
        value=self.current_language,
        options=[
            ft.DropdownOption(key="en", text=self.t("language_en")),
            ft.DropdownOption(key="de", text=self.t("language_de")),
        ],
        on_select=lambda e: self.change_language(e.control.value),
        width=220,
    )

    settings_section = self.build_surface_section(
        self.t("application_settings"),
        ft.Column([language_dropdown], spacing=12),
    )

    account_section = self.build_surface_section(
        self.t("delete_account"),
        ft.Column(
            [
                ft.Text(
                    self.t("delete_account_copy"), color=self.surface_muted_color()
                ),
                ft.Row(
                    [
                        ft.FilledButton(
                            self.t("delete_account"),
                            icon=ft.Icons.DELETE_FOREVER_OUTLINED,
                            style=ft.ButtonStyle(bgcolor=SEDA_RED),
                            on_click=lambda _: self.open_confirm_dialog(
                                self.t("delete_account_confirm_title"),
                                self.t(
                                    "delete_account_confirm_copy",
                                    name=self.current_user.name,
                                ),
                                lambda dialog: (
                                    self.close_dialog(dialog),
                                    self.delete_current_user(),
                                ),
                            ),
                        )
                    ]
                ),
            ],
            spacing=12,
        ),
    )

    return ft.Column(
        [
            personal_section,
            body_section,
            calculated_section,
            settings_section,
            account_section,
        ],
        spacing=20,
    )


# ---------------------------
# About page
# This keeps one simple place for app context and status information.
# ---------------------------
def build_about_view(self):
    """Build a lightweight about page connected to the live app state. Partly AI-generated."""
    feature_section = self.build_surface_section(
        self.t("feature_overview"),
        ft.Text(self.t("feature_overview_copy"), color=self.surface_muted_color()),
    )

    about_section = self.build_surface_section(
        self.t("about_title"),
        ft.Column(
            [
                ft.Text(self.t("about_copy"), color=self.surface_muted_color()),
                self.build_label_value_row(
                    self.t("database_status"),
                    self.t("database_ready"),
                ),
                self.build_label_value_row(
                    self.t("developers_label"),
                    DEVS,
                ),
            ],
            spacing=10,
        ),
    )

    license_section = self.build_surface_section(
        self.t("license_title"),
        ft.Column(
            [
                ft.Text(self.t("license_copy"), color=self.surface_muted_color()),
                self.build_label_value_row(
                    self.t("license_name_label"),
                    self.t("license_name_value"),
                ),
                self.build_label_value_row(
                    self.t("license_spdx_label"),
                    "GPL-3.0-or-later",
                ),
                self.build_label_value_row(
                    self.t("license_copyright_label"),
                    self.t("license_copyright_value"),
                ),
                self.build_label_value_row(
                    self.t("license_file_label"),
                    "LICENSE.md",
                ),
                ft.FilledButton(
                    self.t("show_full_license"),
                    icon=ft.Icons.GAVEL_OUTLINED,
                    style=self.primary_filled_button_style(),
                    on_click=self.open_license_dialog,
                ),
            ],
            spacing=10,
        ),
    )

    return ft.Column([about_section, feature_section, license_section], spacing=20)
