# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Tobias Mignat & Sabine Steverding
# See LICENSE.md for the full license text.
"""Utility helpers for paginated CLI output."""


def paginator(text, lines_per_page=30, input_fn=input, output_fn=print):
    """Show long text in smaller CLI pages. AI-generated."""
    lines = text.splitlines()

    if not lines:
        output_fn("")
        return

    for start in range(0, len(lines), lines_per_page):
        block = lines[start : start + lines_per_page]
        output_fn("\n".join(block))

        has_next_page = start + lines_per_page < len(lines)
        if has_next_page:
            input_fn("Press Enter to continue...")
