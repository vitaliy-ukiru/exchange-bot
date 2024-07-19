from aiogram import Dispatcher
from dishka import AsyncContainer
from dishka.integrations.aiogram import setup_dishka

from exchangebot.presentation.telegram.handlers.users.exchange import exchange_router


def create_dp(
    container: AsyncContainer,
) -> Dispatcher:
    dp = Dispatcher(disable_fsm=True)  # don't set storage, because we don't need fsm
    dp.include_router(exchange_router)
    setup_dishka(container, dp)
    return dp
