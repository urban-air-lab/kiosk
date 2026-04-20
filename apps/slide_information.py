import streamlit as st
from PIL import Image

def run():
    # --- Seiteneinstellungen ---
    st.set_page_config(
        page_title="UrbanAirLab Messnetz",
        layout="wide"
    )



    st.markdown(
        """
        <style>
        /* Gesamtes Padding reduzieren */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0.5rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 1280px;
        }
    
        /* Header-Abstand reduzieren */
        h1 {
            margin-top: 0rem;
            margin-bottom: 0.2rem;
            font-size: 2.2rem;
        }
    
        h2 {
            margin-top: 0.8rem;
            margin-bottom: 0.4rem;
        }
    
        h3 {
            margin-top: 0.6rem;
            margin-bottom: 0.3rem;
        }
    
        /* Weniger Abstand zwischen Markdown-Absätzen */
        p {
            margin-bottom: 0.5rem;
        }
    
        /* Sidebar komplett ausblenden */
        [data-testid="stSidebar"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- FIX: Top-Spacer gegen abgeschnittenen Titel ---
    st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)

    st.markdown("## UrbanAirLab Messnetz")
    st.caption(
        "Messnetz für Luft- und Aufenthaltsqualität am TechCampus"
    )

    # --- Hauptlayout ---
    left_col, right_col = st.columns([2.2, 1])

    # --- Linke Spalte ---
    with left_col:
        st.markdown("### Motivation und Ziele")

        st.markdown(
            """
            Die Lebensqualität in Städten hängt maßgeblich von der Qualität der
            Umgebungsluft ab. Die kontinuierliche Überwachung ist essenziell für
            Gesundheits‑ und Umweltschutz.
            """
        )

        st.markdown("### Ziele von UrbanAirLab")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                """
                **Messdatenerhebung**
                - CO, NO, NO₂, O₃, PM₂.₅, PM₁₀
                - Meteorologische Größen
    
                **Datenverarbeitung**
                - Speicherung, Prüfung & Filterung
                - Statistische Auswertung
                - Kalibrier‑ & QS‑Methoden
                """
            )

        with col2:
            st.markdown(
                """
                **Langzeitbeobachtung**
                - Tages‑, Wochen‑ & Jahresverläufe
                - Verkehrs‑ und Wetterabhängigkeiten
    
                **Bewertung**
                - Standortvergleiche
                - Identifikation von Belastungsschwerpunkten
                - Unterstützung stadtplanerischer Maßnahmen
                """
            )

    # --- Rechte Spalte ---
    with right_col:
        st.markdown("### Messpunkte am TechCampus")

        try:
            campus_map = Image.open("../assets/urbanairlab_messpunkte-2025.webp")
            st.image(
                campus_map,
                width='content'
            )
        except FileNotFoundError:
            st.info("Lageplan hier einfügen")

    # --- Footer ---
    st.markdown("---")
    st.caption("© UrbanAirLab – Hochschule Heilbronn")
    st.markdown("Ansprechpartner, Abkürzungen erklären")
