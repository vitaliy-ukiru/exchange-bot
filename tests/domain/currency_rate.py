from decimal import Decimal

import pytest

from exchangebot.domain.entities import CurrencyRate, CurrencyCode, Money, RUB_CURRENCY


@pytest.fixture
def usd_rate():
    return CurrencyRate(
        code=CurrencyCode("USD"),
        title="USD",
        rate_to_rub=Money(Decimal(88))
    )

def test_convert_rub_to_usd(usd_rate):
    one_dollar = RUB_CURRENCY.convert(usd_rate, Money(Decimal(88)))

    assert one_dollar == Money(Decimal(1))

def test_convert_to_usd_rub(usd_rate):
    rubles = usd_rate.convert(RUB_CURRENCY, Money(Decimal(1)))

    assert rubles == Money(Decimal(88))


