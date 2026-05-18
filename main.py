# main.py
import streamlit as st
import importlib
import time
import sys
import os
from pathlib import Path

DEV_MODE = False

# --- 1. Pfade & Konfiguration ---
BASE_DIR = Path(__file__).parent
STATE_DIR = BASE_DIR / "state"

# Pfade definieren (Funktionieren jetzt auf beiden Systemen)
CURRENT_APP_FILE = STATE_DIR / "current_app.txt"
APPS_FILE = STATE_DIR / "apps.txt"

# Layout-Helfer importieren
try:
    import layout_helpers
    sys.modules['layout_helpers'] = layout_helpers
except ImportError:
    pass

# WICHTIG: Muss als erstes Streamlit-Kommando kommen!
st.set_page_config(layout="wide")

# --- HILFSFUNKTIONEN ---
def get_current_app():
    try:
        with open(CURRENT_APP_FILE) as f:
            return f.read().strip()
    except:
        return None

def load_apps():
    try:
        with open(APPS_FILE) as f:
            return [l.strip() for l in f.readlines() if l.strip()]
    except:
        return []

# --- DEV MODE ---
# DEV_MODE = os.getenv("STELE_DEV") == "1"

if DEV_MODE:
    # Diese Steuerelemente bleiben jetzt dauerhaft sichtbar
    st.sidebar.header("DEV – GPIO Simulation")

    if st.sidebar.button("◀ Previous"):
        apps = load_apps()
        try:
            with open(CURRENT_APP_FILE) as f:
                current = f.read().strip()
            if current in apps:
                idx = (apps.index(current) - 1) % len(apps)
                with open(CURRENT_APP_FILE, "w") as f:
                    f.write(apps[idx])
                st.rerun()
        except:
            pass

    if st.sidebar.button("Next ▶"):
        apps = load_apps()
        try:
            with open(CURRENT_APP_FILE) as f:
                current = f.read().strip()
            if current in apps:
                idx = (apps.index(current) + 1) % len(apps)
                with open(CURRENT_APP_FILE, "w") as f:
                    f.write(apps[idx])
                st.rerun()
        except:
            pass

    if st.sidebar.button("🏠 Home"):
        apps = load_apps()
        if apps:
            with open(CURRENT_APP_FILE, "w") as f:
                f.write(apps[0])
            st.rerun()

    st.sidebar.success("Dev-Mode aktiv")

# --- HAUPT LOOP ---
content_placeholder = st.empty()

while True:
    # Apps laden
    apps = load_apps()
    current = get_current_app()

    # Falls keine aktuelle App gefunden oder ungültig -> auf erste App setzen
    if not current or current not in apps:
        if apps:
            current = apps[0]
            # Optional: Zustand direkt schreiben für Konsistenz
            with open(CURRENT_APP_FILE, "w") as f:
                f.write(current)
        else:
            with content_placeholder.container():
                st.error("Keine Apps in state/apps.txt gefunden.")
            time.sleep(1)
            continue

    try:
        # Modul dynamisch importieren
        module = importlib.import_module(f"apps.{current}")

        # Inhalt rendern (nur hier wird der Platzhalter überschrieben)
        with content_placeholder.container():
            module.run()

    except Exception as e:
        with content_placeholder.container():
            st.error(f"Fehler beim Laden von {current}")
            st.exception(e)

    time.sleep(1.5)
