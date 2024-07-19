from dataclasses import dataclass

from exchangebot.domain.exceptions import AppError


class ApplicationError(AppError):
    """Base Application Exception."""

    @property
    def title(self) -> str:
        return "An application error occurred"


class FailFetchRatesError(AppError):
    code = "FAIL_FETCH_RATES"

    @property
    def title(self) -> str:
        return "Fail fetch currency rates"


@dataclass(eq=False)
class CurrencyNotFound(AppError):
    currency: str

    code = "CURRENCY_NOT_FOUND"

    @property
    def title(self) -> str:
        return f"Currency {self.currency} not found"
