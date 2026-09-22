import streamlit as st

st.header("Reservoir Dashboard")

st.write(
    "This app explores weekly reservoir statistics for Norway's electricity "
    "price areas (NO1–NO5), published by NVE (the Norwegian Water Resources "
    "and Energy Directorate). Use the sidebar to navigate between an overview "
    "table showing each variable's first-month trend and an interactive plot "
    "of the full dataset."
)

st.write(
    "This is part 1 of a semester-long project for IND320 – Data to Decision. "
    "Data is currently read from a local CSV file; a later part of the "
    "project will switch this to a MongoDB database instead."
)