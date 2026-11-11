import streamlit as st
import streamlit.components.v1 as components

# Configure page layout
st.set_page_config(page_title="Tower Math Defense PWA", page_icon="🏰", layout="centered")

st.title("🏰 Tower Math Defense PWA")
st.markdown("Defeat enemies in ascending arithmetic order! Play using **Desktop Arrow Keys** or **Mobile Touch Buttons** below.")

# Load local HTML game build
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Render game inside Streamlit iframe component
components.html(html_content, height=680, scrolling=False)
