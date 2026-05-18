# apps/demo/main.py
import streamlit as st
from layout_helpers import *

def run():
    st.title("Demo App")

    # --- Beispiel usage Template 1: Large Image ---
    st.subheader("Hero Image Beispiel")
    layout_helpers.template_hero(
        image_path="https://placehold.co/800x400",
        caption_text="Das ist ein Bild mit kleinem Text darunter."
    )

    st.markdown("---")

    # --- Beispiel usage Template 2: Split Layout ---
    st.subheader("Split Layout Beispiel")
    layout_helpers.template_split_left_text(
        content_left="### Links Text\nHier steht eine Erklärung zum Bild rechts. Das Layout nutzt `st.columns` [2].",
        content_right="https://placehold.co/400x300"
    )
