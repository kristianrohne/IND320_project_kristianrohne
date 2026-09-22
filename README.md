# IND320 Project - Reservoir Dashboard - Kristian Mathias Røhne

Compulsory hand-in project for IND320 – Data to Decision (NMBU), exploring weekly
reservoir statistics for Norway's electricity price areas (NO1–NO5), published by
NVE (the Norwegian Water Resources and Energy Directorate).

## Live app

https://ind320-project-kristianrohne.streamlit.app/

## Project structure

- `notebook.ipynb` – data exploration, plotting, and the development log for this hand-in
- `app.py` – Streamlit app home page
- `pages/` – the app's additional pages (data table, interactive plot, extra page)
- `data_utils.py` – shared, cached data loading used by all pages
- `data/reservoirs.csv` – the raw dataset

## Running locally

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
uv sync
uv run streamlit run app.py
```

## About this hand-in

This is part 1 of a four-part semester project. Data is currently read from a
local CSV file; a later part of the project will switch this to a MongoDB
database instead.