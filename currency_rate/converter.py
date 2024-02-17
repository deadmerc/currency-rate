import requests
from urllib.parse import urljoin, urlencode
import simplejson as json
from datetime import date
from typing import List

from pydantic import BaseModel

from .exceptions import InvalidCurrencyException, \
    InvalidDateException, \
    UnableConvertCurrencyException, \
    UnableGetSymbolsException, \
    UnableGetLatestRatesException


class RequestSession(requests.Session):
    def __init__(self):
        super().__init__()
        self.domain = 'https://currency.noxio.dev'

    def request(self, method, url, *args, **kwargs):
        return super().request(method, urljoin(self.domain, url), *args, **kwargs)


class Symbol(BaseModel):
    symbol: str
    title: str
    min_date: date = None
    max_date: date = None


class Symbols:
    _cache = None

    def __init__(self):
        self._load()

    def __iter__(self):
        return iter(self.list)

    def _load(self):
        with RequestSession() as session:
            res = session.get('/api/v1/currencies')
            if not res.status_code == 200:
                raise UnableGetSymbolsException()
            data = []
            symbols = res.json(cls=json.JSONDecoder)
            print(symbols)
            for symbol in symbols['data']:
                print(symbol)
                data.append(Symbol(**symbol))
            self._cache = data

    @property
    def list(self) -> List[Symbol]:
        if not self._cache:
            self._load()
        return self._cache

    def verify(self, symbol) -> bool:
        for currency in self:
            if currency.symbol == symbol:
                return True
        return False


class Converter:
    def __init__(self):
        self.symbols = Symbols()

    def latest(self):  # NOQA
        with RequestSession() as session:
            res = session.get(f"/api/v1/rates")
            if not res.status_code == 200:
                raise UnableGetLatestRatesException()
            data = res.json(cls=json.JSONDecoder)
            return data["rates"]

    def rate(self,
             currency_from: str,
             currency_to: str,
             amount: float = 1.0,
             at: date = False,
             verify: bool = True) -> float:
        if verify:
            if not self.symbols.verify(currency_from): raise InvalidCurrencyException(currency_from)  # NOQA: E701
            if not self.symbols.verify(currency_to): raise InvalidCurrencyException(currency_to)  # NOQA: E701
            if at and at > date.today(): raise InvalidDateException(at)  # NOQA: E701
        with RequestSession() as session:
            try:
                request_data = {"from": currency_from, "to": currency_to, "amount": amount}
                if at:
                    request_data["date"] = f"{at}"
                res = session.get(f"/api/v1/convert?{urlencode(request_data)}")
                assert res.status_code == 200
                data = json.loads(res.text, use_decimal=True)
                assert data["success"]
                return data["data"]["result"]
            except Exception as e:
                raise UnableConvertCurrencyException(e)


if __name__ == '__main__':
    c = Converter()
    print(c.symbols.list)
    rate = c.rate('USD', 'EUR', 1, date.today())
    print(f"Current rate USD -> EUR: {rate}")
