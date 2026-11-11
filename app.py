import streamlit as st

# Configure page layout
st.set_page_config(page_title="Tower Math Defense PWA", page_icon="🏰", layout="centered")

st.title("🏰 Tower Math Defense PWA")
st.markdown("Defeat enemies in ascending arithmetic order! Play using **Desktop Arrow Keys** or **Mobile Touch Buttons** below.")

# Render local index.html game inside Streamlit iframe
st.iframe("index.html", height=780)
