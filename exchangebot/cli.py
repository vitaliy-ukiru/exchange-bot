import asyncio

import click
from aiogram import Bot
from dishka import make_async_container
from redis.asyncio import Redis

from exchangebot.infrastructure import logging
from exchangebot.infrastructure.di.provider import DIProvider
from exchangebot.presentation.telegram.main import create_dp


@click.group()
def cli():
    logging.setup()



async def _check_redis_connection(client: Redis):
    try:
        await client.ping()
    except Exception as err:
        raise ConnectionError("Failed connect to redis") from err


async def _main_polling(skip_updates: bool):
    container = make_async_container(DIProvider())
    await _check_redis_connection(await container.get(Redis))
    dp = create_dp(container)
    bot = await container.get(Bot)

    try:
        await dp.start_polling(bot, skip_updates=skip_updates)
    finally:
        await container.close()
        await bot.session.close()


@cli.command()
@click.option("--skip-updates", is_flag=True, default=False, help="Skip pending updates")
def polling(skip_updates: bool):
    asyncio.run(_main_polling(skip_updates))
