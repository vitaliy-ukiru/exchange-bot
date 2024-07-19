from abc import ABC, abstractmethod
from decimal import Decimal

from exchangebot.domain.entities import CurrencyRate


class Usecase(ABC):
    @abstractmethod
    async def load_rates(self):
        raise NotImplementedError

    @abstractmethod
    async def convert_amount(
        self,
        source_currency_code: str,
        dest_currency_code: str,
        amount: Decimal
    ) -> Decimal:
        raise NotImplementedError

    @abstractmethod
    async def get_all_rates(self) -> list[CurrencyRate]:
        raise NotImplementedError
