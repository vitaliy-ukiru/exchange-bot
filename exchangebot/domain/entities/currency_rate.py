from dataclasses import dataclass
from decimal import Decimal
from typing import NewType, Self

Money = NewType("Money", Decimal)
CurrencyCode = NewType("CurrencyCode", str)
RUB = CurrencyCode("RUB")


@dataclass(eq=False)
class CurrencyRate:
    code: CurrencyCode
    title: str
    rate_to_rub: Money

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, CurrencyRate):
            raise TypeError("Invalid type for check on equal")

        return self.code == other.code

    def in_rub(self, amount: Money) -> Money:
        """
        Convert amount from current currency to RUB currency.
        :param amount: Amount to convert
        :return: Amount in RUB
        """
        return self.rate_to_rub * amount

    def from_rub(self, amount: Money) -> Money:
        """
        Convert amount (RUB) to current currency
        :param amount: amount in RUB
        :return: Amount in current currency
        """
        return amount / self.rate_to_rub

    def convert(self, final_currency: Self, amount: Money) -> Money:
        """
        Converts money from self currency to final currency.
        If one of the currencies is not the RUB, then the convert takes place in two stages.
        First in rubles, then in the required currency.
        :param final_currency: Currency in which the amount will be converted
        :param amount: Amount in which the money will be converted from 'self'
        :return: Converted amount in 'final_currency'
        """

        # convert 'amount' from 'self' to 'final'

        # fast way, when it same currency
        if self == final_currency:
            return amount

        if self.code == RUB:
            return self.from_rub(amount)

        amount_in_rub = self.in_rub(amount)

        # convert from currency to rub
        if final_currency.code == RUB:
            return amount_in_rub

        # Otherwise first convert to rub, and after convert to final
        return final_currency.from_rub(amount_in_rub)


RUB_CURRENCY = CurrencyRate(RUB, "Российский рубль", Money(Decimal("1")))
