import streamlit as st

st.set_page_config(page_title="Study Dashboard", page_icon="📚")

st.title("My Week in Study Hours 📚")
st.write("How is my study time divided between courses throughout the week?")
st.write("""
- Open **Survey** in the sidebar to log a study session outside class.
- Open **Visuals** to compare the original weekly study hours and explore the
  hours recorded through Survey.
""")
