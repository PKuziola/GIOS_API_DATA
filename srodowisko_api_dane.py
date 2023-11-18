"""
Module is reponsible for getting data from gios api and uploading it into Sqlite3 database.
"""

import os
from datetime import datetime
from datetime import date
from time import sleep
import sqlite3
import requests
import pandas
from pandas import json_normalize


def convert_data_to_df(source_data):
    """
    Converts downloaded data to pandas.DataFrame

    Args:
        source_data: Data downloaded from API

    Returns:
        pandas.DataFrame
    """
    df = pandas.DataFrame(source_data)
    df = df.explode("data")
    df = pandas.concat([df, df.pop("data").apply(pandas.Series)], axis=1).reset_index(
        drop=True
    )
    return df


def save_df_in_sqlite(source_frame: pandas.DataFrame, if_exists: str, table_name: str):
    """
    Uploads pandas.Dataframe to sqlite3 database.

    Args:
        source_frame: Source data, dataframe which we want to upload to sqlite3 database.
        if_exists: Action which is taken when database arelady exists, options are: [replace, append, fail].
        table_name: Table to which data is uploaded.

    Returns:
        None

    Raises:
        sqlite3.OperationalError: database is locked: Error occurs when database is opened while running script.
    """
    to_sql_kwargs = dict(
        {
            "name": table_name,
            "con": sqlite3.connect(os.getcwd() + "\gios.db"),
            "schema": None,
            "if_exists": if_exists,
            "index": False,
            "index_label": None,
            "chunksize": None,
            "dtype": None,
            "method": None,
        }
    )
    c = sqlite3.connect(os.getcwd() + "\gios.db").cursor()
    source_frame.to_sql(**to_sql_kwargs)


def download_station_info():
    """
    Downloads information about air quality monitoring stations in Poland from the GIOŚ API.

    Args:
        None

    Returns:
        pandas.DataFrame: Dataframe containing information about monitoring stations.
    """
    gios_url = "https://api.gios.gov.pl/pjp-api/rest/"
    response_all_stations = requests.get(f"{gios_url}station/findAll", timeout=10)
    response_all_stations_json = response_all_stations.json()
    json_df = json_normalize(response_all_stations_json).drop(
        columns=[
            "city.id",
            "city.commune.communeName",
            "city.commune.districtName",
            "city.commune.provinceName",
        ]
    )
    json_df.rename(columns={"city.name": "cityName"}, inplace=True)
    return json_df


def download_measurement_data(today: bool = False):
    """
    Downloads air quality measurement data from the API.

    Args:
        today: Boolean argument which defines if we download only today's data, default value is False

    Returns:
        pd.DataFrame: Dataframe containing measurement data.
    """
    gios_url = "https://api.gios.gov.pl/pjp-api/rest/"
    today_date = date.today()
    data = []
    response_all_stations = requests.get(f"{gios_url}station/findAll", timeout=10)
    response_all_stations_json = response_all_stations.json()
    for element in response_all_stations_json:
        data_list = []
        id = element["id"]
        response_sensor = requests.get(f"{gios_url}station/sensors/{id}", timeout=10)
        response_sensor_json = response_sensor.json()
        for sensor_element in response_sensor_json:
            data_element = {}
            sensor_id = sensor_element["id"]
            response_sensor_measurements = requests.get(
                f"{gios_url}data/getData/{sensor_id}", timeout=10
            )
            sleep(5)
            response_sensor_measurements = response_sensor_measurements.json()
            measurements_values = response_sensor_measurements["values"]
            for measurements_value in measurements_values:
                if today is False or (
                    today is True
                    and today_date
                    == datetime.strptime(
                        measurements_value["date"], "%Y-%m-%d %H:%M:%S"
                    ).date()
                ):
                    data_list.append(
                        {
                            "paramCode": response_sensor_measurements["key"],
                            "date": measurements_value["date"],
                            "value": measurements_value["value"],
                        }
                    )


            data_element.update(
                {"stationId": id, "sensorId": sensor_id, "data": data_list}
            )
            data.append(data_element)
    data_frame_ready_to_sql = convert_data_to_df(data)
    return data_frame_ready_to_sql


if __name__ == "__main__":
    while True:
        save_df_in_sqlite(download_station_info(), "replace", "stations_basic_info")
        save_df_in_sqlite(
            download_measurement_data(today=True), "append", "measurements"
        )
        sleep(3600)
