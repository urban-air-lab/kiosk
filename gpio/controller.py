# controller.py
"""
Steuert den Streamlit-Kiosk per GPIO-Buttons (Raspberry Pi)
oder simuliert sie unter Windows (Dev-Mode).

Buttons:
    LEFT   (GPIO 23) → Zurück  (Previous)
    MIDDLE (GPIO 24) → Home
    RIGHT  (GPIO 25) → Weiter  (Next)

Schreibt den Namen der aktuellen App in state/current_app.txt.
Wird parallel zu main.py gestartet:
    python controller.py
"""
import os
import sys
import time
import platform
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
BASE_DIR = Path(__file__).resolve().parent.parent
STATE_DIR = BASE_DIR / "state"

# Pfade definieren (Funktionieren jetzt auf beiden Systemen)
APP_FILE = STATE_DIR / "current_app.txt"
CURRENT_APP_FILE = STATE_DIR / "apps.txt"

print(f"[controller] BASE_DIR = {BASE_DIR}")
print(f"[controller] APPS_FILE = {APPS_FILE} (existiert: {APPS_FILE.exists()})")


PIN_LEFT   = 23
PIN_MIDDLE = 24
PIN_RIGHT  = 25

BOUNCE_TIME = 0.3

# ---------- Hilfsfunktionen für State ----------
def load_apps():
    """Liest die Liste der verfügbaren Apps aus apps.txt."""
    try:
        with open(CURRENT_APP_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[controller] FEHLER: {CURRENT_APP_FILE} nicht gefunden!")
        return []


def get_current_app():
    """Liest den Namen der aktuell angezeigten App."""
    try:
        with open(CURRENT_APP_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def set_current_app(name: str):
    """Schreibt den Namen der neuen App in current_app.txt."""
    with open(CURRENT_APP_FILE, "w", encoding="utf-8") as f:
        f.write(name)
    print(f"[controller] → wechsle zu: {name}")

# ---------- Action Handler (die eigentliche Logik) ----------
def on_left():
    """Zurück: gehe zur vorherigen App."""
    apps = load_apps()
    if not apps:
        return
    current = get_current_app()
    if current in apps:
        idx = (apps.index(current) - 1) % len(apps)
    else:
        idx = 0
    set_current_app(apps[idx])

def on_middle():
    """Weiter: gehe zur nächsten App."""
    apps = load_apps()
    if not apps:
        return
    current = get_current_app()
    if current in apps:
        idx = (apps.index(current) + 1) % len(apps)
    else:
        idx = 0
    set_current_app(apps[idx])

def on_right():
    """Home: zurück zur ersten App."""
    apps = load_apps()
    if not apps:
        return
    set_current_app(apps[0])

# ---------- GPIO-Initialisierung (nur auf dem Pi) ----------
def setup_gpio():
    """
    Initialisiert die gpiozero-Buttons und bindet sie an die Handler.
    Gibt die Button-Objekte zurück, damit sie nicht garbage-collected werden.
    """
    from gpiozero import Button

    btn_left   = Button(PIN_LEFT,   pull_up=True, bounce_time=BOUNCE_TIME)
    btn_middle = Button(PIN_MIDDLE, pull_up=True, bounce_time=BOUNCE_TIME)
    btn_right  = Button(PIN_RIGHT,  pull_up=True, bounce_time=BOUNCE_TIME)

    # ← DAS HIER FEHLT WAHRSCHEINLICH IN IHREM CODE:
    btn_left.when_pressed   = on_left
    btn_middle.when_pressed = on_middle
    btn_right.when_pressed  = on_right

    print("[controller] GPIO-Buttons initialisiert:")
    print(f"   LEFT  (GPIO {PIN_LEFT})  → Zurück")
    print(f"   MID   (GPIO {PIN_MIDDLE}) → Weiter")
    print(f"   RIGHT (GPIO {PIN_RIGHT}) → Home")

    return btn_left, btn_middle, btn_right


# ---------- Windows-Fallback (Dev-Mode) ----------
def run_windows_fallback():
    """
    Auf Windows / ohne GPIO: Tastatur-Simulation.
    Drücken Sie a / s / d + Enter, um die Buttons zu simulieren.
    """
    print("[controller] Windows-Modus: keine GPIO verfügbar.")
    print("   Steuerung via Tastatur:")
    print("     a + Enter → Zurück (Left)")
    print("     s + Enter → Weiter (Middle)")
    print("     d + Enter → Home (Right)")
    print("     q + Enter → Beenden")
    print()

    while True:
        try:
            key = input("Button (a/s/d/q): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break

        if key == "a":
            on_left()
        elif key == "s":
            on_middle()
        elif key == "d":
            on_right()
        elif key == "q":
            break
        else:
            print("   Unbekannte Eingabe. Nur a/s/d/q erlaubt.")


# ---------- Main Entry Point ----------
def main():
    is_linux = platform.system() == "Linux"

    if is_linux:
        try:
            from signal import pause
            buttons = setup_gpio()  # WICHTIG: Referenz behalten!
            print("[controller] Warte auf Button-Drücke... (Ctrl+C zum Beenden)")
            pause()  # blockiert hier; gpiozero-Callbacks laufen im Hintergrund
        except ImportError as e:
            print(f"[controller] gpiozero nicht installiert: {e}")
            print("   Installiere mit:  pip install gpiozero")
            sys.exit(1)
        except Exception as e:
            print(f"[controller] GPIO-Fehler: {e}")
            print("[controller] Falle auf Tastatur-Modus zurück...")
            run_windows_fallback()
    else:
        run_windows_fallback()


if __name__ == "__main__":
    main()