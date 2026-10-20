import streamlit as st
import pandas as pd
from data_utils import load_reservoir_data, choose_area_type


st.header("Reservoir data overview")
st.write(
    "Each row is one variable. Each column shows its trend during the first calendar month "
    "of the data for one area of the chosen type."
)

# Choose area type; all area numbers of that type are shown side by side
area_type = choose_area_type()
# Load data with function from data_utils.py
df = load_reservoir_data(area_type=area_type)

# Keep only the first calendar month in the data (not just the first 4 rows)
first_month = df["date"].dt.to_period("M").min()
first_month_df = df[df["date"].dt.to_period("M") == first_month]
st.write(f"First month in the data: **{first_month}**")

# Measurement columns only (area_number, iso_year and iso_week are identifiers)
value_cols = ["fill_ratio", "capacity_twh", "filling_twh", "fill_ratio_previous_week", "fill_ratio_change"]
area_numbers = sorted(df["area_number"].unique())

# One row per variable, one list of first-month values per area number
rows = []
for col in value_cols:
    row = {"column": col}
    for nr in area_numbers:
        area_values = first_month_df[first_month_df["area_number"] == nr][col]
        row[f"{area_type} {nr}"] = area_values.tolist()
    rows.append(row)

# Use only first month from dataset
summary_df = pd.DataFrame(rows)

# Display dataset: one mini line chart per area number
st.dataframe(
    summary_df,
    column_config={
        f"{area_type} {nr}": st.column_config.LineChartColumn(f"{area_type} {nr}")
        for nr in area_numbers
    },
    hide_index=True,
)
