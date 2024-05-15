import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from app.handlers import router
from app.others import mydb

async def main() -> None:
    bot = Bot('6864377086:AAHptfnSpDPnzRNDt4kaAwAW2oLIBRmH7zA', parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        mydb.close()
        print('Exit')