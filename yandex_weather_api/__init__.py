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
import voluptuous as vol
from .types import Enum, number, boolean, integer, WeatherAnswer


class Rate(Enum):
    "Тариф доступа. Возможные значения: "
    VALUES = (
        "informers",  # тариф «Погода на Вашем сайте»
        "forecast"    # тариф «Тестовый»
    )


class Language(Enum):
    "Язык ответа"
    VALUES = (
        "ru_RU",  # русский язык для домена России
        "ru_UA",  # русский язык для домена Украины
        "uk_UA",  # украинский язык для домена Украины
        "be_BY",  # белорусский язык для домена Беларуси
        "kk_KZ",  # казахский язык для домена Казахстана
        "tr_TR",  # турецкий язык для домена Турции
        "en_US"   # международный английский
    )


def stringify(schema):
    "Проверяет схему и преобразует полученное значение в строку"
    return lambda x: str(schema(x))


def lowcase_str_boolean(obj):
    "Делает из obj строку `true` или `false`"
    if isinstance(obj, str):
        if obj not in ["true", "false"]:
            raise RuntimeError(
                'Expecting "true" or "false", got {}'.format(obj))
        return obj
    return str(bool(obj)).lower()


ARGS_SCHEMA = vol.Schema({
    vol.Required("lat"): stringify(number),       # широта
    vol.Required("lon"): stringify(number),       # долгота
    vol.Optional("lang"): stringify(Language.validate)  # язык ответа
})


ARGS_FORECAST_SCHEMA = ARGS_SCHEMA.extend({
    vol.Optional("limit"): stringify(integer),  # срок прогноза
    vol.Optional("hours"): lowcase_str_boolean,  # наличие почасового прогноза
    vol.Optional("extra"): lowcase_str_boolean   # подробный прогноз осадков
})


def validate_args(api_key, *, rate="informers", **kwargs):
    "Проверяет и формирует аргументы для запроса"
    rate = Rate.validate(rate)
    headers = {"X-Yandex-API-Key": api_key}
    url = "https://api.weather.yandex.ru/v1/{}".format(rate)
    if rate == "informers":
        params = ARGS_SCHEMA(kwargs)
    else:
        params = ARGS_FORECAST_SCHEMA(kwargs)
    return (url,), {"headers": headers, "params": params}


def get(session, api_key, **kwargs):
    """
    Выполняет доступ к API.

    session - модуль requests или сессия из него
    api_key - строка ключа доступа к API
    rate - тариф, может быть `informers` или `forecast`
    lat, lon - широта и долгота

    ```
    import yandex_weather_api
    import requests as req

    yandex_weather_api.get(req, "ЗАМЕНИ_МЕНЯ_КЛЮЧОМ", lat=55.10, lon=60.10)
    ```
    """
    args, kwargs = validate_args(api_key, **kwargs)
    resp = session.get(*args, **kwargs)
    return WeatherAnswer.validate(resp.json())


async def async_get(session, api_key, **kwargs):
    """
    Выполняет асинхронный доступ к API.

    session - экземпляр объекта ClientSession из aiohttp
    api_key - строка ключа доступа к API
    rate - тариф, может быть `informers` или `forecast`
    lat, lon - широта и долгота
    """
    args, kwargs = validate_args(api_key, **kwargs)
    resp = await session.get(*args, **kwargs)
    return WeatherAnswer.validate(await resp.json())
