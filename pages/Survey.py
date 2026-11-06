import csv
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

csv_path = Path(__file__).resolve().parent.parent / "data.csv"

st.title("Log a Study Session 📝")
st.write("Enter one study session outside class. Use the same spelling each time you log a course.")

if not csv_path.is_file() or csv_path.stat().st_size == 0:
    st.error("Place the provided data.csv with its Category,Value header in the Lab02 folder.")
    st.stop()

with st.form("survey_form"):
    category_input = st.text_input("Which course did you study?", placeholder="CS 1301")
    value_input = st.text_input("How many hours did you study?", placeholder="1.5")
    submitted = st.form_submit_button("Save study session")

if submitted:
    course = category_input.strip()
    try:
        hours = float(value_input)
    except ValueError:
        st.error("Enter study hours as a number, such as 1.5.")
    else:
        if not course:
            st.error("Enter a course name.")
        elif not 0 < hours <= 24:
            st.error("Enter more than 0 and up to 24 hours for one session.")
        else:
            try:
                with csv_path.open("a", encoding="utf-8", newline="") as csv_file:
                    csv.writer(csv_file).writerow([course, hours])
            except OSError:
                st.error("The session could not be saved to data.csv.")
            else:
                st.success("Study session saved.")

st.divider()
st.header("Sessions Saved in CSV")
current_data = pd.read_csv(csv_path, dtype={"Category": str}, keep_default_na=False)
if current_data.empty:
    st.info("Your first saved session will appear here.")
else:
    st.dataframe(
        current_data.rename(columns={"Category": "Course", "Value": "Study hours"}),
        hide_index=True,
    )
