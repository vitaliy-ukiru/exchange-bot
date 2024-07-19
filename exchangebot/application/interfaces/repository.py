from abc import ABC, abstractmethod

from exchangebot.application import dto
from exchangebot.domain.entities import CurrencyRate


class CurrencyRateRepository(ABC):
    @abstractmethod
    async def save_currency_rate(self, currency: dto.Rate):
        raise NotImplementedError


class CurrencyRateFinder(ABC):
    @abstractmethod
    async def get_all_currencies_rates(self) -> list[CurrencyRate]:
        raise NotImplementedError

    @abstractmethod
    async def get_currency_rate(self, code: str) -> CurrencyRate | None:
        raise NotImplementedError
