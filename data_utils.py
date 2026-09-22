# data_utils.py
import pandas as pd
import streamlit as st

RENAME_MAP = {
    "dato_Id": "date",
    "omrType": "area_type",
    "omrnr": "area_number",
    "iso_aar": "iso_year",
    "iso_uke": "iso_week",
    "fyllingsgrad": "fill_ratio",
    "kapasitet_TWh": "capacity_twh",
    "fylling_TWh": "filling_twh",
    "neste_Publiseringsdato": "next_publication_date",
    "fyllingsgrad_forrige_uke": "fill_ratio_previous_week",
    "endring_fyllingsgrad": "fill_ratio_change",
}

@st.cache_data
def load_reservoir_data(area_number: int = 1) -> pd.DataFrame:
    # Loading the csv with pandas
    df = pd.read_csv("data/reservoirs.csv")
    # Renaming the columns, as in the notebook
    df = df.rename(columns=RENAME_MAP)
    # Set data format in the date column
    df["date"] = pd.to_datetime(df["date"])
    # Sort by dataes
    df = df.sort_values("date")
    # Only return the data from the specific area
    df = df[df["area_number"] == area_number]
    return df