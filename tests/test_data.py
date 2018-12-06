import json
import os

import pytest

from yandex_weather_api.types import *


def get_test_data(name):
    t = os.path.join(os.path.dirname(__file__), name)
    with open(t) as f:
        data = json.load(f)
    return data

@pytest.fixture
def forecast():
    return get_test_data("request_testing.json")

@pytest.fixture
def informers():
    return get_test_data("request_informers.json")

def test_informers(informers):
    wa = WeatherAnswer.validate(informers)
    assert(wa.forecast == wa.forecasts)

def test_forecast(forecast):
    wa = WeatherAnswer.validate(forecast)
    assert(wa.forecast == wa.forecasts)
