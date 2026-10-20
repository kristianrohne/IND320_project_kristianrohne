import streamlit as st
from data_utils import load_reservoir_data, choose_area_type
import matplotlib.pyplot as plt

st.header("Plot")
# Choose area type; all area numbers of that type are plotted as separate lines
area_type = choose_area_type()

df = load_reservoir_data(area_type=area_type)

# List of numeric columns that make sense to display
# Excluding area_number/iso_year/iso_week because they're identifiers, not measurements,
value_cols = ["fill_ratio", "capacity_twh", "filling_twh", "fill_ratio_previous_week", "fill_ratio_change"]

# Let user select a column 
selected_option = st.selectbox("Choose a column", value_cols)


# Get month labels from dataset
month_labels = df["date"].dt.to_period("M").astype(str).unique().tolist()
# Let user set interval for dataset
start_month, end_month = st.select_slider(
        "Select month range", options=month_labels, value=(month_labels[0], month_labels[11])
)
# The NVE API has no date parameters, so all data is downloaded once (cached) and the slider selects the interval
st.caption("The NVE API always returns all data, so the slider selects which interval of the downloaded data is shown.")


# Filter dataset for interval
filtered_df = df[(df["date"].dt.to_period("M").astype(str) >= start_month) &
                  (df["date"].dt.to_period("M").astype(str) <= end_month)]


# Reshape: one row per date, one column per area number, values from the chosen column.
# Pandas draws each column as its own line, so we get one line per area.
wide_df = filtered_df.pivot(index="date", columns="area_number", values=selected_option)

# Plot one line per area number
fig, ax = plt.subplots(figsize=(12, 5))
wide_df.plot(ax=ax)
ax.set_title(f"{selected_option} for {area_type} areas")
ax.set_xlabel("Date")
ax.set_ylabel(selected_option)
ax.legend(title="Area number")
st.pyplot(fig)
plt.close(fig)