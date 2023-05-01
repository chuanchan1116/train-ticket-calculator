"""Pytest for RailApi"""
import pytest
from rail_api import RailApi


@pytest.fixture()
def api_class():
    return RailApi()


def test_get_station_info(api_class):
    station = api_class.get_stations()
