import streamlit as st
from pathlib import Path
from PIL import Image
from layout_helpers import *

def run():
    st.markdown("## Campusmessnetz")

    # Layout: 40% Text, 60% Bild
    col_text, col_image = st.columns([0.4, 0.6])

    with col_text:
        st.markdown("""
        **Standorte & Messstrategie**

        Das Messnetz auf dem Hochschulcampus in Sontheim besteht aus strategisch positionierten Messstellen. 
        Diese ermöglichen die gezielte Untersuchung der Luftqualität in Abhängigkeit von lokalen Belastungsschwerpunkten 
        (z.B. Zufahrten, Parkbereiche) und frequentierten Aufenthaltsbereichen der Studierenden.

        Durch die enge Vernetzung der Sensoren können mikroklimatische Effekte und Schadstoffverteilung im direkten 
        Umfeld des Campus detailliert erfasst werden. Die Daten dienen als Open-Source-Basis für Forschungsprojekte 
        und die Lehre.
        """)

    with col_image:
        # --- PFAD ANPASSEN ---
        # Hier den Pfad zu Ihrem Bild angeben (z.B. assets/campus_map.jpg)
        ROOT_DIR = Path(__file__).resolve().parent.parent
        image_path = ROOT_DIR / "assets" / "urbanairlab_messpunkte-2025.webp"

        try:
            if image_path.exists():
                img = Image.open(image_path)
                st.image(img, caption="Lageplan der Campus-Messstellen", width="stretch")
            else:
                st.info(f"Bild nicht gefunden: {image_path.name}")
        except Exception as e:
            st.error(f"Fehler beim Laden des Bildes: {e}")

#    render_fixed_footer()