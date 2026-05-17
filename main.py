# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Main entry point for SEDA."""

import sys
import os

from controllers.cli_controller import main as cli_main
from ui.cli_view import show_welcome, show_license_long


def run_interactive_launcher():
    """Run the CLI/GUI chooser in an interactive terminal. AI-generated."""
    show_welcome()
    ux = input("""Do you want to run the CLI or GUI? Enter:
        'c' for CLI
        'g' for GUI
        'l' for showing the license\n""").lower()
    if ux == "g":
        from ui.gui import run_gui_app

        run_gui_app()
    elif ux == "c":
        cli_main()
    elif ux == "l":
        show_license_long()
    else:
        print("Input invalid. Please enter 'g/c/l'. Exiting now...")
        sys.exit(1)


def main():
    """Start SEDA in GUI or interactive launcher mode depending on the environment. AI-generated."""
    if "--cli" in sys.argv:
        cli_main()
        return

    if "--license" in sys.argv:
        show_welcome()
        show_license_long()
        return

    if (
        "--gui" in sys.argv
        or os.getenv("FLET_APP_STORAGE_DATA") is not None
        or sys.stdin is None
        or not sys.stdin.isatty()
    ):
        from ui.gui import run_gui_app

        run_gui_app()
        return

    run_interactive_launcher()


if __name__ == "__main__":
    main()
