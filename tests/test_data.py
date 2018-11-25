import json
from aio_yandex_weather.types import *
import os

t = os.path.join(os.path.dirname(__file__), "request_testing.json")

with open(t) as f:
    data = json.load(f)

wa = WeatherAnswer.validate(data)
assert(wa.forecast == wa.forecasts)
