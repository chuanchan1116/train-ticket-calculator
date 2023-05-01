"""This module is used to query TRA info through https://tdx.transportdata.tw/
"""
#!/usr/bin/env python3

import logging
import sys
from dataclasses import dataclass

import requests
from rail_api_enum import TrainType


@dataclass
class TrainStation:
    """Base Class for train station data"""

    def __init__(self, station: dict) -> None:
        self.station_uid = station["StationUID"]
        self.station_id = station["StationID"]
        self.zh_station_name = station["StationName"]["Zh_tw"]
        self.en_station_name = station["StationName"]["En"]
        self.station_class = station["StationClass"]


@dataclass
class TrainStations:
    """Class for all stations"""

    def __init__(self, station_list: list) -> None:
        self._station_list = []
        self._name_mapping = {}
        for i in station_list:
            station = TrainStation(i)
            self._station_list.append(station)
            self._name_mapping[station.en_station_name] = station
            self._name_mapping[station.zh_station_name] = station

    def __getitem__(self, name: str) -> TrainStation:
        return self._name_mapping[name]


class RailApi:
    """Api Client for querying train information"""

    api_url = "https://tdx.transportdata.tw/api/basic/"
    auth_url = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"

    def __init__(self) -> None:
        self._get_auth()
        self._init_stations()

    def _get_auth(self):
        logging.debug("Authenticating...")
        self.access_token = ""

    def _init_stations(self):
        logging.debug("Getting Train Station Info")

        res = requests.get(
            self.api_url + "v3/Rail/TRA/Station",
            params={"$format": "json"},
            timeout=30,
        )
        if not res.ok:
            raise Exception(res.text)
        self._train_station_list = TrainStations(res.json()["Stations"])

    def get_stations(self) -> TrainStations:
        """Get all station info

        Returns:
            TrainStations: Train stations
        """
        return self._train_station_list

    def get_fares(self, sta1: TrainStation, sta2: TrainStation) -> list:
        """Get fare price between stations

        Args:
            sta1 (TrainStation): From staion
            sta2 (TrainStation): To staion

        Returns:
            list: Return a list of price fare
        """
        res = requests.get(
            self.api_url
            + f"v3/Rail/AFR/ODFare/{sta1.station_id}/to/{sta2.station_id}",
            params={"$filter": "Direction eq 0"},
            timeout=30,
        )
        if not res.ok:
            raise Exception(res.text)
        return res.json()["ODFares"]

    def get_fares_by_type(
        self, sta1: TrainStation, sta2: TrainStation, train_type: TrainType
    ) -> list:
        """Get fare list by certain train type

        Args:
            sta1 (TrainStation): from station
            sta2 (TrainStation): to station
            train_type (TrainType): Type of train

        Returns:
            list: Fare list
        """
        return [
            x
            for x in self.get_fares(sta1, sta2)
            if x["TrainType"] == train_type
        ]
