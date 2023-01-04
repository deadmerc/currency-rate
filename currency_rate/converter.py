import requests
from incremental import Version
from urllib.parse import urljoin, urlencode
import simplejson as json
from datetime import date

__version__ = Version('CurrencyRate', 0, 1, 0)


class InvalidCurrencyException(Exception):
    pass


class InvalidDateException(Exception):
    pass


class UnableConvertCurrencyException(Exception):
    pass


class RequestSession(requests.Session):
    def __init__(self):
        super().__init__()
        self.domain = 'https://api.exchangerate.host'

    def request(self, method, url, *args, **kwargs):
        return super().request(method, urljoin(self.domain, url), *args, **kwargs)


class Symbols:
    _cache = None

    def __init__(self):
        self._load()

    def _load(self):
        with RequestSession() as session:
            res = session.get('/symbols')
            if res.status_code == 200:
                self._cache = json.loads(res.text)['symbols']

    @property
    def list(self):
        if not self._cache:
            self._load()
        return self._cache

    def verify(self, ticker) -> bool:
        if ticker in self.list:
            return True
        return False


class Converter:
    def __init__(self):
        self.symbols = Symbols()

    def latest(self, currency_base='USD'):
        with RequestSession() as session:
            res = session.get(f"/latest?base={currency_base}")
            if res.status_code == 200:
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
            request_data = {"from": currency_from, "to": currency_to, "amount": amount}
            if at:
                request_data["date"] = f"{at}"
            res = session.get(f"/convert?{urlencode(request_data)}")
            if res.status_code == 200:
                data = json.loads(res.text, use_decimal=True)
                if "success" in data and data['success'] and "result" in data:
                    value = data["result"]
                    return value
            raise UnableConvertCurrencyException()


if __name__ == '__main__':
    c = Converter()
    rate = c.rate('USD', 'EUR', 1, date.today())
    print(f"Current rate USD -> EUR: {rate}")
