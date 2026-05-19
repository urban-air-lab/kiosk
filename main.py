# main.py
import streamlit as st
import importlib
import time
import sys
import os
from pathlib import Path
from layout_helpers import *

DEV_MODE = False

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
    
    /* === FIX: Streamlit Stale-Elemente sofort ausblenden === */
    [data-stale="true"] {
        display: none !important;
    }
    .element-container.stale,
    .stale-element {
        display: none !important;
        opacity: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Sidebar NUR verstecken, wenn NICHT im Dev-Mode
if not DEV_MODE:
    st.markdown(
        """
        <style>
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

    def switch_app(direction):
        """direction: -1 = previous, +1 = next, 0 = home"""
        apps = load_apps()
        if not apps:
            st.sidebar.error("Keine Apps in apps.txt gefunden")
            return

        try:
            current = get_current_app()
        except Exception as e:
            st.sidebar.error(f"Fehler beim Lesen: {e}")
            current = None

        # Fallback: wenn current ungültig, auf ersten Eintrag setzen
        if current not in apps:
            st.sidebar.warning(f"'{current}' nicht in apps.txt – springe zu '{apps[0]}'")
            new_app = apps[0]
        else:
            if direction == 0:
                new_app = apps[0]
            else:
                idx = (apps.index(current) + direction) % len(apps)
                new_app = apps[idx]

        try:
            CURRENT_APP_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(CURRENT_APP_FILE, "w", encoding="utf-8") as f:
                f.write(new_app)
            st.sidebar.success(f"→ {new_app}")
        except Exception as e:
            st.sidebar.error(f"Schreibfehler: {e}")
            return

        st.rerun()

    if st.sidebar.button("◀ Previous", key="dev_prev"):
        switch_app(-1)

    if st.sidebar.button("Next ▶", key="dev_next"):
        switch_app(+1)

    if st.sidebar.button("🏠 Home", key="dev_home"):
        switch_app(0)

    # Status-Anzeige für Debugging
    st.sidebar.divider()
    st.sidebar.caption(f"**current_app.txt:** `{get_current_app()}`")
    st.sidebar.caption(f"**apps.txt:** {load_apps()}")
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
