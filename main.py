# main.py
import streamlit as st
import importlib
import time
import sys
import os
from pathlib import Path
from layout_helpers import *

DEV_MODE = True

# --- Pfade & Konfiguration ---
BASE_DIR = Path(__file__).parent
STATE_DIR = BASE_DIR / "state"
CURRENT_APP_FILE = STATE_DIR / "current_app.txt"
APPS_FILE = STATE_DIR / "apps.txt"

try:
    import layout_helpers
    sys.modules['layout_helpers'] = layout_helpers
except ImportError:
    pass

# Styling für 1280x720 Kiosk-Display
# Mindestschriftgröße 18px für gute Lesbarkeit
# Weniger Padding, um mehr Text auf den Screen zu bekommen
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    body { font-size: 18px !important; }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1280px;
    }
    h1 { font-size: 2rem; }
    h2 { font-size: 1.4rem; }
    [data-testid="stSidebar"] { display: none; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Hilfsfunktionen ---
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

# --- Session State Init ---
if "last_app" not in st.session_state:
    st.session_state.last_app = None

# --- DEV MODE (unverändert) ---
if DEV_MODE:
    st.sidebar.header("DEV – GPIO Simulation")

    if st.sidebar.button("◀ Previous"):
        apps = load_apps()
        try:
            with open(APP_FILE) as f:
                current = f.read().strip()
            if current in apps:
                idx = (apps.index(current) - 1) % len(apps)
                with open(APP_FILE, "w") as f:
                    f.write(apps[idx])
                st.rerun()
        except:
            pass

    if st.sidebar.button("Next ▶"):
        apps = load_apps()
        try:
            with open(APP_FILE) as f:
                current = f.read().strip()
            if current in apps:
                idx = (apps.index(current) + 1) % len(apps)
                with open(APP_FILE, "w") as f:
                    f.write(apps[idx])
                st.rerun()
        except:
            pass

    if st.sidebar.button("🏠 Home"):
        apps = load_apps()
        if apps:
            with open(APP_FILE, "w") as f:
                f.write(apps[0])
            st.rerun()

    st.sidebar.success("Dev-Mode aktiv")

# --- Apps & aktuellen Eintrag laden ---
apps = load_apps()
current = get_current_app()

if not current or current not in apps:
    if apps:
        current = apps[0]
        with open(CURRENT_APP_FILE, "w") as f:
            f.write(current)
    else:
        st.error("Keine Apps in state/apps.txt gefunden.")
        st.stop()

# --- App-Modul-Cache löschen bei Wechsel (wichtig!) ---
if st.session_state.last_app != current:
    for module_name in list(sys.modules.keys()):
        if module_name.startswith("apps."):
            del sys.modules[module_name]
    st.session_state.last_app = current

# --- App rendern (KEIN st.empty, KEIN while-Loop) ---
try:
    module = importlib.import_module(f"apps.{current}")
    st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)
    module.run()
    render_fixed_footer()

except Exception as e:
    st.error(f"Fehler beim Laden von {current}")
    st.exception(e)

# --- Auto-Refresh: prüfen, ob sich die App geändert hat ---
time.sleep(1.5)
new_current = get_current_app()
if new_current != current:
    # App wurde durch Button gewechselt → komplettes Rerun
    st.rerun()
else:
    # Auch ohne App-Wechsel: regelmäßig refreshen
    # (damit der Controller-Trigger detected wird)
    st.rerun()
