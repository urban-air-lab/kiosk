import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go
import time

from plotly.subplots import make_subplots
from dotenv import load_dotenv
from ual.data_processor import DataProcessor
from ual.get_config import get_config
from ual.influx.Influx_db_connector import InfluxDBConnector
from ual.influx.influx_query_builder import InfluxQueryBuilder
from ual.influx.sensors import SensorSource

from PIL import Image

# --- KONFIGURATION ---
load_dotenv()

CACHE_KEY_PREFIX = "slide_colocation"
CACHE_DURATION_SECONDS = 60  # 1 Minute

def run():
    run_config: dict = get_config("slide_colocation_config.yaml")

    ual_source = SensorSource.from_strings(bucket=run_config["ual_bucket"], sensor=run_config["ual_sensor"])
    lubw_source = SensorSource.from_strings(bucket=run_config["lubw_bucket"], sensor=run_config["lubw_sensor"])
    connection: InfluxDBConnector = InfluxDBConnector(os.getenv("INFLUX_URL"), os.getenv("INFLUX_TOKEN"),
                                                      os.getenv("INFLUX_ORG"))

    # --- CACHING LOGIK ---
    current_time = time.time()

    # Prüfen, ob wir schon Daten im Cache haben und ob diese noch jung genug sind
    has_cache = (CACHE_KEY_PREFIX + "_last_update") in st.session_state
    is_expired = has_cache and (
                current_time - st.session_state[CACHE_KEY_PREFIX + "_last_update"] > CACHE_DURATION_SECONDS)

    if not has_cache or is_expired:
        print(f"DEBUG: Aktualisiere Daten von InfluxDB... ({current_time})")

        # 1. QUERIES AUSFÜHREN
        ual3_query: str = InfluxQueryBuilder() \
            .set_bucket(ual_source.get_bucket()) \
            .set_range(run_config["start_time"], run_config["stop_time"]) \
            .set_topic(ual_source.get_sensor()) \
            .set_fields(run_config["ual3_fields"]) \
            .build()
        ual3_data_raw: pd.DataFrame = connection.query_dataframe(ual3_query)

        lubw_query: str = InfluxQueryBuilder() \
            .set_bucket(lubw_source.get_bucket()) \
            .set_range(run_config["start_time"], run_config["stop_time"]) \
            .set_topic(lubw_source.get_sensor()) \
            .set_fields(run_config["lubw_fields"]) \
            .build()
        lubw_data_raw: pd.DataFrame = connection.query_dataframe(lubw_query)

        # 2. DATA PROCESSING
        # Wir cachen das ERGEBNIS des Processors, um Rechenzeit zu sparen beim Neuladen
        data_processor: DataProcessor = (DataProcessor(ual3_data_raw, lubw_data_raw)
                                         .to_hourly()
                                         .remove_nan()
                                         .align_dataframes_by_time())

        ual3_data, lubw_data = data_processor.get_inputs(), data_processor.get_targets()

        # 3. IN SESSION STATE SPEICHERN
        st.session_state[CACHE_KEY_PREFIX + "_ual"] = ual3_data
        st.session_state[CACHE_KEY_PREFIX + "_lubw"] = lubw_data
        st.session_state[CACHE_KEY_PREFIX + "_last_update"] = current_time

    else:
        # Daten aus Cache laden
        # print(f"DEBUG: Nutze gecachte Daten...") # Optional falls man Logs will
        ual3_data = st.session_state[CACHE_KEY_PREFIX + "_ual"]
        lubw_data = st.session_state[CACHE_KEY_PREFIX + "_lubw"]

        # --- ANZEIGE ---
        st.markdown("# Kollokationsmessungen an der LUBW Station in der Hans-Riesser-Straße")
        st.markdown("Hintergrundinformationen bereitstellen, die LUBW betreibt eine Messstelle ... ")
        st.markdown("Seit Juli 2025 betreiben wir dort parallel eine Messstation")

        # --- GRAFIK ---
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=ual3_data.index, y=ual3_data['NO2'], mode='lines', name='UAL3 NO2'),
                      secondary_y=False,
                      )
        fig.add_trace(go.Scatter(x=lubw_data.index, y=lubw_data['NO2'], mode='lines', name='LUBW NO2'),
                      secondary_y=False,
                      )
        fig.add_trace(go.Scatter(x=lubw_data.index, y=lubw_data['RLF'], mode='lines', name='rel. hum'),
                      secondary_y=True,
                      )

        # Layout Einstellungen
        # WICHTIG: width=None und autosize=True für die volle Breite
        fig.update_layout(
            title='Vergleich der Messergebnisse',
            width=None,  # Breite NICHT festlegen (damit sie flexibel ist)
            autosize=True,  # Autosize aktivieren
            legend=dict(xanchor="auto", yanchor="auto")
        )

        # Chart rendern
        # key f"{CACHE_KEY_PREFIX}_{time.time()}" verhindert den DuplicateElementID Fehler
        st.plotly_chart(fig, width='stretch', key=f"{CACHE_KEY_PREFIX}_{time.time()}")