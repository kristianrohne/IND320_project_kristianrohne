import streamlit as st
from data_utils import load_reservoir_data
import matplotlib.pyplot as plt

st.header("Plot")
# Make user select the area that they want displayed
selected_area = st.selectbox("Choose area", [1, 2, 3, 4, 5])

# Load dataset with function from data_utils.py
df = load_reservoir_data(area_number = selected_area)
# List of numeric columns that makes sense to display
value_cols = ["fill_ratio", "capacity_twh", "filling_twh", "fill_ratio_previous_week", "fill_ratio_change"]

# Let user select a column 
selected_option = st.selectbox("Choose a column", ["All columns"] + list(value_cols))


# Get month labels from dataset
month_labels = df["date"].dt.to_period("M").astype(str).unique().tolist()
# Let user set interval for dataset
start_month, end_month = st.select_slider(
    "Select month range", options=month_labels, value=(month_labels[0], month_labels[0])
)


# Filter dataset for interval and the numeric columns
filtered_df = df[(df["date"].dt.to_period("M").astype(str) >= start_month) &
                  (df["date"].dt.to_period("M").astype(str) <= end_month)]

filtered_df = filtered_df.set_index("date")
filtered_df = filtered_df[value_cols]


# Plotting for all columns
if selected_option == "All columns":
    # min-max normalzing numeric columns 
    normalized_df = (filtered_df - filtered_df.min()) / (filtered_df.max() - filtered_df.min())

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 5))
    normalized_df.plot(ax=ax)
    ax.set_title("Reservoir metrics over time (normalized)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Normalized value (0–1)")
    st.pyplot(fig)
    plt.close(fig)

else:
    # Using only the selected column from the dataset
    filtered_df = filtered_df[selected_option]

    # Plotting the selected data
    fig, ax = plt.subplots(figsize=(12, 5))
    filtered_df.plot(ax=ax)
    ax.set_title(f"{selected_option} over time")
    ax.set_xlabel("Date")
    ax.set_ylabel(selected_option)
    st.pyplot(fig)
    plt.close(fig)
