"""
    yandex_weather_api - Yandex Weather API python module

    Copyright 2018 Pavel Pletenev <cpp.create@gmail.com>
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
# pylint: disable=no-name-in-module,arguments-differ
import os
from textwrap import dedent
from pprint import pprint
import requests
import plumbum.cli
from plumbum.colors import green
from . import get, async_get


class Weather(plumbum.cli.Application):
    "Интерфейс командной строки для Яндекс.Погоды"
    def main(self):
        if not self.nested_command:
            raise RuntimeError("No command specified")


@Weather.subcommand('cli')
class WeatherCli(plumbum.cli.Application):
    """
    Интерфейс командной строки для Яндекс.Погоды

    Параметры lat и lon - широта и долгота точки, для которой будет
    запрошена погода.
    В среде выполнения должна быть установлена переменная среды YANDEX_API_KEY,
    содержащая ключ доступа к API.
    Также можно указать переменную среды YANDEX_WEATHER_RATE=forecast, если вы
    используете тариф "Тестовый".
    """
    def main(self, lat, lon):
        # pylint: disable=invalid-name
        api_key = os.environ.get("YANDEX_API_KEY")
        rate = os.environ.get("YANDEX_WEATHER_RATE", "informers")
        w = get(requests, api_key, rate=rate, lat=lat, lon=lon, limit=2)
        pprint(w)
        temp = green | (str(w.fact.temp) + '°C')
        print(dedent(f"""
        Температура { temp } (ощущается как {w.fact.feels_like}°C)
        За окном - {w.fact.condition}
        Ветер {w.fact.wind_dir} {w.fact.wind_speed} м/с
        Давление {w.fact.pressure_mm} мм.рт.ст.
        {w.fact.icon.as_url()}
        {w.info.url}
        """).strip())


def setup_client(app):
    # pylint: disable=missing-docstring
    from aiohttp import ClientSession

    async def on_startup(app):
        app["client_session"] = ClientSession()

    async def on_shutdown(app):
        await app["client_session"].close()

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)


@Weather.subcommand('server')
class WeatherWeb(plumbum.cli.Application):
    """
    Интерфейс командной строки для Яндекс.Погоды

    Запускает asyncio сервер на HTTP порте `port`,
    предоставляющий json-ответ прогноза по точке lat и lon (широта и долгота).
    В среде выполнения должна быть установлена переменная YANDEX_API_KEY,
    содержащая ключ доступа к API.
    Также можно указать переменную среды YANDEX_WEATHER_RATE=forecast, если вы
    используете тариф "Тестовый".
    """
    def main(self, lat, lon, port=8000):
        api_key = os.environ.get("YANDEX_API_KEY")
        rate = os.environ.get("YANDEX_WEATHER_RATE", "informers")

        from aiohttp import web
        routes = web.RouteTableDef()

        @routes.get('/')
        async def weather(request):  # pylint: disable=unused-variable
            return web.json_response(
                await async_get(
                    request.app["client_session"],
                    api_key, rate=rate, lat=lat, lon=lon
                )
            )
        app = web.Application()
        app.add_routes(routes)
        setup_client(app)
        web.run_app(app, port=port)


if __name__ == "__main__":
    Weather.run()
