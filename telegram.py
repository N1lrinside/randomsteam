import asyncio
import logging
import sys
import re
from os import getenv
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from GameSteam import GameSteam
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="2005",
  database="databasename"
)

TOKEN = getenv('6864377086:AAHptfnSpDPnzRNDt4kaAwAW2oLIBRmH7zA')

dp = Dispatcher()

def random(id_steam: str) -> str:
    User = GameSteam(id_steam)
    game_id = User.random_games()
    User.get_state_about_achievements(game_id)
    return (f'Название игры: {User.name}\n'
            f'Кол-во выполненных достижений: {User.stats_achievement}\n'
            f'https://store.steampowered.com/app/{game_id}')

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!\n"
                         "🎮 Добро пожаловать в бота  'Рандомная игра из библиотеки Steam!' 🎮\n"
                         "Этот бот поможет вам выбрать, в какую игру поиграть из вашей коллекции в Steam.\n"
                         "Просто отправьте команду /randomgame, "
                         "и бот случайным образом выберет игру из вашей библиотеки.\n"
                         "Но перед этим отправьте ссылку на ваш аккаунт в стиме!" )

@dp.message(Command('randomgame'))
async def randomgame(message: Message) -> None:
    try:
        await message.answer("Анализирую библиотеку стим и подбираю игру")
        cursor = mydb.cursor()
        cursor.execute(f"SELECT steam_id FROM Steams_id WHERE id = {message.from_user.id}")
        id_steam = cursor.fetchall()
        await message.answer(f'{random(id_steam[0][0])}')
    except NameError:
        await message.answer('Вы еще не отправляли ссылку на стим профиль')

def random(id_steam: str) -> str:
    User = GameSteam(id_steam)
    return f'https://steamcommunity.com/id/{User.random_games()}'

@dp.message()
async def echo_handler(message: types.Message) -> None:
    try:
        if re.search(r'/id/', message.text) or re.search(r'/profiles/\d+', message.text):
            cursor = mydb.cursor()
            sql = "INSERT INTO Steams_id (id, steam_id) VALUES (%s, %s)"
            if re.search(r'/id/\w+', message.text) is None:
                User = GameSteam(re.search(r'/profiles/\d+', message.text).group()[10:])
                val = (message.from_user.id, User.user_id)
            else:
                User = GameSteam(re.search(r'/id/\w+', message.text).group()[4:])
                val = (message.from_user.id, User.user_id)
            try:
                cursor.execute(sql, val)
            except:
                sql = "UPDATE Steams_id SET steam_id = %s WHERE id = %s"
                val = (User.user_id, message.from_user.id)
                cursor.execute(sql, val)
            mydb.commit()
            await message.answer('ID успешно обработан')
        else:
            await message.reply('Неверная ссылка')
    except TypeError as err:
        print(err)
        await message.answer("Nice try!")

@dp.message()
async def main() -> None:
    bot = Bot('6864377086:AAHptfnSpDPnzRNDt4kaAwAW2oLIBRmH7zA', parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        mydb.close()
        print('Exit')