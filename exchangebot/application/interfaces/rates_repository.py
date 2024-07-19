from abc import ABC, abstractmethod
from datetime import datetime

from exchangebot.application import dto


class RatesFetcher(ABC):
    @abstractmethod
    async def last_fetch_utc(self) -> datetime | None:
        raise NotImplementedError

    @abstractmethod
    async def fetch_rates(self) -> dto.RatesReport:
        raise NotImplementedError
