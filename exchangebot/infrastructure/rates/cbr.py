from datetime import datetime
from decimal import Decimal
from xml.etree import ElementTree

from aiohttp import ClientSession

from exchangebot.application.dto.rates import RatesReport, Rate
from exchangebot.application.exceptions import FailFetchRatesError
from exchangebot.application.interfaces.rates_repository import RatesFetcher

DEFAULT_CBR_RATES = "https://cbr.ru"


class CBRRatesFetcher(RatesFetcher):
    _session: ClientSession
    _last_fetch: datetime | None

    def __init__(
        self,
        session: ClientSession,
        cbr_host: str | None = None,
    ):
        self._session = session
        self.__rates_url = cbr_host or DEFAULT_CBR_RATES + "/scripts/XML_daily.asp"
        self._last_fetch = None

    async def fetch_rates(self) -> RatesReport:
        resp_body = None
        try:
            async with self._session.get(self.__rates_url) as resp:
                if not resp.ok:
                    raise FailFetchRatesError()
                resp_body = await resp.text()  # CP1251 gives from CBR

        except Exception as err:
            raise FailFetchRatesError() from err

        rates = self._parse_rates(resp_body)
        self._last_fetch = datetime.utcnow()
        return rates

    async def last_fetch_utc(self) -> datetime | None:
        return self._last_fetch

    @staticmethod
    def _parse_rates(body: str) -> RatesReport:
        root = ElementTree.fromstring(body)
        rates_date = datetime.strptime(root.get("Date"), "%d.%m.%Y").date()
        rates = [
            Rate(
                code=rate.find(CODE_KEY).text,
                name=rate.find(NAME_KEY).text,
                rate=Decimal(rate.find(RATE_KEY).text.replace(",", "."))
            )

            for rate in root
        ]
        return RatesReport(
            date=rates_date,
            rates=rates
        )


CODE_KEY = "CharCode"
NAME_KEY = "Name"
RATE_KEY = "VunitRate"
