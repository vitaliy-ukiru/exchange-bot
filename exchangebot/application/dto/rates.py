import datetime
from dataclasses import dataclass
from decimal import Decimal

from exchangebot.application.dto.base import DTO

@dataclass(frozen=True)
class Rate(DTO):
    code: str
    name: str
    rate: Decimal


@dataclass(frozen=True)
class RatesReport(DTO):
    date: datetime.date
    rates: list[Rate]
