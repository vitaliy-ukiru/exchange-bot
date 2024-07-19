from datetime import timedelta
from typing import AsyncIterable

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiohttp import ClientSession
from dishka import Provider, provide, Scope, AnyOf
from redis.asyncio import Redis

from exchangebot.application.interfaces import CurrencyRateFinder, CurrencyRateRepository, Usecase
from exchangebot.application.interfaces.rates_repository import RatesFetcher
from exchangebot.application.service import Service
from exchangebot.config import Config
from exchangebot.infrastructure.rates.cbr import CBRRatesFetcher
from exchangebot.infrastructure.repository.redis_repo import CurrencyRatesRepoImpl


class DIProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> Config:
        return Config()

    @provide(scope=Scope.APP)
    def get_bot(self, cfg: Config) -> Bot:
        return Bot(
            token=cfg.bot_token.get_secret_value(),
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML
            ),
        )

    @provide(scope=Scope.APP)
    async def get_redis_client(self, cfg: Config) -> AsyncIterable[Redis]:
        client = Redis.from_url(cfg.redis_url.unicode_string())
        yield client

        await client.aclose()

    @provide(scope=Scope.APP)
    def get_fsm_storage(self, client: Redis) -> BaseStorage:
        storage = RedisStorage(redis=client)
        # don't close storage, because it already will close in redis provider
        return storage

    @provide(scope=Scope.APP)
    async def get_cbr_fetcher(self) -> AsyncIterable[RatesFetcher]:
        async with ClientSession() as session:
            fetcher = CBRRatesFetcher(session)
            yield fetcher

    @provide(scope=Scope.APP)  # make sense change to request
    async def get_rates_repo(
        self,
        client: Redis,
        cfg: Config,
    ) -> AnyOf[CurrencyRateFinder, CurrencyRateRepository]:
        return CurrencyRatesRepoImpl(
            client,
            cfg.redis_prefix,
        )

    @provide(scope=Scope.APP)
    async def get_usecase(
        self,
        finder: CurrencyRateFinder,
        repo: CurrencyRateRepository,
        fetcher: RatesFetcher,
        cfg: Config,
    ) -> Usecase:
        return Service(
            fetcher=fetcher,
            repository=repo,
            finder=finder,
            min_duration_between_fetch=timedelta(minutes=cfg.force_reload_rates_minutes)
        )
