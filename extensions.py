import requests
import json

# переменную с валютами также помещает в данном файле, в целях избежания цикличного импорта
currency = {
    "ЕВРО": "EUR",
    "ДОЛЛАР": "USD",
    "РУБЛЬ": "RUB",
}


class CurrencyConverter:  # Класс, который содержит статический метод для конвертации
    @staticmethod
    def get_price(base: str, quote: str, amount: str) -> str:
        if base not in currency or quote not in currency:
            raise APIException("Неверно указана валюта. Пожалуйста, проверьте правильность ввода.")
        if quote == base:
            raise APIException(f'Невозможно перевести {base} в {quote}')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={currency[base]}&tsyms={currency[quote]}')
        response = json.loads(r.content)

        if currency[quote] not in response:
            raise APIException("Некорректный ответ от API. Пожалуйста, попробуйте позже.")

        rate = response[currency[quote]]
        converted_amount = rate * int(amount)
        return converted_amount


class APIException(Exception):  # собственный класс исключений при неверном вводе данных пользователем или ошибки API
    pass
