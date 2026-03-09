import streamlit as st
import os
import pandas as pd
import pydeck as pdk

from dotenv import load_dotenv
from ual.data_processor import DataProcessor
from ual.get_config import get_config
from ual.influx.Influx_db_connector import InfluxDBConnector
from ual.influx.influx_query_builder import InfluxQueryBuilder
from ual.influx.sensors import SensorSource
from utils import get_timestamps_with_offset
load_dotenv()



def main():
    end_time_str, start_time_str = get_timestamps_with_offset()

    run_config: dict = get_config("slide_heatmap_config.yaml")

    ual4_source = SensorSource.from_strings(bucket=run_config["ual4_bucket"], sensor=run_config["ual4_sensor"])
    ual5_source = SensorSource.from_strings(bucket=run_config["ual5_bucket"], sensor=run_config["ual5_sensor"])
    connection: InfluxDBConnector = InfluxDBConnector(os.getenv("INFLUX_URL"), os.getenv("INFLUX_TOKEN"),
                                                      os.getenv("INFLUX_ORG"))

    ual4_query: str = InfluxQueryBuilder() \
        .set_bucket(ual4_source.get_bucket()) \
        .set_range(start_time_str, end_time_str) \
        .set_topic(ual4_source.get_sensor()) \
        .set_fields(run_config["ual4_fields"]) \
        .build()
    ual4_data: pd.DataFrame = connection.query_dataframe(ual4_query)
    st.dataframe(ual4_data)

    ual5_query: str = InfluxQueryBuilder() \
        .set_bucket(ual5_source.get_bucket()) \
        .set_range(start_time_str, end_time_str) \
        .set_topic(ual5_source.get_sensor()) \
        .set_fields(run_config["ual5_fields"]) \
        .build()
    ual5_data: pd.DataFrame = connection.query_dataframe(ual5_query)
    st.dataframe(ual5_data)

    data_processor: DataProcessor = (DataProcessor(ual4_data, ual5_data)
                                     .to_hourly()
                                     .remove_nan()
                                     .align_dataframes_by_time())

    ual4_data, ual5_data = data_processor.get_inputs(), data_processor.get_targets()

    "# Heatmap der 3 Stationen auf dem Campus (unvalidierte Messwerte)" # TODO: Mit Inhalt füllen

    combined_data = pd.DataFrame({
        'NO2_UAL_4': ual4_data['NO2'],
        'NO2_UAL_5': ual5_data['NO2'],
        "ual4_lat": run_config["ual4_lat"],
        "ual4_lon": run_config["ual4_lon"],
        "ual5_lat": run_config["ual5_lat"],
        "ual5_lon": run_config["ual5_lon"]
    })

    st.dataframe(combined_data)
    map_data = pd.DataFrame({
        'sensor': ['UAL-4', 'UAL-5'],
        'lat': [run_config["ual4_lat"], run_config["ual5_lat"]],
        'lon': [run_config["ual4_lon"], run_config["ual5_lon"]],
        'NO2': [ual4_data['NO2'].mean(), ual5_data['NO2'].mean()]  # Use mean or latest value
    })

    # Create ScatterplotLayer to show both sensors
    layer = pdk.Layer(
        "ScatterplotLayer",
        map_data,
        get_position='[lon, lat]',
        get_radius=50,  # Adjust size as needed
        get_fill_color=[255, 0, 0],  # Red color
        get_stroke_color=[0, 0, 0],
        get_line_width=1,
        pickable=True,
        opacity=0.8
    )

    # Set viewport to center between both sensors
    central_lat = map_data['lat'].mean()
    central_lon = map_data['lon'].mean()

    view_state = pdk.ViewState(
        latitude=central_lat,
        longitude=central_lon,
        zoom=10,
        pitch=0
    )

    # Render the map
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="light"
    )

    st.pydeck_chart(r)

if __name__ == "__main__":
    main()
