# SEDA GUI Backlog

> This document is partly AI-generated. The findings are written by the DEVS.

This file collects GUI, UX, layout, branding, and product-facing improvement ideas for the desktop application.

Use this file for:
- GUI and UX improvements
- navigation and layout changes
- feature ideas with a strong UI impact
- visual consistency work
- follow-up tasks that depend on backend changes

Do not use this file for:
- purely technical debt without user-facing impact
- low-level refactoring tasks
- non-UI architecture cleanup

## Now

### GUI Structure

- [ ] Add language selection to the login screen
- [ ] Persist language choice and dark mode
- [ ] Define a maximum content width
  Reason: the current GUI looks too stretched on 2560 px screens
- [ ] Move `Water Tracker` before `Nutrition` in the header
- [ ] Move `Weight Logs / BMI / Statistics` out of `Profile` into a dedicated tab
- [ ] Add language selection as a graphical button next to the dark mode button
- [x] Replace accidental blue default buttons with `seda-mint`

### Forms and Inputs

- [ ] Replace free-text date and time inputs where appropriate
- [ ] Add a date picker for date fields
- [ ] Add a time picker for time fields
- [ ] Use dropdowns or scroll-wheel style controls where they improve input safety
- [ ] Align `Weight in kg` and `Optional timestamp` more cleanly in `Body Statistics & Physics`
- [ ] Remove the helper text `Leave empty to use the current time`

### Profile and Weight Flow

- [ ] Ask for the first weight during profile creation
  Reason: this should automatically create the first `WeightLog`

### Dashboard

- [ ] Make the `Water Tracker` and `Weight & BMI` cards the same height
- [ ] Improve the presentation of the `Calorie Balance`
- [ ] Add status bars to the calorie balance area
- [ ] Make the calorie balance more visually consistent
- [ ] Make the calorie balance easier to understand at a glance
- [ ] Highlight overshooting more clearly with color
- [ ] Separate target and current values more clearly

### Nutrition UX

- [ ] Consider replacing `Nutrition` with a more concise or memorable label
- [ ] Show food stats on click in the search flow
- [ ] Trigger search with `Enter`
  Note: mobile should still keep the button as the safe fallback
- [ ] Clear the search bar automatically after `Consume` or `Add to Template`
- [ ] Add an `X` button inside the search field for quick clearing
- [ ] Return focus to the search field automatically after actions
- [ ] Do not store directly consumed single foods as meal templates
  Source: moved from `BUG-016` in `bug_tracker.py`
- [ ] Align the `Nutrition` icon and the `Log Meal` icon stylistically

### Branding and Copy

- [ ] Replace the current logo in the header placeholder area
- [ ] Replace the current logo on the create-account page
- [ ] Replace the current logo on the login screen
- [ ] Replace the current about-page text:
  `This desktop GUI is the first interactive workbench for the SEDA learning project`
- [ ] Write a short, clearer about-page description
- [ ] Explain what the app does
- [ ] Explain what the app is for
- [ ] Present the project with real ambition instead of framing it only as a learning exercise

## Next

### Nutrition Display

- [ ] Make calorie presentation more intuitive
- [ ] Add icons where they improve scanning
- [ ] Group related values more clearly
- [ ] Build a stronger visual hierarchy
- [ ] Highlight the most important values more clearly
- [ ] Show calories without decimal places
  Note: internal calculations should remain precise
- [ ] Round gram values to sensible display precision where helpful

### Search Enhancements

- [ ] Cache recent search terms and show them as suggestions
- [ ] Add autocomplete to the food search

### Guidance

- [ ] Evaluate whether a lightweight guided setup for the first `WeightLog` is worthwhile
  Trade-off: better UX, but more implementation effort

## Later

### Backend Dependencies With GUI Impact

- [ ] Delete meal templates reliably when deleting a user account
  Options:
  - [ ] reset `database.db` cleanly
  - [ ] or reliably cascade-delete all dependent table entries
- [ ] Add target values for nutrients
- [ ] Build an activity database for multiple activity types
- [ ] Check the database structure for orphaned entries

### General Design Follow-up

- [ ] Test mobile responsiveness
- [ ] Recheck consistent card spacing across pages

## Alternatives and Open Questions

- [ ] Alternative to asking for weight during profile creation:
  show a placeholder such as `Please create your first WeightLog`
  Comment: likely weaker than collecting the weight during onboarding
- [ ] Alternative to asking for weight during profile creation:
  use a guided first `WeightLog` tutorial
  Comment: elegant, but more complex
