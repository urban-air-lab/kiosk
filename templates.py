import streamlit as st

def template_large_image_with_caption(image_path, caption_text):
    """
    Layout: Großes Bild zentriert, kleiner Text darunter.
    """
    st.image(image_path, use_column_width='always') # Nimmt die volle Breite ein
    st.caption(caption_text)

def template_split_layout(content_left, content_right_or_image):
    """
    Layout: Links Text, rechts Bild oder weiterer Text.
    content_left: String oder Markdown
    content_right_or_image: Pfad zum Bild oder String/Markdown
    """
    # Erstelle zwei Spalten mit gleichen Breiten (Verhältnis 1:1)
    # Fütz ungleich Breiten z.B. [2, 1] nutzen
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(content_left)

    with col_right:
        # Prüfen, ob es sich um ein Bild handelt (einfacher Check)
        # In der Praxis wollen Sie hier vielleicht explizit zwischen Text und Bild unterscheiden
        if isinstance(content_right_or_image, str) and content_right_or_image.endswith(('.png', '.jpg', '.jpeg')):
            st.image(content_right_or_image, use_column_width=True)
        else:
            st.markdown(content_right_or_image)
