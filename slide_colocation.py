import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go

from plotly.subplots import make_subplots
from dotenv import load_dotenv
from ual.data_processor import DataProcessor
from ual.get_config import get_config
from ual.influx.Influx_db_connector import InfluxDBConnector
from ual.influx.influx_query_builder import InfluxQueryBuilder
from ual.influx.sensors import SensorSource

load_dotenv()

def main():

    run_config: dict = get_config("slide_colocation_config.yaml")

    ual_source = SensorSource.from_strings(bucket=run_config["ual_bucket"], sensor=run_config["ual_sensor"])
    lubw_source = SensorSource.from_strings(bucket=run_config["lubw_bucket"], sensor=run_config["lubw_sensor"])
    connection: InfluxDBConnector = InfluxDBConnector(os.getenv("INFLUX_URL"), os.getenv("INFLUX_TOKEN"),
                                                      os.getenv("INFLUX_ORG"))

    ual3_query: str = InfluxQueryBuilder() \
        .set_bucket(ual_source.get_bucket()) \
        .set_range(run_config["start_time"], run_config["stop_time"]) \
        .set_topic(ual_source.get_sensor()) \
        .set_fields(run_config["ual3_fields"]) \
        .build()
    ual3_data: pd.DataFrame = connection.query_dataframe(ual3_query)

    lubw_query: str = InfluxQueryBuilder() \
        .set_bucket(lubw_source.get_bucket()) \
        .set_range(run_config["start_time"], run_config["stop_time"]) \
        .set_topic(lubw_source.get_sensor()) \
        .set_fields(run_config["lubw_fields"]) \
        .build()
    lubw_data: pd.DataFrame = connection.query_dataframe(lubw_query)

    data_processor: DataProcessor = (DataProcessor(ual3_data, lubw_data)
                                     .to_hourly()
                                     .remove_nan()
                                     .align_dataframes_by_time())

    ual3_data, lubw_data = data_processor.get_inputs(), data_processor.get_targets()

    "# Kollokationsmessungen an der LUBW Station in der Hans-Riesser-Straße" # TODO: Mit Inhalt füllen
    "Hintergrundinformationen bereitstellen, die LUBW betreibt eine Messstelle ... "
    "Seit Juli 2025 betreiben wir dort parallel eine Messstation"

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
    fig.update_layout(title='Vergleich der Messergebnisse')
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
