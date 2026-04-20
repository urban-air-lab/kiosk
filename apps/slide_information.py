import streamlit as st
from PIL import Image
from pathlib import Path

def run():
    # --- CSS Styling ---
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
    st.caption("Messnetz für Luft- und Aufenthaltsqualität am TechCampus")

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
                """
            )

    # --- Rechte Spalte ---
    with right_col:
        st.markdown("### Messpunkte am TechCampus")

        # Pfad dynamisch finden (besser als hardcodiert)
        # Wir gehen davon aus, dass assets im Hauptordner liegt
        try:
            # Pfad relativ zum Skript (apps/... -> ../assets/...)
            # Oder einfach wie in main.py: BASE_DIR nutzen, wenn hier verfügbar
            # Hier fest definieren relativ zum Projekt-Root:
            ROOT_DIR = Path(__file__).resolve().parent.parent  # Geht aus apps/ -> stele/
            image_path = ROOT_DIR / "assets" / "urbanairlab_messpunkte-2025.webp"

            if image_path.exists():
                campus_map = Image.open(image_path)
                # FIX: use_container_width=True statt width='content'
                st.image(campus_map, use_container_width=True)
            else:
                st.info(f"Lageplan nicht gefunden: {image_path}")

        except Exception as e:
            st.info(f"Fehler beim Laden des Lageplans: {e}")

    # --- Footer ---
    st.markdown("---")
    st.caption("© UrbanAirLab – Hochschule Heilbronn")
    st.markdown("Ansprechpartner, Abkürzungen erklären")
