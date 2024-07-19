from decimal import Decimal, InvalidOperation

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.utils.formatting import Code, Text, as_list as fmt_as_list
from dishka.integrations.aiogram import FromDishka, inject

from exchangebot.application.interfaces import Usecase
from exchangebot.domain.entities import CurrencyRate

exchange_router = Router(name="exchange")

DEC_EXP = Decimal("1.0000")


@exchange_router.message(Command("exchange"))
@inject
async def exchange_cmd(
    m: Message,
    command: CommandObject,
    usecase: FromDishka[Usecase],
):
    args = command.args.split(' ')
    if len(args) != 3:
        await m.answer("Usage: /exchange <from> <to> <amount>", parse_mode=ParseMode.MARKDOWN)
        return

    from_currency, to_currency, amount = args
    try:
        amount = Decimal(amount)
    except InvalidOperation:
        await m.answer("Amount must be valid decimal number")
        return

    converted_amount = await usecase.convert_amount(
        from_currency, to_currency, amount
    )

    await m.answer(f'{converted_amount.quantize(DEC_EXP)} {to_currency}')


@exchange_router.message(Command("rates"))
@inject
async def rates_cmd(m: Message, usecase: FromDishka[Usecase]):
    rates = await usecase.get_all_rates()

    result = fmt_as_list(
        *map(_convert_currency_rate_to_str, rates),
        sep="\n\n"
    )

    await m.answer(**result.as_kwargs())


def _convert_currency_rate_to_str(rate: CurrencyRate) -> Text:
    return Text(
        rate.title,
        " - ",
        Code(rate.code),
        " - ",
        Code(rate.rate_to_rub.quantize(DEC_EXP))
    )
