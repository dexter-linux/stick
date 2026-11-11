import streamlit as st
import streamlit.components.v1 as components

# Configure page layout
st.set_page_config(page_title="Tower Math Defense PWA", page_icon="🏰", layout="centered")

st.title("🏰 Tower Math Defense PWA")
st.markdown("Defeat enemies in ascending arithmetic order! Play using **Desktop Arrow Keys** or **Mobile Touch Buttons** below.")

# Read the contents of index.html and render it directly as components HTML
with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

components.html(html_content, height=780, scrolling=False)
