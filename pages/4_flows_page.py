import streamlit as st
from data_utils import load_flow_data
import matplotlib.pyplot as plt

st.header("Cross-border electricity flows")

# Load the daily flow data from MongoDB
df = load_flow_data()


# Split the page into two columns: pie chart on the left, line plot on the right
left, right = st.columns(2)

with left:
    # Choose connection with radio buttons and year with a selectbox
    connection = st.radio("Connection", sorted(df["connection"].unique()))
    years = sorted(df["date"].dt.year.unique())
    year = st.selectbox("Year", years)

    # Keep only the chosen connection and year
    pie_df = df[(df["connection"] == connection) & (df["date"].dt.year == year)]

    # Total flow per direction (in and out of Norway) for that year
    totals = pie_df.groupby("direction")["flow_mwh"].sum()

    fig, ax = plt.subplots()
    ax.pie(totals, labels=totals.index, autopct="%1.0f%%")
    ax.set_title(f"{connection}, {year}: flow in and out of Norway")
    st.pyplot(fig)
    plt.close(fig)

with right:
    # Choose which months to include with pills (several can be selected)
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    months = st.pills("Months", options=list(range(1, 13)), selection_mode="multi",
                      default=[1], format_func=lambda m: month_names[m - 1])

    if not months:
        st.info("Select at least one month.")
    else:
        # Same connection and year as on the left, but only the selected months
        line_df = pie_df[pie_df["date"].dt.month.isin(months)]

        # Some months have no data (e.g. 2024 starts in October), so check before plotting
        if line_df.empty:
            st.info("No data for the selected months in this year.")
        else:
            wide_df = line_df.pivot(index="date", columns="direction", values="flow_mwh")

            fig, ax = plt.subplots()
            wide_df.plot(ax=ax)
            ax.set_title(f"{connection}, {year}: daily flow")
            ax.set_xlabel("Date")
            ax.set_ylabel("Flow (MWh)")
            st.pyplot(fig)
            plt.close(fig)

# Short documentation of where the data comes from
with st.expander("About the data"):
    st.write(
        "The data shows cross-border electricity flows between Norway and its neighbouring "
        "countries, from the ENTSO-E Transparency Platform (transparency.entsoe.eu). "
        "The hourly data was downloaded through the ENTSO-E API in the Jupyter Notebook, "
        "stored in a local Cassandra database, extracted with Spark, aggregated to daily totals "
        "and inserted into MongoDB, which this page reads from. "
        "'out' means flow out of Norway (export), 'in' means flow into Norway (import)."
    )
    st.warning("Currently showing dummy data – the real ENTSO-E data will be added soon.")