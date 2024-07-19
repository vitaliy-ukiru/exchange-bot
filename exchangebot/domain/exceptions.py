from dataclasses import dataclass
from typing import ClassVar


@dataclass(eq=False)
class AppError(Exception):
    """Base Error."""

    code: ClassVar[str] = "APP_ERROR"

    @property
    def title(self) -> str:
        return "An app error occurred"
