"""Pytest for RailApi"""
import argparse
import os

import pytest

from rail_api import RailApi


@pytest.fixture()
def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-id", default=os.environ.get("CLIENT_ID"))
    parser.add_argument(
        "--client-secret", default=os.environ.get("CLIENT_SECRET")
    )
    return parser.parse_args()


@pytest.fixture()
def api_class(args):
    return RailApi(args.client_id, args.client_secret)


def test_get_station_info(api_class):
    stations = api_class.get_stations()
    assert stations["臺北"].station_id == '1000'
