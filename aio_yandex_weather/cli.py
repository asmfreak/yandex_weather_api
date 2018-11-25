import os
from textwrap import dedent

import requests
import plumbum.cli
from plumbum.colors import green, red
from . import get


class Weather(plumbum.cli.Application):
    def main(self, lat, lon):
        api_key = os.environ.get("YANDEX_API_KEY")
        rate = os.environ.get("YANDEX_WEATHER_RATE", "informers")
        w = get(requests, api_key, rate=rate, lat=lat, lon=lon)
        print(dedent(f"""
        Температура { green | (str(w.fact.temp) + '°C')} (ощущается как {w.fact.feels_like}°C)
        За окном - {w.fact.condition}
        Ветер {w.fact.wind_dir} {w.fact.wind_speed} м/с
        Давление {w.fact.pressure_mm} мм.рт.ст.
        {w.fact.icon.as_url()}
        {w.info.url}
        """).strip())

if __name__ == "__main__":
    Weather.run()
