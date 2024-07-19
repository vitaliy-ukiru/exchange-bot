from _decimal import Decimal
from datetime import datetime, timedelta

from exchangebot.application.exceptions import CurrencyNotFound
from exchangebot.application.interfaces import RatesFetcher, CurrencyRateRepository, Usecase, \
    CurrencyRateFinder
from exchangebot.domain.entities import CurrencyRate, Money


class Service(Usecase):
    def __init__(
        self,
        fetcher: RatesFetcher,
        repository: CurrencyRateRepository,
        finder: CurrencyRateFinder,
        min_duration_between_fetch: timedelta,
    ):
        self._min_duration_between_fetch = min_duration_between_fetch
        self._repo = repository
        self._fetcher = fetcher
        self._finder = finder

    async def load_rates(self):
        report = await self._fetcher.fetch_rates()
        for rate in report.rates:
            await self._repo.save_currency_rate(rate)

    async def _can_reload_rates(self) -> bool:
        now = datetime.utcnow()
        last_fetch = await self._fetcher.last_fetch_utc()
        if not last_fetch:
            return True

        return now - last_fetch > self._min_duration_between_fetch

    async def _get_currency(self, code: str) -> CurrencyRate:
        if rate := await self._finder.get_currency_rate(code):
            return rate

        # We can not find currency for 2 major reasons:
        # 1. User inputs currency that not exists in CBR list
        # 2. Currency not loaded to DB.
        # Second version may appear because application didn't have time to load
        # list, and it needs force load.
        if await self._can_reload_rates():
            await self.load_rates()

        rate = await self._finder.get_currency_rate(code)
        if not rate:
            raise CurrencyNotFound(code)

        return rate

    async def convert_amount(self, source_currency_code: str, dest_currency_code: str,
                             amount: Decimal) -> Decimal:
        from_rate = await self._get_currency(source_currency_code)
        to_rate = await self._get_currency(dest_currency_code)

        amount = Money(amount)

        return from_rate.convert(to_rate, amount)

    async def get_all_rates(self) -> list[CurrencyRate]:
        rates = await self._finder.get_all_currencies_rates()
        if rates:
            return rates

        await self.load_rates()
        return await self._finder.get_all_currencies_rates()
