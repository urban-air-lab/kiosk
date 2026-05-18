# controller.py
import os
import sys
import time
from pathlib import Path


# --- KORREKTUR FÜR WINDOWS ---
# Auf Windows gibt es kein signal.pause(), wir definieren eine Alternative
if os.name == 'nt':
    # Windows erkannt
    print("INFO: Läufe auf Windows (Simulation). Keine Hardware-Buttons verfügbar.")

    # Wir definieren eine eigene pause()-Funktion für Windows
    def pause():
        print("Controller läuft im Hintergrund (Simulation). Drücke STRG+C zum Beenden.")
        while True:
            time.sleep(1)
else:
    # Linux / macOS / Raspberry Pi
    try:
        from signal import pause
    except ImportError:
        # Fallback, falls pause aus anderen Gründen fehlt
        def pause():
            while True:
                time.sleep(1)

# gpiozero importieren (funktioniert auf Windows meist nur mit Simulation/Mock-Pins)
# Falls gpiozero auf Windows ohne Mock-Pins installed ist, könnte es hier noch Fehler geben.
# Wir versuchen es einfach.
try:
    from gpiozero import Button
except Exception as e:
    print(f"FEHLER: gpiozero konnte nicht importiert werden: {e}")
    print("Stellen Sie sicher, dass Sie auf dem Pi sind oder die Mock-Pins konfiguriert sind.")
    sys.exit(1)

# --- Konfiguration (Pfad anpassen für Windows & Linux) ---
# Wir holen das Verzeichnis, in dem diese main.py liegt.
BASE_DIR = Path(__file__).parent
STATE_DIR = BASE_DIR / "state"

# Pfade definieren (Funktionieren jetzt auf beiden Systemen)
APP_FILE = STATE_DIR / "current_app.txt"
APPS_FILE = STATE_DIR / "apps.txt"

PIN_LEFT_PREV   = 23
PIN_CENTER_NEXT = 25
PIN_RIGHT_HOME  = 24

def get_apps():
    return []

def get_current_app_index(apps):
    return 0

def set_app(new_index, apps):
    print(f"Simulation: App wurde gewechselt (Index {new_index}).")

def go_prev(): print("Linker Button (Simulation)"); pass
def go_next(): print("Mittlerer Button (Simulation)"); pass
def go_home(): print("Rechter Button (Simulation)"); pass

if __name__ == "__main__":
    print("Starte Kiosk Controller...")

    # Auf dem echten Pi werden hier Buttons initialisiert
    # if not os.name == 'nt':
    #     btn_prev = Button(PIN_LEFT_PREV, pull_up=True, bounce_time=0.3)
    #     btn_next = Button(PIN_CENTER_NEXT, pull_up=True, bounce_time=0.3)
    #     btn_home = Button(PIN_RIGHT_HOME, pull_up=True, bounce_time=0.3)
    #     btn_prev.when_pressed = go_prev
    #     btn_next.when_pressed = go_next
    #     btn_home.when_pressed = go_home

    # Aufruf der (angepassten) pause-Funktion
    pause()
