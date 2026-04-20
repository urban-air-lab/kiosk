import streamlit as st
import importlib
import time
import sys
from pathlib import Path

# dev mode, über  set STELE_DEV=1  in terminal aktivieren
import os

DEV_MODE = os.getenv("STELE_DEV") == "1"

if DEV_MODE:
    st.sidebar.header("DEV – GPIO Simulation")

    if st.sidebar.button("◀ Previous"):
        with open(APP_FILE, "w") as f:
            f.write(apps[(apps.index(current) - 1) % len(apps)])

    if st.sidebar.button("Next ▶"):
        with open(APP_FILE, "w") as f:
            f.write(apps[(apps.index(current) + 1) % len(apps)])

    if st.sidebar.button("🌐 Toggle Language"):
        with open("state/lang.txt") as f:
            lang = f.read().strip()
        with open("state/lang.txt", "w") as f:
            f.write("en" if lang == "de" else "de")


# eigentlicher code

BASE_DIR = Path(__file__).resolve().parent
APPS_DIR = BASE_DIR / "apps"

APP_FILE = "./state/current_app.txt"
APPS_FILE = "./state/apps.txt"

# sicherstellen, dass /apps importierbar ist
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

st.set_page_config(layout="wide")

def get_current_app():
    try:
        with open(APP_FILE) as f:
            return f.read().strip()
    except:
        return None

def load_apps():
    with open(APPS_FILE) as f:
        return [l.strip() for l in f.readlines() if l.strip()]

apps = load_apps()
current = get_current_app()

if current not in apps:
    current = apps[0]

try:
    module = importlib.import_module(f"apps.{current}")
    module.run()
except Exception as e:
    st.error(f"Fehler beim Laden von {current}")
    st.exception(e)

time.sleep(1)
st.rerun()

