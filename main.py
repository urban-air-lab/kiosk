import streamlit as st
import importlib
import time
import sys
from pathlib import Path
import os

# Pfad-Setup sicherstellen
#BASE_DIR = Path(__file__).resolve().parent

# Sicherheitshalber zum System-Path hinzufügen
#if str(BASE_DIR) not in sys.path:
#    sys.path.insert(0, str(BASE_DIR))

# Hier DEFINITIV absolute Pfade verwenden, damit es mit controller.py übereinstimmt
#APP_FILE = BASE_DIR / "state" / "current_app.txt"
#APPS_FILE = BASE_DIR / "state" / "apps.txt"
APP_FILE = "/home/kiosk/kiosk/state/current_app.txt"
APPS_FILE = "/home/kiosk/kiosk/state/apps.txt"  #


st.set_page_config(layout="wide")

# Funktionen definieren
def get_current_app():
    try:
        with open(APP_FILE) as f:
            return f.read().strip()
    except:
        return None

def load_apps():
    try:
        with open(APPS_FILE) as f:
            return [l.strip() for l in f.readlines() if l.strip()]
    except:
        return []


apps = load_apps()
current = get_current_app()

if current not in apps:
    if apps:
        current = apps[0]
    else:
        st.error("Keine Apps in state/apps.txt gefunden.")
        st.stop()

# Dev Mode START
DEV_MODE = os.getenv("STELE_DEV") == "1"

if DEV_MODE:
    st.sidebar.header("DEV – GPIO Simulation")

    if st.sidebar.button("◀ Previous"):
        with open(APP_FILE, "w") as f:
            f.write(apps[(apps.index(current) - 1) % len(apps)])
            st.rerun() # Sofort neu laden nach Klick

    if st.sidebar.button("Next ▶"):
        with open(APP_FILE, "w") as f:
            f.write(apps[(apps.index(current) + 1) % len(apps)])
            st.rerun()

    if st.sidebar.button("🌐 Toggle Language"):
        lang_file = BASE_DIR / "state" / "lang.txt"
        try:
            with open(lang_file) as f:
                lang = f.read().strip()
            with open(lang_file, "w") as f:
                f.write("en" if lang == "de" else "de")
        except:
            pass
# Dev Mode ENDE

# Eigentlicher Code

for module_name in list(sys.modules.keys()):
    if module_name.startswith('apps.'):
        del sys.modules[module_name]

try:
    # Importieren
    module = importlib.import_module(f"apps.{current}")

    # Funktion ausführen
    module.run()

except Exception as e:
    st.error(f"Fehler beim Laden von {current}")
    st.exception(e)

try:
    module = importlib.import_module(f"apps.{current}")
    module.run()
except Exception as e:
    st.error(f"Fehler beim Laden von {current}")
    st.exception(e)
