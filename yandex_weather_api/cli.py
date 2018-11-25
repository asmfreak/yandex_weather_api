import os
from textwrap import dedent

import requests
import plumbum.cli
from plumbum.colors import green, red
from . import get, async_get

class Weather(plumbum.cli.Application):
    def main(self):
        if not self.nested_command:
            raise RuntimeError("No command specified")

@Weather.subcommand('cli')
class WeatherCli(plumbum.cli.Application):
    def main(self, lat, lon):
        if self.nested_command:
            return
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

def setup_client(app):
    from aiohttp import ClientSession
    async def on_startup(app):
        app["client_session"] = ClientSession()
    async def on_shutdown(app):
        await app["client_session"].close()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

@Weather.subcommand('server')
class WeatherWeb(plumbum.cli.Application):
    def main(self, lat, lon, port=8000):
        api_key = os.environ.get("YANDEX_API_KEY")
        rate = os.environ.get("YANDEX_WEATHER_RATE", "informers")

        from aiohttp import web
        routes = web.RouteTableDef()
        @routes.get('/')
        async def weather(request):
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
