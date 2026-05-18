import streamlit as st
from layout_helpers import *

def run():
    # Styling für 1280x720 Kiosk-Display
    # Mindestschriftgröße 18px für gute Lesbarkeit
    # Weniger Padding, um mehr Text auf den Screen zu bekommen
    st.markdown(
        """
        <style>
        body {
            font-size: 18px !important;
        }

        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
            max-width: 1280px;
        }

        h1 {
            font-size: 2rem;
            margin-top: 0.2rem;
            margin-bottom: 0.5rem;
        }

        h2 {
            font-size: 1.4rem;
            margin-top: 1rem;
            margin-bottom: 0.4rem;
        }

        ul {
            margin-top: 0rem;
            margin-bottom: 0rem;
        }

        li {
            margin-bottom: 0.2rem;
        }

        [data-testid="stSidebar"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## Das UrbanAirLab Projekt")

    # Info-Box für die Zusammenfassung
    st.info("""
    **Kurzinfo:** Aufbau eines qualitätsgesicherten Messnetzes (17 Stationen: 7 Campus, 10 Stadt) zur Luftqualität in Heilbronn. 
    Ansatz: Verbindung von moderner Sensortechnik und KI. Integraler Bestandteil der Bewerbung "European Green Capital".
    """)

    # Hauptlayout: 2 Spalten um Platz optimal zu nutzen
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Problemstellung")
        st.markdown("""
        - **Hohe Belastung:** Luftschadstoffe in urbanen Räumen (Verkehr, Industrie).
        - **Datenlücke:** Nur 2 amtliche LUBW-Stationen in Heilbronn.
        - **Kosten & Qualität:** Amtliche Messgeräte sind extrem teuer; Low-Cost-Sensoren (40€) benötigen wissenschaftliche Kalibration.
        - **Gesundheit:** Feinstaub verursacht ca. 300.000 vorzeitige Todesfälle/Jahr in der EU.
        - **Klimawandel:** Verstärkter Urban Heat Island-Effekt.
        """)

        st.markdown("### ✅ Motivation & Lösungsansatz")
        st.markdown("""
        Wir schließen die **räumliche Datenlücke** durch Sensortechnik + Machine Learning. 
        Kooperation mit LUBW, DLR und Stadt Heilbronn. Der offene Ansatz fördert Bürgerinteresse 
        und vereint zwei Zukunftsthemen in einem Projekt.
        """)

    with col2:
        st.markdown("### Projektziele")
        st.markdown("""
        - **Erhebung:** Qualitätsgesicherte Messung von CO, NO, NO₂, O₃, PM₂.₅, PM₁₀.
        - **Methodik:** Entwicklung von ML-basierten Kalibrationsmethoden.
        - **Langzeit:** Beobachtung von Verkehrs- und Wetterabhängigkeiten.
        - **Bewertung:** Einfluss von Maßnahmen (Begrünung, Tempolimit) prüfen.
        """)

        st.markdown("### Nahziele & Integration")
        st.markdown("""
        - **Lehre:** Reallabor für Studierende (Analytik, KI, Big Data).
        - **Third Mission:**
            - Frei zugängliche Daten (Open Data).
            - Integration in Green City Dashboard.
            - Sensibilisierung von Stadtverwaltung & Bürgern.
        """)

    render_fixed_footer()