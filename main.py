# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.

"""Main entry point for SEDA."""

import sys

from model.controller import main as cli_main
from ui.cli_view import show_welcome, show_license_long

show_welcome()

if __name__ == "__main__":
    ux = input("""Do you want to run the CLI or GUI? Enter:
        'c' for CLI
        'g' for GUI
        'l' for showing the license\n""").lower()
    if ux == "g":
        from ui.ui import ft, main as gui_main

        ft.app(target=gui_main)
    elif ux == "c":
        cli_main()
    elif ux == "l":
        show_license_long()
    else:
        print("Input invalid. Please enter 'y/n/l'. Exiting now...")
        sys.exit(1)
