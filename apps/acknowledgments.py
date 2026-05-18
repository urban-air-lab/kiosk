import streamlit as st
from layout_helpers import *

def run():
    # ---------- Page Config ----------
    st.set_page_config(
        page_title="Fördernde",
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
    st.markdown("## Danksagung")

    st.markdown(
        '''
### „Wenn ich wüsste, dass morgen die Welt unterginge, würde ich heute noch ein Apfelbäumchen pflanzen.“
        
Dieses Zitat wird seit Ende des Zweiten Weltkriegs oft Martin Luther in den Mund gelegt, lässt sich aber nicht belegbar in den Schriften des Reformators nachweisen. Die Zuschreibung hält sich dennoch so hartnäckig wie die Hoffnung, die der Satz ausdrückt: auch wenn es morgen vielleicht zu spät ist, kann man im Heute dennoch das Richtige tun. 

Jeder Baum und Beitrag zählt – das ist der Leitspruch unseres Projekts. Hartnäckig hoffnungsvoll sind wir gemeinsam mit unseren Fördernden sowie unseren Baumpatinnen und Baumpaten, mit deren Hilfe wir am TechCampus der Hochschule Heilbronn einen Klimawald pflanzen.
Klimaschutz im Kleinen, Reallabor und Begegnungsort – **vielen Dank für Ihre Unterstützung, ohne Sie könnten wir dieses wichtige Projekt nicht umsetzen!**
        ''')

    # ---------- 3‑Spalten‑Layout ----------
    left, middle, right = st.columns([1.35, 0.95, 1.35])

    # ---------- Linke Spalte ----------
    with left:
        st.markdown(
            """
            - Gudula Achterberg
            - Ulrike Barthelmeß
            - Annette Baumann
            - Gianna Cuttica
            - Melanie Dominke
            - EDEKA Südwest und Stiftung NatureLife-International
            - EDEKA Ueltzhöfer
            - Förderkreis der Hochschule Heilbronn e. V.
           """
        )

    # ---------- Bild ----------
    with middle:
        st.markdown(
            """
            - Charles und Dr. Melanie Gish
            - Anna und Tobias Held
            - Dr. Katja Horneffer
            - Thomas Jakob & Daniela Finken
            - Béatrice Kachel
            - Koeber Landschaftsarchitektur GmbH
            - KlimaStiftung der Kreissparkasse Heilbronn
            """
        )

    # ---------- Rechte Spalte ----------
    with right:
        st.markdown(
            """
            - Kreissparkasse Heilbronn
            - Paula Leihenseder
            - Literaturhaus Heilbronn
            - Regina Reuz
            - Roland Schweizer
            - Jutta Trumpfheller
            - Marco und Mirja Wollny
            """
        )

    # ---------- Footer ----------
    render_fixed_footer()