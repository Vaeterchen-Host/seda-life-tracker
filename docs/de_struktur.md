# Projektstruktur (ai-generiert)

> Diese Datei beschreibt den aktuellen Aufbau des Workspaces und soll als einfache Orientierung für das Projekt dienen.

## Kurzüberblick

SEDA ist aktuell ein Python-Projekt mit drei Hauptbereichen:

- Fachlogik in `model/`
- Benutzeroberflächen in `ui/`
- Daten in `data/`
- Tests in `tests/`
- Dokumentation in `docs/`

Zusätzlich gibt es Hilfsdateien, ältere Experimente und einige Legacy- oder Utility-Dateien, die nicht direkt zum Kernablauf gehören.

## Ordner im Projekt

### `model/`
Hier liegt die eigentliche Anwendungslogik.

Wichtige Dateien:
- `classes.py`: zentrale Domänenklassen wie `User`, `WaterLog`, `WeightLog`, `Food`, `Meal`, `MealItem` und Hilfsobjekte für Nährwerte
- `database.py`: SQLite-Zugriff, Tabellenaufbau und Datenbankmethoden für User, Wasserlogs, Gewichtslogs, Aktivitätslogs, Food-Logs, Mahlzeiten und Meal-Items
- `controller.py`: CLI-Steuerung und Verbindung zwischen Eingaben, Logik und Datenbank
- `open_food_api.py`: experimentelle Anbindung an Open Food Facts für Suchen per Barcode oder Produktname

### `ui/`
Dieser Ordner enthält alles rund um die Benutzeroberfläche.

Wichtige Dateien:
- `ui.py`: grafische Oberfläche mit Flet
- `cli_view.py`: Ein- und Ausgaben für die Kommandozeile
- `theme_utils.py`: kleine Hilfsfunktionen zum Umschalten des Flet-Themes


### `data/`
Hier liegen Projektdateien mit echten Nutzdaten.

Aktuell:
- `database.db`: die SQLite-Datenbank des Projekts
- `bls_foods.sqlite`: separate Lebensmitteldatenbank, die in `model/database.py` über `FoodDatabase` verwendet wird

### `tests/`
Hier liegen automatisierte Tests.

Aktuell:
- `test_classes.py`: Tests für Klassen aus `model/classes.py`
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
- mehrere exportierte Diagramme als `.png`
- `Anforderungsanalyse Tabelle.ods`: begleitende Analyse-Dokumentation

### `utils/`
Hier liegen Hilfsdateien, Einzeltests oder ältere Zusatzskripte.

Beispiele:
- `paginator.py`: Hilfsfunktion für seitenweise CLI-Ausgabe, aktuell für lange Lizenztexte genutzt
- `tobi_classes.py`: ältere oder parallele Klassenimplementierung aus der Entwicklung
- `bine_cli_main.py`: alternativer CLI-Controller-Prototyp
- `test_bine.py`: zusätzliche entwicklungsnahe Datenbanktests
- `tobi_cli_controller`: ausführbares Python-Skript ohne `.py`-Endung, offenbar als weiterer experimenteller Controller behalten

Dieser Ordner wirkt im Moment wie ein Sammelbereich für Zwischenstände oder ergänzende Werkzeuge.

### `legacy/`
Hier liegt älterer Code, der nicht mehr zum Hauptpfad gehört, aber noch aufbewahrt wird.

Aktuell:
- `ui_german.py`
- `ui_discardable.py`

## Wichtige Dateien im Hauptordner

### `main.py`
Das ist der Einstiegspunkt des Programms.

Aktuell:
- fragt ab, ob die GUI oder die CLI gestartet werden soll
- zeigt optional die Lizenz an
- startet bei `g` die Flet-Oberfläche
- startet bei `c` den CLI-Controller
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

### `data/bls_foods.sqlite`
Diese Datenbank enthält eine große statische Lebensmittelsammlung.

Wichtig:
- sie dient als Nachschlagewerk für Lebensmitteldaten
- sie soll nur read-only verwendet werden
- Änderungen an dieser Datei sind im normalen Projektablauf nicht vorgesehen


### `bug_tracker.py`
Diese Datei sammelt bekannte Probleme und technische Baustellen des Projekts.

Sie ist keine Laufzeitlogik, aber nützlich für Planung und Wartung.

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
- Teile der Codebasis bereiten bereits Food- und Meal-Tracking vor, aber der aktuell sichtbare Laufzeitfokus liegt weiterhin vor allem auf User-, Wasser- und Gewichtsverwaltung.
