# yandex_weather_api

Библиотека для доступа к API Яндекс Погоды. Для работы с необходим ключ
[отсюда](https://developer.tech.yandex.ru/keys). Библиотека очень тонко
обрамляет JSON-ответ сервера Yandex для
[одного](https://tech.yandex.ru/weather/doc/dg/concepts/forecast-response-info-docpage/)
и [другого](https://tech.yandex.ru/weather/doc/dg/concepts/forecast-response-test-docpage/) тарифов.

Для запроса данных воспользуйтесь функциями
`get` и `async_get`.
Оба варианта принимают в качестве первого
аргумента объект сессии из библиотек `requests`
и `aiohttp` для выполнения синхронных или
асинхронных запросов соотвественно.

Погоду можно получать из командной строки, воспользовавшись утилитой yandex_weather_api. Запустите её с аргументом `--help`, чтобы получить информацию о том, какие подкомманды она подерживает.
