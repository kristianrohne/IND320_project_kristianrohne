# data_utils.py
# this is the shared, cached loader used by the pages scripts
import pandas as pd
import streamlit as st
import requests

# NVE's Magasinstatistikk API: returns all weekly reservoir data as JSON
NVE_URL = "https://biapi.nve.no/magasinstatistikk/api/Magasinstatistikk/HentOffentligData"

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
def load_reservoir_data(area_type: str = "EL") -> pd.DataFrame:
    
    
    # Fetch the data from the API (no parameters, always returns all data)
    response = requests.get(NVE_URL, timeout=60)
    response.raise_for_status()  # stop with an error if the request failed
    # The JSON is a list of dictionaries (one per row), which pandas turns into a table
    df = pd.DataFrame(response.json())

    # Renaming the columns, as in the notebook
    df = df.rename(columns=RENAME_MAP)
    # The API data interleaves multiple areas and isn't sorted by date
    # Convert the date column to datetime
    df["date"] = pd.to_datetime(df["date"])
    # Sort by dates
    df = df.sort_values("date")

    # Only return the data from the specific area type AND area number
    # Only return the data for the chosen area type (all area numbers of that type)
    df = df[df["area_type"] == area_type]
    return df


# Which area numbers exist for each area type in the dataset
AREAS = {
    "EL": [1, 2, 3, 4, 5],  # electricity price areas NO1-NO5
    "VASS": [1, 2, 3],      # water-course areas
    "NO": [0],              # the whole of Norway
}


def choose_area_type():
    # Only the area type, used where all area numbers are shown at once
    st.caption("**Area type:** EL = electricity price areas (NO1–NO5), "
               "VASS = water-course areas, NO = all of Norway.")
    return st.radio("Choose area type", list(AREAS.keys()), horizontal=True)