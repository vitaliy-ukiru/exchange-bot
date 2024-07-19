from decimal import Decimal

from pydantic import BaseModel
from redis.asyncio import Redis

from exchangebot.application import dto
from exchangebot.application.interfaces import CurrencyRateFinder, CurrencyRateRepository
from exchangebot.domain.entities import CurrencyRate, CurrencyCode, Money, RUB_CURRENCY


class RateModel(BaseModel):
    code: str
    name: str
    rate: Decimal


class CurrencyRatesRepoImpl(CurrencyRateFinder, CurrencyRateRepository):
    def __init__(self, client: Redis, prefix: str):
        self.prefix = prefix
        self._client = client

    async def save_currency_rate(self, currency: dto.Rate):
        key = self._format_key(currency.code)
        data = convert_dto_to_model(currency)

        await self._client.set(key, data.model_dump_json())

    async def get_all_currencies_rates(self) -> list[CurrencyRate]:
        key = self._format_key("*")

        rates = [
            await self._iter_get_rate(key)
            async for key in self._client.scan_iter(key)
        ]

        return rates

    async def _iter_get_rate(self, key: str) -> CurrencyRate:
        data = await self._client.get(key)
        if data is None:
            raise KeyError("Fail get currency key in iter")

        model = RateModel.model_validate_json(data)

        return convert_model_to_entity(model)

    async def get_currency_rate(self, code: str) -> CurrencyRate | None:
        if code == "RUB":
            return RUB_CURRENCY

        key = self._format_key(code)

        data = await self._client.get(key)
        if not data:
            return None

        model = RateModel.model_validate_json(data)
        return convert_model_to_entity(model)

    def _format_key(self, code: str):
        return ':'.join((self.prefix, "rate", code))


def convert_dto_to_model(rate: dto.Rate) -> RateModel:
    return RateModel(
        code=rate.code,
        name=rate.name,
        rate=rate.rate,
    )


def convert_model_to_entity(rate: RateModel) -> CurrencyRate:
    return CurrencyRate(
        code=CurrencyCode(rate.code),
        title=rate.name,
        rate_to_rub=Money(rate.rate)
    )
