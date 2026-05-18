import streamlit as st
from layout_helpers import *

def run():
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

#    render_fixed_footer()