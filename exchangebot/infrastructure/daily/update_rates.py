from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dishka import AsyncContainer
from loguru import logger

from exchangebot.application.interfaces import Usecase
from exchangebot.config import Config


async def bind_daily_task(scheduler: AsyncIOScheduler, container: AsyncContainer):
    cfg = await container.get(Config)
    scheduler.add_job(
        update_rates_cron,
        trigger=CronTrigger.from_crontab(cfg.update_rates_cron), args=(container,),
    )

async def update_rates_cron(container: AsyncContainer):
    async with container() as c_request:
        logger.info("scheduled update rates")
        uc = await c_request.get(Usecase)
        await uc.load_rates()
