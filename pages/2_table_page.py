import streamlit as st
import pandas as pd
from data_utils import load_reservoir_data


st.header("Reservoir data overview")
st.write(
    "Each row below represents one variable from the reservoir dataset for selected area, "
    "showing its trend over the first month of weekly observations (its own "
    "min–max scale per row)."
)

# Display only one area at a time, that is more clean
selected_area = st.selectbox("Choose area", [1, 2, 3, 4, 5])
# Load data with function from data_utils.py
df = load_reservoir_data(area_number = selected_area)

# Excluded non-numeric columns (area_type, date fields) since LineChartColumn needs numeric lists
numeric_cols = df.select_dtypes(include="number").columns

# For storing data from first month
rows = []
for col in numeric_cols:
    # Select only first 4 weeks
    first_month_values = df[col].iloc[:4].tolist()
    rows.append({"column": col, "trend": first_month_values})

# Use only first month from dataset
summary_df = pd.DataFrame(rows)

# Display dataset
st.dataframe(
    summary_df,
    column_config={
        "trend": st.column_config.LineChartColumn("First month trend"),
    },
    hide_index=True,
)
