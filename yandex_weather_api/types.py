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
from typing import Tuple, Union, Sequence, TypeVar

import voluptuous as vol
from box import Box


# typing typevar
T = TypeVar('T')  # pylint: disable=invalid-name


def ensure_list(value: Union[T, Sequence[T]]) -> Sequence[T]:
    """Wrap value in list if it is not one."""
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def ensure_list_of(validator):
    """Wrap value if it is not one, and run validator in each item."""
    return lambda value: list(validator(y) for y in ensure_list(value))


def number(num):
    "Валидатор для объектов, приводимых к float"
    return float(num)


def integer(num):
    "Валидатор для объектов, приводимых к int"
    return int(num)


def boolean(num):
    "Валидатор для объектов, приводимых к булеву типу"
    return bool(num)


class Enum(str):
    "Тип-перечисление с валидатором"
    VALUES = ()  # type: Tuple[str, ...]

    @classmethod
    def validate(cls, cnd):
        "Проверяет, что переданный объект - один из возможных `VALUES`"
        if cnd not in cls.VALUES:
            raise ValueError("Value {} cannot be used in {}".format(
                cnd, cls
            ))
        return cls(cnd)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, super().__repr__())


class Condition(Enum):
    "Текущее состояние погоды"
    VALUES = (
        "clear",  # ясно
        "partly-cloudy",  # малооблачно
        "cloudy",  # облачно с прояснениями
        "overcast",  # пасмурно
        "partly-cloudy-and-light-rain",  # небольшой дождь
        "partly-cloudy-and-rain",  # дождь
        "overcast-and-rain",  # сильный дождь
        "overcast-thunderstorms-with-rain",  # сильный дождь, гроза
        "cloudy-and-light-rain",  # небольшой дождь
        "overcast-and-light-rain",  # небольшой дождь
        "cloudy-and-rain",  # дождь
        "overcast-and-wet-snow",  # дождь со снегом
        "partly-cloudy-and-light-snow",  # небольшой снег
        "partly-cloudy-and-snow",  # снег
        "overcast-and-snow",  # снегопад
        "cloudy-and-light-snow",  # небольшой снег
        "overcast-and-light-snow",  # небольшой снег
        "cloudy-and-snow",  # снег
    )


class WindDir(Enum):
    "Направление ветра"
    VALUES = (
        "nw",  # северо-западное
        "n",  # северное
        "ne",  # северо-восточное
        "e",  # восточное
        "se",  # юго-восточное
        "s",  # южное
        "sw",  # юго-западное
        "w",  # западное
        "c"   # штиль
    )


class Season(Enum):
    "Время года"
    VALUES = (
        "summer",  # лето
        "autumn",  # осень
        "winter",  # зима
        "spring"   # весна
    )


class Daytime(Enum):
    "Время суток"
    VALUES = (
        "d",  # светлое время суток
        "n",  # темное время суток
    )


class Icon(str):
    """
    Код иконки погоды. Иконка доступна по адресу
    https://yastatic.net/weather/i/icons/blueye/color/svg/
    <значение из поля icon>.svg. 	Строка
    """
    URL_FORMAT = "https://yastatic.net/weather/i/icons/blueye/color/svg/{}.svg"
    @classmethod
    def validate(cls, cnd):
        "Проверяет правильность данного объекта"
        return cls(cnd)

    def as_url(self):
        "Выдаёт ссылку на значок погоды"
        return self.URL_FORMAT.format(self)


class BoxWithSchema(Box):
    """
    Коробка, которая может проверить валидность входных данных
    на соответсвие схеме SCHEMA, которую должны предоставить потомки
    """
    @classmethod
    def validate(cls, obj):
        "Проверяет схему SCHEMA на объекте obj и создаёт коробку"
        return cls(cls.SCHEMA(obj))


class TZInfo(BoxWithSchema):
    "Информация о часовом поясе. Содержит поля offset, name, abbr и dst."
    SCHEMA = vol.Schema({
        # Часовой пояс в секундах от UTC. 	Число
        vol.Optional("offset"): number,
        # Название часового пояса. 	Строка
        vol.Optional("name"): str,
        # Сокращенное название часового пояса. 	Строка
        vol.Optional("abbr"): str,
        # Признак летнего времени. 	Логический
        vol.Optional("dst"): bool
    })


class Info(BoxWithSchema):
    """
    Объект info

    Объект содержит информацию о населенном пункте.
    """
    SCHEMA = vol.Schema({
        # Широта (в градусах). Число
        vol.Required("lat"): number,
        # Долгота (в градусах). Число
        vol.Required("lon"): number,
        # Идентификатор населенного пункта. 	Число
        vol.Optional("geoid"): number,
        # URL-путь на странице https://yandex.TLD/pogoda/. 	Строка
        vol.Optional("slug"): str,
        # Информация о часовом поясе. Содержит поля offset, name, abbr и dst.
        vol.Optional("tzinfo"): TZInfo.validate,
        # Норма давления для данной координаты (в мм рт. ст.). 	Число
        vol.Optional("def_pressure_mm"): number,
        # Норма давления для данной координаты (в гектопаскалях). 	Число
        vol.Optional("def_pressure_pa"): number,
        # Страница населенного пункта на сайте Яндекс.Погода. Строка
        vol.Required("url"): str

    }, extra=vol.ALLOW_EXTRA)


class FacticalWeatherInfo(BoxWithSchema):
    """
    Объект fact

    Объект содержит информацию о погоде на данный момент.
    """
    SCHEMA = vol.Schema({
        # Температура (°C). 	Число
        vol.Required("temp"): number,
        # Ощущаемая температура (°C). 	Число
        vol.Required("feels_like"): number,
        # Температура воды (°C).
        # Параметр возвращается для населенных пунктов,
        # где данная информация актуальна. 	Число
        vol.Optional("temp_water"): number,
        # Код иконки погоды. Иконка доступна по адресу
        # https://yastatic.net/weather/i/icons/blueye/color/svg/
        # <значение из поля icon>.svg. 	Строка
        vol.Required("icon"): Icon.validate,
        # Код расшифровки погодного описания. Возможные значения:
        vol.Required("condition"): Condition.validate,
        # Скорость ветра (в м/с). Число
        vol.Required("wind_speed"): number,
        # Скорость порывов ветра (в м/с). 	Число
        vol.Required("wind_gust"): number,
        # Направление ветра. Возможные значения:
        vol.Required("wind_dir"): WindDir.validate,
        # Давление (в мм рт. ст.). Число
        vol.Required("pressure_mm"): number,
        # Давление (в гектопаскалях). Число
        vol.Required("pressure_pa"): number,
        # Влажность воздуха (в процентах). Число
        vol.Required("humidity"): number,
        # Светлое или темное время суток. Возможные значения:
        vol.Required("daytime"): Daytime.validate,
        # Признак полярного дня или ночи. 	Логический
        vol.Required("polar"): bool,
        # Время года в данном населенном пункте. Возможные значения:
        vol.Required("season"): Season.validate,
        # Время замера погодных данных в формате Unixtime. 	Число
        vol.Required("obs_time"): number,
        # Тип осадков. Возможные значения: 	Число
        # 0 — без осадков.
        # 1 — дождь.
        # 2 — дождь со снегом.
        # 3 — снег.
        vol.Optional("prec_type"): number,
        # Сила осадков. Возможные значения: 	Число
        # 0 — без осадков.
        # 0.25 — слабый дождь/слабый снег.
        # 0.5 — дождь/снег.
        # 0.75 — сильный дождь/сильный снег.
        # 1 — сильный ливень/очень сильный снег.
        vol.Optional("prec_strength"): number,
        # Облачность. Возможные значения: 	Число
        # 0 — ясно.
        # 0.25 — малооблачно.
        # 0.5 — облачно с прояснениями.
        # 0.75 — облачно с прояснениями.
        # 1 — пасмурно.
        vol.Optional("cloudness"): number,
    }, extra=vol.ALLOW_EXTRA)


class MoonText(Enum):
    "Код фазы Луны. Возможные значения:"
    VALUES = (
        "full-moon",  # полнолуние
        "decreasing-moon",  # убывающая Луна
        "last-quarter",  # последняя четверть
        "new-moon",  # новолуние
        "growing-moon",  # растущая Луна
        "first-quarter",  # первая четверть
    )


class PartName(Enum):
    "Название времени суток. Возможные значения:"
    VALUES = (
        "night",  # ночь
        "morning",  # утро
        "day",  # день
        "evening",  # вечер
    )


class ForecastPart(BoxWithSchema):
    """
    Все прогнозы погоды на время суток имеют одинаковый набор полей.

    Ответ содержит прогноз на 2 ближайших периода.
    """
    SCHEMA = vol.Schema({
        # Название времени суток. Возможные значения: 	Строка
        vol.Optional("part_name"): PartName.validate,
        # Минимальная температура для времени суток (°C). 	Число
        vol.Required("temp_min"): number,
        # Максимальная температура для времени суток (°C). 	Число
        vol.Required("temp_max"): number,
        # Средняя температура для времени суток (°C). 	Число
        vol.Required("temp_avg"): number,
        # Ощущаемая температура (°C). 	Число
        vol.Required("feels_like"): number,
        # Код иконки погоды. Иконка доступна по адресу
        # https://yastatic.net/weather/i/icons/blueye/color/svg/
        # <значение из поля icon>.svg. 	Строка
        vol.Required("icon"): Icon.validate,
        # Код расшифровки погодного описания. Возможные значения: 	Строка
        vol.Required("condition"): Condition.validate,
        # Светлое или темное время суток. Возможные значения: 	Строка
        vol.Required("daytime"): Daytime.validate,
        # Признак полярного дня или ночи. 	Логический
        vol.Required("polar"): bool,
        # Скорость ветра (в м/с). 	Число
        vol.Required("wind_speed"): number,
        # Скорость порывов ветра (в м/с). 	Число
        vol.Required("wind_gust"): number,
        # Направление ветра. Возможные значения: 	Строка
        vol.Required("wind_dir"): WindDir.validate,
        # Давление (в мм рт. ст.). 	Число
        vol.Required("pressure_mm"): number,
        # Давление (в гектопаскалях). 	Число
        vol.Required("pressure_pa"): number,
        # Влажность воздуха (в процентах). 	Число
        vol.Required("humidity"): number,
        # Прогнозируемое количество осадков (в мм). 	Число
        vol.Required("prec_mm"): number,
        # Прогнозируемый период осадков (в минутах). 	Число
        vol.Required("prec_period"): number,
        # Вероятность выпадения осадков. 	Число
        vol.Required("prec_prob"): number,
    }, extra=vol.ALLOW_EXTRA)


BASE_FORECAST_SCHEMA = vol.Schema({
    # Дата прогноза в формате ГГГГ-ММ-ДД. 	Строка
    vol.Required("date"): str,
    # Дата прогноза в формате Unixtime. 	Число
    vol.Required("date_ts"): number,
    # Порядковый номер недели. 	Число
    vol.Required("week"): int,
    # Время восхода Солнца, локальное время (может отсутствовать
    # для полярных регионов). Строка
    vol.Required("sunrise"): str,
    # Время заката Солнца, локальное время (может отсутствовать
    # для полярных регионов). 	Строка
    vol.Required("sunset"): str,
    # Код фазы Луны. Возможные значения: 	Число
    # 0 — полнолуние.
    # 1-3 — убывающая Луна.
    # 4 — последняя четверть.
    # 5-7 — убывающая Луна.
    # 8 — новолуние.
    # 9-11 — растущая Луна.
    # 12 — первая четверть.
    # 13-15 — растущая Луна.
    vol.Required("moon_code"): int,
    # Текстовый код для фазы Луны. Возможные значения: 	Строка
    vol.Required("moon_text"): MoonText.validate,
}, extra=vol.ALLOW_EXTRA)


class Forecast(BoxWithSchema):
    """
    Объект forecast

    Объект содержит данные прогноза погоды при использовании тарифа
    "Для сайтов". Переформирует данные в соответсвии с тарифом "Тестовый"
    """

    SCHEMA = BASE_FORECAST_SCHEMA.extend({
        # Прогнозы по времени суток. Содержит следующие поля: 	Объект
        vol.Required("parts"): [ForecastPart.validate]
    })

    @classmethod
    def validate(cls, obj):
        ret = super().validate(obj)
        parts = {}
        for part in ret.parts:
            parts[part.part_name] = part
        ret.parts = Box(parts)
        return ret


class Forecasts(BoxWithSchema):
    """
    Объект forecast

    Объект содержит данные прогноза погоды для тарифа "Тестовый"
    """
    SCHEMA = BASE_FORECAST_SCHEMA.extend({
        # Прогнозы по времени суток. Содержит следующие поля: 	Объект
        vol.Required("parts"): {
            vol.Required(key): ForecastPart.validate for key in PartName.VALUES
        },
    })


class WeatherAnswer(BoxWithSchema):
    """
    Ответ для тарифа «Погода на вашем сайте»

    Ответ на запрос `Фактическое значение и прогноз погоды` возвращается
    в формате JSON. Информация в ответе содержит:
    """
    SCHEMA = vol.Schema({
        # Время сервера в формате Unixtime. Числ
        vol.Required("now"): number,
        # Время сервера в UTC. Строка
        vol.Optional("now_dt"): str,
        # Объект информации о населенном пункте. Объект
        vol.Required("info"): Info.validate,
        # Объект фактической информации о погоде. Объект
        vol.Required("fact"): FacticalWeatherInfo.validate,
        # Объект прогнозной информации о погоде. Объект
        vol.Exclusive("forecast", "forecast"):
            ensure_list_of(Forecast.validate),
        vol.Exclusive("forecasts", "forecast"): [Forecasts.validate]
    }, extra=vol.ALLOW_EXTRA)

    @classmethod
    def validate(cls, obj):
        ret = super().validate(obj)
        if "forecasts" in ret:
            ret.forecast = ret.forecasts
        else:
            ret.forecasts = ret.forecast
        return ret
