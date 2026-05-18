import streamlit as st
from layout_helpers import *

def run():
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
    left, right = st.columns([1.35, 1.35])

    # ---------- Linke Spalte ----------
    with left:
        st.markdown(
            """
            - Gudula Achterberg
            - Regina Reuz
            - Jutta Trumpfheller
            - Béatrice Kachel
            - Marco Wollny
            - Mirja Wollny
            - Klimastiftung Kreissparkasse Heilbronn
            - Melanie Dominke           """
        )

    # ---------- Rechte Spalte ----------
    with right:
        st.markdown(
            """
            - Thomas Jakob & Daniela Finken 
            - Uelzhöffer LEH Ellhofen KG
            - Uelzhöffer LEH Sontheim KG
            - Baumann
            - Uelzhöffer LEH Südbahnhof KG
            - Koeber Landschaftsarchitektur GmbH
            - EDEKA Südwest
            - Ulrike Barthelmes
            """
        )

    # ---------- Footer ----------
#    render_fixed_footer()