import streamlit as st
from PIL import Image

# ---------- Page Config ----------
st.set_page_config(
    page_title="UrbanAirLab – Sensorsystem",
    layout="wide"
)

# ---------- CI + Platzspar‑CSS ----------
st.markdown(
    """
    <style>
    /* Gesamtfläche */
    .block-container {
        padding: 0.6rem 1.6rem;
        max-width: 1280px;
    }


    /* Farben (CI-nahe, anpassbar) */
    :root {
        --ci-blue: #003A8F;
        --ci-lightblue: #E6EEF8;
        --ci-gray: #4A4A4A;
    }

    /* Titel */
    h1, h2 {
        color: var(--ci-blue);
        margin-bottom: 0.1rem;
    }

    h3 {
        color: var(--ci-blue);
        margin-top: 0.4rem;
        margin-bottom: 0.2rem;
    }

    p, li {
        color: var(--ci-gray);
        font-size: 0.92rem;
    }

    ul {
        margin-top: 0.2rem;
        margin-bottom: 0.5rem;
        padding-left: 1.2rem;
    }

    hr {
        margin: 0.6rem 0;
    }

    /* Sidebar komplett aus */
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- FIX: Top-Spacer gegen abgeschnittenen Titel ---
st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)


# ---------- Titel ----------
st.markdown("## Cloudbasiertes Open‑Source‑System mit Low‑Cost‑Sensoren")

# ---------- 3‑Spalten‑Layout ----------
left, middle, right = st.columns([1.35, 0.95, 1.35])

# ---------- Linke Spalte ----------
with left:
    st.markdown(
        """
        Um die **räumliche und zeitliche Variabilität** der Luftverschmutzung
        in Städten zu erfassen, ist ein engmaschiges Messnetz erforderlich.

        - In Heilbronn existieren nur zwei Messstellen der **LUBW**
        - Mobile, kostengünstige Sensoren schließen diese Lücke
        - Einsatz von **Low‑Cost‑Luftqualitätssensoren (LQS)**

        Die verwendeten Sensorsysteme wurden am Institut für Steuerungs‑
        und Kraftwerkstechnik (IFK) der Universität Stuttgart entwickelt
        und an der Hochschule Heilbronn für dieses Projekt umgesetzt.
        """
    )

# ---------- Bild ----------
with middle:
    try:
        img = Image.open("assets/sensorsystem.jpg")
        st.image(
            img,
            width='stretch',
            caption=(
                "Sensorsystem zur Messung von CO, NO, NO₂, O₃, "
                "PM₂.₅, PM₁₀, rel. Feuchte und Temperatur"
            )
        )
    except FileNotFoundError:
        st.info("Sensorsystem‑Abbildung hier einfügen")

# ---------- Rechte Spalte ----------
with right:
    st.markdown(
        """
        Am Markt verfügbare Lösungen sind häufig **nicht transparent**,
        da Hardware, Software und Algorithmen nicht offen zugänglich sind.

        Dies ist problematisch für:
        - Wissenschaftliche Forschung
        - Öffentliche Entscheidungsfindung
        - Bürgerbeteiligung

        **Ansatz von UrbanAirLab**
        - Vollständig offene Hardware & Software
        - Nachvollziehbarkeit und Reproduzierbarkeit
        - Community‑Beteiligung möglich
        - Anpassbar und erweiterbar
        - Kombinierbar mit externen Datenquellen
        """
    )

# ---------- Footer ----------
st.markdown(
    "<small style='color:#666'>www.hs-heilbronn.de/UrbanAirLab</small>",
    unsafe_allow_html=True
)