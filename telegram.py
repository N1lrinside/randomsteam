import asyncio
import logging
import sys
from os import getenv
import re

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv('6864377086:AAHptfnSpDPnzRNDt4kaAwAW2oLIBRmH7zA')


# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!\n "
                         f"🎮 Добро пожаловать в бота  'Рандомная игра из библиотеки Steam!' 🎮\n"
                         f"Этот бот поможет вам выбрать, в какую игру поиграть из вашей коллекции в Steam. \
                         Просто отправьте команду /randomgame, \
                         и бот случайным образом выберет игру из вашей библиотеки.\n"
                         f"🔍 Как использовать: \n")

async def random(id_steam: str) -> str:
    return f'https://steamcommunity.com/id/{id_steam}'

@dp.message(commands=['start'])
async def randomgame(message: Message) -> None:
    await message.answer(f'{random(id_steam)}')

@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        if re.search(r'/id/', message.text):
            global id_steam
            id_steam = message.text[re.search(r'/id/', message.text).span()[1]:]
            await message.answer('ID успешно обработан')
        else:
            await message.reply('Неверная ссылка')
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")

@dp.message()
async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot('6864377086:AAHptfnSpDPnzRNDt4kaAwAW2oLIBRmH7zA', parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
