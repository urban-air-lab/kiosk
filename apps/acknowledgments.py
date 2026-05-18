import streamlit as st
from layout_helpers import *

def run():
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
#    render_fixed_footer()