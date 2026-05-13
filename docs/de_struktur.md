# Projektstruktur (ai-generiert)

> AI-updated für den aktuellen V0.5-Projektstand.

> Diese Datei beschreibt den aktuellen Aufbau des Workspaces und soll als einfache Orientierung für das Projekt dienen.

## Kurzüberblick

SEDA ist aktuell ein Python-Projekt mit mehreren aktiven Hauptbereichen:

- Fachlogik in `model/`
- Benutzeroberflächen in `ui/`
- Daten in `data/`
- Tests in `tests/`
- Dokumentation in `docs/`

Zusätzlich gibt es Hilfsdateien, ältere Experimente, Release-Unterordner und einige Legacy- oder Utility-Dateien, die nicht direkt zum Kernablauf gehören.

## Ordner im Projekt

### `model/`
Hier liegt die eigentliche Anwendungslogik.

Wichtige Dateien:
- `class_user.py`: zentrale `User`-Klasse mit Berechnungen für Alter, Wasserziel, BMI und Kalorienwerte
- `classes_log.py`: Log-Klassen und Handler für Wasser, Gewicht, Mahlzeiten und Aktivitäten
- `classes_food.py`: Domänenklassen für `Food`, `Meal`, `BigSeven` und `NutrientSummary`
- `database.py`: SQLite-Zugriff, Tabellenaufbau und Datenbankmethoden für User, Wasserlogs, Gewichtslogs, Aktivitätslogs, Food-Logs, Mahlzeiten und Meal-Items
- `controller.py`: CLI-Steuerung und Verbindung zwischen Eingaben, Logik, externer Food-DB und Hauptdatenbank
- `open_food_api.py`: experimentelle Anbindung an Open Food Facts für Suchen per Barcode oder Produktname, aktuell nicht der zentrale Suchpfad

### `ui/`
Dieser Ordner enthält alles rund um die Benutzeroberfläche.

Wichtige Dateien:
- `gui.py`: grafische Oberfläche mit Flet
- `gui copy.py`: ältere oder parallele GUI-Arbeitskopie
- `cli_view.py`: Ein- und Ausgaben für die Kommandozeile
- `translations.py`: Sprachtexte für die GUI in Deutsch und Englisch

### `data/`
Hier liegen Projektdateien mit echten Nutzdaten.

Aktuell:
- `database.db`: die SQLite-Datenbank des Projekts
- `bls_foods.sqlite`: separate Lebensmitteldatenbank, die in `model/database.py` über `FoodDatabase` verwendet wird

### `tests/`
Hier liegen automatisierte Tests.

Aktuell:
- `test_user_class.py`: Tests für die `User`-Klasse
- `test_log_classes.py`: Tests für Log-Klassen und Log-Handler
- `test_food_classes.py`: Tests für `Food`, `Meal` und Nährwertlogik
- `test_cli_view.py`: Tests für CLI-View-Funktionen
- `test_database.py`: Tests für Datenbankfunktionen
- `test.db`: zusätzliche Testdatenbank

### `test_db/`
Dieser Pfad ist für isolierte temporäre Testdatenbanken vorgesehen.

Er wird in `tests/test_database.py` und `utils/test_bine.py` als Zielpfad verwendet, ist aber aktuell kein regulär versionierter Standardordner im Repository.
Die Tests erzeugen dort bei Bedarf temporäre `.db`-Dateien.

### `docs/`
Hier liegt die Projektdokumentation.

Aktuell:
- `de_struktur.md`: deutsche Beschreibung der Projektstruktur
- `en_structur.md`: englische Version der Strukturübersicht
- `gui_backlog.md`: GUI-, UX- und produktnahe Aufgabenliste
- `design_system.md`: schlanke Style- und Layout-Konventionen für die GUI
- `v0.1/`: ältere exportierte Diagramme aus einer früheren Projektphase
- `v0.5/`: freier Release-Ordner für Material der aktuellen Version
- mehrere exportierte Diagramme als `.png`
- `Anforderungsanalyse Tabelle.ods`: begleitende Analyse-Dokumentation

### `utils/`
Hier liegen Hilfsdateien, Einzeltests oder ältere Zusatzskripte.

Beispiele:
- `paginator.py`: Hilfsfunktion für seitenweise CLI-Ausgabe, aktuell für lange Lizenztexte genutzt
- `test_bine.py`: zusätzliche entwicklungsnahe Datenbanktests
- aktuell liegt hier vor allem Hilfs- und Experimentiermaterial, kein zentraler Runtime-Code mehr

Dieser Ordner wirkt im Moment wie ein Sammelbereich für Zwischenstände oder ergänzende Werkzeuge.

### `legacy/`
Hier liegt älterer Code, der nicht mehr zum Hauptpfad gehört, aber noch aufbewahrt wird.

Aktuell:
- `bine_cli_main.py`
- `cli_controller.py`
- `theme_utils.py`
- `tobi_classes.py`
- `ui_german.py`
- `ui_discardable.py`
- `ui_v0.1.py`

### `BLS_4_0_2025_DE/`
Hier liegt Material rund um die externe BLS-Lebensmitteldatenbasis.

Aktuell:
- Excel-Dateien und PDF-Dokumentation zur BLS-Quelle
- `bls_foods.sqlite`: eine weitere SQLite-Version der Lebensmitteldaten
- `import_bls_to_sqlite.py`: Importskript für diese Datenbasis

Dieser Ordner wirkt wie Daten- und Import-Arbeitsmaterial und gehört nicht zum normalen Laufzeitpfad der App.

### `Beispiele/`
Hier liegen Lern-, Tutorial- und Experimentdateien.

Aktuell:
- verschiedene kleine Python-Beispiele
- `flet_tutorial/` mit mehreren Flet-Lernskripten

Dieser Ordner gehört nicht zum eigentlichen App-Produktionspfad, ist aber für das Lernprojekt nachvollziehbar Teil des Repositories.

## Wichtige Dateien im Hauptordner

### `main.py`
Das ist der Einstiegspunkt des Programms.

Aktuell:
- fragt ab, ob die GUI oder die CLI gestartet werden soll
- zeigt optional die Lizenz an
- startet bei `g` die Flet-Oberfläche
- startet bei `c` den CLI-Controller
- nutzt `ui.cli_view.show_welcome()` für den Starttext
- enthält aktuell noch eine veraltete Fehlermeldung mit `y/n/l`, obwohl der Prompt selbst `g/c/l` verwendet


### `config.py`
Hier stehen zentrale Einstellungen und Pfade.

Aktuell:
- `BASE_DIR`
- `DB_PATH`
- `FOOD_DB_PATH`
- `LICENSE_PATH`
- `DB_TEST_PATH`
- `DEVS`
- `VERSION`

Hinweis:
- `VERSION` steht im Code aktuell noch auf `0.1.0`, obwohl der gewünschte Release-Kontext laut Arbeitsstand V0.5 ist.

### `data/bls_foods.sqlite`
Diese Datenbank enthält eine große statische Lebensmittelsammlung.

Wichtig:
- sie dient als Nachschlagewerk für Lebensmitteldaten
- sie soll nur read-only verwendet werden
- Änderungen an dieser Datei sind im normalen Projektablauf nicht vorgesehen


### `bug_tracker.py`
Diese Datei sammelt bekannte Probleme und technische Baustellen des Projekts.

Sie ist keine Laufzeitlogik, aber nützlich für Planung und Wartung.
GUI- und UX-Planung liegen nun bewusst getrennt in `docs/gui_backlog.md`.

### `requirements.txt`
Hier stehen die Python-Abhängigkeiten des Projekts, zum Beispiel:
- `flet`
- `Flask`
- `pytest`
- weitere Hilfsbibliotheken

### `LICENSE.md`
Diese Datei enthält den vollständigen GPL-Lizenztext, der in der CLI angezeigt und in der GUI eingelesen wird.


## Was nicht direkt zum Kern gehört

Im Workspace gibt es außerdem:

- `venv/`: lokale virtuelle Python-Umgebung
- `__pycache__/`: automatisch erzeugte Python-Zwischendateien
- `.git/`: Git-Verwaltung
- `.codex/`: lokale Werkzeug- oder Editor-Datei

Diese Dinge sind wichtig für die Entwicklung, aber nicht Teil der eigentlichen Fachstruktur.

## Was macht `.gitignore`?

Die Datei `.gitignore` legt fest, welche Dateien oder Ordner Git nicht verfolgen soll.

Im aktuellen Projekt betrifft das unter anderem:
- Python-Caches
- virtuelle Umgebungen
- Editor-Dateien

Wichtig:
`.gitignore` löscht nichts. Sie verhindert nur, dass bestimmte Dateien versehentlich versioniert werden.

- `utils/` sollte nur Hilfsfunktionen enthalten oder später sauber auf andere Ordner verteilt werden.
- `legacy/` ist sinnvoll für alten Code, sollte aber nicht mit aktivem UI-Code verwechselt werden.
- ältere UI-Dateien in `legacy/` könnten später weiter aufgeräumt oder klarer markiert werden.
- Food-, Meal- und Activity-Tracking sind inzwischen sichtbar im aktiven Laufzeitpfad angekommen, nicht nur als Vorbereitung.
