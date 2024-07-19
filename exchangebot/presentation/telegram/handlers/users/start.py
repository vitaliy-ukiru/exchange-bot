from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

start_router = Router()

START_TEXT = """This bot can exchange currencies by CBR rates.

Commands
/exchange {from} {to} {amount} - Converts <code> amount </code> 
Example: /exchange USD RUB 10 - Converts 10 USD to RUB

/rates - Get all available currency rates. 
"""


@start_router.message(Command("start", "help"))
async def start_handler(m: Message):
    await m.answer(START_TEXT)
