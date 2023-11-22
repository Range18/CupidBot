import sys

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
import asyncio
from config import TOKEN
import logging

loop = asyncio.get_event_loop()
bot = Bot(token=TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(loop=loop, storage=storage)


async def main(dispatcher: Dispatcher) -> None:
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    from bot import dp
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main(dp))
