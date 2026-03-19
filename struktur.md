# Projektstruktur

Diese Ordnerstruktur soll das Projekt uebersichtlicher machen. Nicht jeder Ordner muss sofort voll sein. Wichtig ist vor allem, dass Dateien an einem sinnvollen Ort liegen.

## Ordner im Projekt

### `model/`
Hier kommen Klassen und Datenobjekte hinein, die das eigentliche Fachthema des Programms beschreiben.

Beispiele:
- `Kunde`
- `Buchung`
- `Zimmer`
- `Rechnung`

Kurz gesagt:
In `model` liegt, **was** das Programm verwaltet.

### `ui/`
Hier kommt alles hinein, was zur Benutzeroberflaeche gehoert.

Beispiele:
- Tkinter-Fenster
- Buttons
- Eingabefelder
- Ausgaben fuer Benutzer

Kurz gesagt:
In `ui` liegt, **was der Benutzer sieht und benutzt**.

### `data/`
Hier kommen Dateien hinein, mit denen das Programm arbeitet.

Beispiele:
- `.txt`
- `.csv`
- `.json`
- gespeicherte Beispieldaten

Kurz gesagt:
In `data` liegen **Daten-Dateien, aber normalerweise kein Python-Code**.

### `tests/`
Hier kommen Testdateien hinein. Tests pruefen automatisch, ob Teile des Programms richtig funktionieren.

Beispiele:
- Wird eine Buchung korrekt erstellt?
- Werden falsche Eingaben erkannt?
- Funktioniert eine Methode wie erwartet?

Kurz gesagt:
In `tests` liegt **Code zum Pruefen des Programms**.

### `docs/`
Hier koennen Notizen, Abgaben, Beschreibungen oder Skizzen hinein.

Beispiele:
- Aufgabenbeschreibung
- UML-Skizzen
- Projektideen
- Notizen fuer die Doku

### `Beispiele/`
Dieser Ordner ist fuer Probe-Code, Experimente oder kleine Beispiele gedacht.

Kurz gesagt:
Alles, was **nicht zum eigentlichen Hauptprogramm gehoert**, kann hier hinein.

## Was ist `.gitignore`?

Die Datei `.gitignore` sagt Git, welche Dateien oder Ordner **nicht mit versioniert werden sollen**.

Das ist nuetzlich fuer:
- Cache-Dateien
- temporaere Dateien
- Editor-Dateien
- lokale Testdateien
- Beispielordner, wenn er nicht Teil der Abgabe sein soll

In diesem Projekt wird durch `.gitignore` zum Beispiel `Beispiele/` ignoriert. Das bedeutet:
Git merkt sich Aenderungen in diesem Ordner nicht fuer Commits.

Wichtig:
`.gitignore` loescht keine Dateien. Es verhindert nur, dass Git sie mit aufnimmt.

## Empfehlung fuer dieses Projekt

Im Moment koennte man eure Dateien ungefaehr so einordnen:

- `tk_reader.py` passt wahrscheinlich nach `ui/`
- `buchungssystem.py` passt wahrscheinlich nach `model/` oder spaeter in eine Logik-Datei
- `Beispiele/` bleibt als eigener Beispielordner bestehen

## Einfacher Merksatz

- `model` = Was ist das?
- `ui` = Was sieht der Benutzer?
- `data` = Welche Dateien benutzt das Programm?
- `tests` = Wie pruefen wir, ob es richtig funktioniert?
- `docs` = Was muessen wir dazu festhalten?
