import json
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Study Hours Visuals", page_icon="📈")
st.title("Study Hours Visualizations 📈")


def show_hour_statistics(hours):
    mean_column, median_column = st.columns(2)
    mean_column.metric("Mean study hours", f"{hours.mean():.2f} h")
    median_column.metric("Median study hours", f"{hours.median():.2f} h")


data_path = Path(__file__).resolve().parent.parent / "data.json"
with open(data_path, "r", encoding="utf-8") as json_file:
    study_data = json.load(json_file)

# Graphs from data.json
st.header(f"Part 1 · {study_data['chart_title']}")
st.caption(study_data["description"])

# Static bar chart
st.subheader("Weekly study hours by course")
weekly_totals = {}
for course, daily_hours in study_data["courses"].items():
    weekly_totals[course] = sum(daily_hours)

weekly_df = pd.DataFrame({
    "Course": list(weekly_totals.keys()),
    "Study hours": list(weekly_totals.values())
})
st.bar_chart(weekly_df.set_index("Course"))

# Dynamic line chart
st.subheader("Daily study hours by course")
course_names = list(study_data["courses"].keys())
if "selected_course" not in st.session_state:
    st.session_state["selected_course"] = course_names[0]

st.selectbox("Choose a course:", course_names, key="selected_course")
selected_course = st.session_state["selected_course"]
daily_df = pd.DataFrame({
    "Day": study_data["days"],
    "Study hours": study_data["courses"][selected_course]
})

max_hours = max(max(hours) for hours in study_data["courses"].values())
daily_chart = alt.Chart(daily_df).mark_line(point=True).encode(
    x=alt.X("Day:N", sort=study_data["days"], title="Day of the week"),
    y=alt.Y("Study hours:Q", title="Study hours outside class",
            scale=alt.Scale(domain=[0, max_hours + 0.5])),
    tooltip=[alt.Tooltip("Day:N"), alt.Tooltip("Study hours:Q", format=".1f")]
).properties(
    title=f"Daily Study Hours: {selected_course}",
    height=350
)
st.altair_chart(daily_chart, width="stretch")
st.caption("Choose another course to update the line.")
show_hour_statistics(daily_df["Study hours"])

# Graphs from data.csv
st.divider()
st.header("Part 2 · Logged Study Sessions")
csv_path = data_path.with_name("data.csv")
try:
    survey_data = pd.read_csv(
        csv_path, dtype={"Category": str, "Value": float}, keep_default_na=False
    )
except (OSError, pd.errors.EmptyDataError):
    st.warning("Place the provided data.csv in the Lab02 folder to view the survey charts.")
    st.stop()

if survey_data.empty:
    st.info("Log a study session on the Survey page to see these charts.")
    st.stop()

# Static pie chart uses every saved session.
st.subheader("Share of logged hours by course")
survey_totals = survey_data.groupby("Category", as_index=False)["Value"].sum()
survey_totals["Share"] = survey_totals["Value"] / survey_totals["Value"].sum()
survey_pie = alt.Chart(survey_totals).mark_arc().encode(
    theta=alt.Theta("Value:Q"),
    color=alt.Color("Category:N", title="Course"),
    tooltip=[
        alt.Tooltip("Category:N", title="Course"),
        alt.Tooltip("Value:Q", title="Total study hours", format=".2f"),
        alt.Tooltip("Share:Q", title="Share of all hours", format=".1%"),
    ],
).properties(
    title="Share of Logged Study Hours by Course",
    height=320,
)
st.altair_chart(survey_pie, width="stretch")

# Dynamic scatter plot uses the selected survey course.
st.subheader("Individual study sessions by course")
survey_data["Entry"] = range(1, len(survey_data) + 1)
survey_courses = survey_data["Category"].unique().tolist()
if st.session_state.get("survey_course") not in survey_courses:
    st.session_state["survey_course"] = survey_courses[0]

st.selectbox("Choose a survey course", survey_courses, key="survey_course")
survey_course = st.session_state["survey_course"]
course_sessions = survey_data[survey_data["Category"] == survey_course]
survey_scatter = alt.Chart(course_sessions).mark_circle(size=90).encode(
    x=alt.X(
        "Entry:Q", title="Survey entry number",
        axis=alt.Axis(tickMinStep=1),
        scale=alt.Scale(domain=[0, len(survey_data) + 1]),
    ),
    y=alt.Y(
        "Value:Q", title="Study hours",
        scale=alt.Scale(domain=[0, survey_data["Value"].max() + 0.5]),
    ),
    tooltip=[
        alt.Tooltip("Entry:Q", title="Survey entry number"),
        alt.Tooltip("Value:Q", title="Study hours", format=".2f"),
    ],
).properties(
    title=f"Logged Study Sessions: {survey_course}",
    height=320,
)
st.altair_chart(survey_scatter, width="stretch")
st.caption("Entry numbers show the order in which sessions were saved.")
show_hour_statistics(course_sessions["Value"])
