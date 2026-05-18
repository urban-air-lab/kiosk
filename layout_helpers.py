# layout_helpers.py
import streamlit as st

# Konstante Beschriftungen für die 3 Buttons (Links, Mitte, Rechts)
FOOTER_LABELS = {
    "left": "◀ Zurück",
    "center": "🏠 Home",
    "right": "Weiter ▶"
}

def render_fixed_footer():
    """
    Rendert eine feste Fußzeile mit 3 Buttons-Beschriftungen,
    die den physischen Buttons unter dem Display entsprechen.
    """
    st.markdown("---")  # Trennlinie zum Inhalt
    footer_cols = st.columns(3)

    # Linker Button (GPIO Pin 23)
    with footer_cols[0]:
        st.markdown(f"<div style='text-align: center; font-size: 1.2rem; font-weight: bold;'>{FOOTER_LABELS['left']}</div>", unsafe_allow_html=True)

    # Mittlerer Button (GPIO Pin 24)
    with footer_cols[1]:
        st.markdown(f"<div style='text-align: center; font-size: 1.2rem; font-weight: bold;'>{FOOTER_LABELS['center']}</div>", unsafe_allow_html=True)

    # Rechter Button (GPIO Pin 25)
    with footer_cols[2]:
        st.markdown(f"<div style='text-align: center; font-size: 1.2rem; font-weight: bold;'>{FOOTER_LABELS['right']}</div>", unsafe_allow_html=True)

def template_hero(image_path, caption_text, show_footer=True):
    """
    Template: 1 Große Abbildung, kleiner Text darunter + Footer.
    """
    st.image(image_path, use_column_width='always')
    if caption_text:
        st.caption(caption_text)

    if show_footer:
        render_fixed_footer()

def template_split_left_text(content_left, content_right, show_footer=True):
    """
    Template: Links Text, rechts Abbildung oder mehr Text + Footer.
    """
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(content_left)

    with col_right:
        if isinstance(content_right, str) and content_right.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            st.image(content_right, use_column_width=True)
        else:
            st.markdown(content_right)

    if show_footer:
        render_fixed_footer()
