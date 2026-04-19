# Projektstruktur

> Diese Datei beschreibt den aktuellen Stand des Repositories möglichst nah am Ist-Zustand. Sie ist bewusst eine Bestandsaufnahme und keine Aussage darüber, was davon bereits fachlich sauber, fertig oder fehlerfrei ist.

## Hinweis zur Autorschaft

- Bestehende Projektdateien und die Grundstruktur des Repositories sind nicht KI-generiert.
- Diese überarbeitete Strukturbeschreibung wurde mit KI-Unterstützung angepasst.
- Die Einordnung, welche Bereiche aktiv, experimentell oder Übergangsstand sind, basiert auf dem aktuellen Dateistand im Repository.

## Kurzüberblick

SEDA ist aktuell ein Python-Projekt mit zwei aktiven Bedienwegen:

- CLI über `main.py` und `model/controller.py`
- GUI mit Flet über `ui/ui.py`

Daneben gibt es mehrere Entwicklungs- und Übergangsbereiche:

- eine Hauptdatenbank in `data/database.db`
- eine separate Lebensmitteldatenbank in `data/bls_foods.sqlite`
- Prototypen und Zwischenstände in `utils/`
- alte UI-Stände in `legacy/`
- Lern- und Beispielcode in `Beispiele/`
- Rohdaten und Importskript für BLS in `BLS_4_0_2025_DE/`

## Aktive Projektbereiche

### `model/`

Hier liegt die Fach- und Datenlogik.

Wichtige Dateien:

- `classes.py`: zentrale Domänenklassen wie `User`, `WaterLog`, `WeightLog`, `Food`, `Meal`, `MealItem`, `FoodLog` und weitere Log-/Hilfsklassen; Datei enthält teils markierte KI-generierte Passagen, ist aber insgesamt aktive Projektlogik
- `database.py`: SQLite-Zugriff für die Hauptdatenbank und zusätzlich eine `FoodDatabase` für die separate BLS-Lebensmitteldatenbank; enthält kommentierte Hinweise auf KI-gestützte Teilanpassungen, ist aber nicht rein KI-generiert
- `controller.py`: aktueller CLI-Steuerfluss zwischen `ui.cli_view`, den Klassen und der Datenbank; wirkt überwiegend manuell gewachsen
- `open_food_api.py`: experimenteller Zugriff auf Open Food Facts; aktuell eher Entwicklungsstand als integrierter Kernbestandteil

### `ui/`

Hier liegt die Benutzeroberfläche.

Wichtige Dateien:

- `ui.py`: aktive Flet-GUI; in der Datei selbst als KI-generierter Ausgangscode mit manuellen Anpassungen beschrieben
- `cli_view.py`: Ein-/Ausgabe- und Prompt-Helfer für die Kommandozeile; enthält einzelne als KI-generiert markierte Abschnitte, ist aber nicht vollständig KI-generiert
- `theme_utils.py`: kleine Theme-Hilfsfunktionen für Flet; eher kleiner Hilfscode ohne klare Herkunftsmarkierung

Hinweis:
Die GUI und die CLI greifen beide direkt auf Teile aus `model/` zu. Eine komplett getrennte Schichtenstruktur ist im aktuellen Stand noch nicht konsequent durchgezogen.

### `data/`

Hier liegen die Datenbanken:

- `database.db`: Hauptdatenbank des Projekts; keine KI-generierte Datei, sondern Laufzeit-/Entwicklungsdaten
- `bls_foods.sqlite`: separate SQLite-Datenbank mit Lebensmitteldaten; erzeugte Datendatei, nicht KI-generiert

### `tests/`

Hier liegen die automatisierten Tests für den aktiven Code.

Aktuell enthalten:

- `test_classes.py`: Tests für Domänenklassen; Datei enthält explizit markierte KI-generierte Testanteile
- `test_cli_view.py`: Tests für CLI-Ein-/Ausgabe-Verhalten; einzelne Stellen sind als KI-generiert gekennzeichnet
- `test_database.py`: Tests für Datenbankfunktionen; enthält mehrere explizit als KI-generiert markierte Abschnitte
- `test.db`: leere oder lokal genutzte Testdatenbankdatei; nicht KI-generiert

### `docs/`

Hier liegt die Projektdokumentation.

Aktuell enthalten:

- `de_struktur.md`: diese deutsche Strukturübersicht; in der aktuellen überarbeiteten Form KI-unterstützt
- `en_structur.md`: englische Strukturübersicht; in der aktuellen überarbeiteten Form KI-unterstützt
- mehrere exportierte Diagramme als PNG; nicht als KI-generiert markiert
- `Anforderungsanalyse Tabelle.ods`: Analyse-/Planungsdokument; keine KI-Markierung erkennbar

## Weitere Ordner mit Entwicklungs- oder Übergangscharakter

### `legacy/`

Alte oder verworfene UI-Stände, die nicht der aktuelle Haupteinstieg sind.

Aktuell:

- `ui_german.py`: ältere deutschsprachige GUI-Version; in der Datei selbst als KI-generierter Code mit Anpassungen beschrieben
- `ui_discardable.py`: experimenteller UI-Stand; in den Kommentaren als Test-/Beispielcode und teilweise KI-generiert beschrieben

### `utils/`

Sammelbereich für Hilfsfunktionen, Prototypen und persönliche Zwischenstände.

Aktuell:

- `paginator.py`: aktiver kleiner Helfer für paginierte CLI-Ausgabe; Docstring nennt teilweise KI-generierten Inhalt
- `bine_cli_main.py`: alternativer CLI-Prototyp; überwiegend manueller Zwischenstand mit einzelnen Kommentaren zum Status
- `tobi_cli_controller`: älterer CLI-Prototyp; kein klarer KI-Hinweis in der Datei
- `tobi_classes.py`: ältere oder parallele Klassenversion; enthält wie `model/classes.py` markierte KI-generierte Hilfsanteile
- `test_bine.py`: zusätzliche, eher prototypische Tests; enthält markierte KI-generierte Fixture-/Testanteile

Wichtig:
`utils/` ist derzeit kein rein technischer Utility-Ordner, sondern auch ein Ablageort für Entwicklungsstände.

### `Beispiele/`

Lern- und Beispielcode, der nicht direkt zum eigentlichen Produktpfad gehört.

Darin liegen u. a.:

- allgemeine Python-Übungsdateien
- `flet_tutorial/` mit Flet-Beispielen

Zur Autorschaft gibt es dort keine einheitliche Kennzeichnung; der Ordner wirkt insgesamt wie Lern- und Experimentiermaterial.

### `BLS_4_0_2025_DE/`

Arbeitsbereich rund um die BLS-Lebensmitteldaten.

Aktuell enthalten:

- Originaldateien wie Excel/PDF zur BLS-Datenbasis; nicht KI-generiert
- `import_bls_to_sqlite.py` zum Aufbau der SQLite-Lebensmitteldatenbank
- ein separates `venv/` in diesem Unterordner

## Wichtige Dateien im Projektwurzelverzeichnis

### `main.py`

Aktueller Einstiegspunkt des Projekts.

Verhalten im Ist-Zustand:

- zeigt zuerst eine Begrüßung
- fragt danach nach CLI, GUI oder Lizenzanzeige
- startet bei `g` die Flet-GUI
- startet bei `c` den CLI-Controller
- zeigt bei `l` die Langfassung der Lizenz

Zur Herkunft:
Für `main.py` ist keine ausdrückliche KI-Markierung im Dateikopf vorhanden.

### `config.py`

Zentrale Pfad- und Projektkonfiguration.

Aktuell definiert:

- `BASE_DIR`
- `DB_PATH`
- `FOOD_DB_PATH`
- `LICENSE_PATH`
- `DB_TEST_PATH`
- `DEVS`
- `VERSION`

Zur Herkunft:
In `config.py` sind Teile ausdrücklich als KI-generiert und andere ausdrücklich als nicht KI-generiert kommentiert.

### `README.md`

Kurze Projektbeschreibung mit Start- und Testhinweisen. Die Datei ist als Einstieg brauchbar, aber in Details nicht komplett synchron mit dem aktuellen Repository-Stand.

Zur Herkunft:
Das README nennt sich selbst teilweise KI-generiert.

### `bug_tracker.py`

Sammlung bekannter Probleme und Baustellen. Keine Laufzeitlogik, aber relevant für Wartung und Planung.

### `requirements.txt`

Python-Abhängigkeiten des Projekts.

## Verzeichnisse, die eher Entwicklungsumgebung als Projektstruktur sind

Diese Dinge sind vorhanden, gehören aber nicht zur fachlichen Architektur:

- `venv/`: Haupt-virtuelle Umgebung
- `BLS_4_0_2025_DE/venv/`: zusätzliche virtuelle Umgebung im BLS-Unterordner
- `__pycache__/`: Python-Zwischendateien
- `.pytest_cache/`: pytest-Cache
- `.git/`: Git-Metadaten
- `.codex`: lokales Werkzeug-/Editor-Artefakt
- `test_db/`: Zielordner für während Tests erzeugte temporäre Datenbanken

## Struktur-Fazit zum Status quo

Der aktuelle Stand lässt sich sinnvoll in vier Ebenen lesen:

- aktive Anwendung: `main.py`, `model/`, `ui/`, `data/`, `tests/`
- projektrelevante Dokumentation und Analyse: `docs/`, `README.md`, `bug_tracker.py`
- Entwicklungs- und Übergangsbereiche: `utils/`, `legacy/`
- externe bzw. vorbereitende Datenarbeit und Lernmaterial: `BLS_4_0_2025_DE/`, `Beispiele/`

Das Repository ist damit funktional nutzbar, aber strukturell noch gemischt: aktiver Code, Prototypen, Datenaufbereitung und Lernmaterial liegen aktuell noch recht nah beieinander.
