# SEDA Design System Notes

> This document is partly AI-generated.
> AI-generated as a lightweight style convention for future GUI work.

This file captures visual and interaction rules that should stay consistent across GUI changes.

## Core Goals

- Keep the interface readable on both standard and ultra-wide screens
- Reduce visual noise by reusing the same spacing, colors, and interaction patterns
- Make AI-generated or refactored GUI code easier to align with one shared convention

## Layout

- Define a maximum content width for main page content
- Keep cards in the same row at equal height where the layout allows it
- Use consistent spacing between sections, cards, and controls
- Recheck mobile responsiveness after layout-heavy changes

## Spacing

- Use the same inner padding inside cards of the same type
- Use standard margin values instead of per-view one-off spacing

## Colors

- Use one shared color palette across the GUI
- Avoid accidental blue buttons if the intended accent is turquoise
- Use clear semantic colors:
  - static values: mint
  - dynamic values: yellow
  - warnings or overshooting: red

Current project colors taken from the GUI code:

Background and surface colors:
- Dark page background: `#111315`
- Dark surface background: `#171B21`
- Dark alternate surface: `#1C2626`
- Dark surface border: `#3E4B5D`
- Light page background: `#EEF2F5`
- Light surface background: `#FFFFFF`
- Light alternate surface: `#F4F9F8`
- Light surface border: `#C9D5DE`

Text colors:
- Dark muted text: `#AAB5C3`
- Light muted text: `#5E6B78`
- Light primary text: `#18212B`

Signature colors:
- `seda-mint`: `#00A69C`
- `seda-yellow`: `#EBE46E`
- `seda-red`: `#EB6E85`

## Buttons and Inputs

- Use consistent button styles across pages
- Keep hover states visually consistent
- Use consistent border radii for buttons, cards, and inputs
- Prefer structured input controls over fragile free-text input where possible

## Typography

- Define consistent font sizes for headings, labels, values, and helper text
- Build a clear visual hierarchy so important values stand out immediately

## Icons

- Use a consistent icon language across related features
- Align the `Nutrition` and `Log Meal` icons stylistically

## Motion

- If hover or transition effects are used, keep them subtle and consistent

## Usage Rule

- Use `docs/gui_backlog.md` for open UI tasks
- Use this file for stable rules that should remain true across future GUI work
