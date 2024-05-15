import re
from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.utils.markdown import hbold
from app.GameSteam import GameSteam
from app.others import mydb, random
import mysql.connector

button_hello = InlineKeyboardButton(text="Подобрать игру", callback_data="randomgame")

row = [button_hello]

inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[row])

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!\n"
                         "🎮 Добро пожаловать в бота  'Рандомная игра из библиотеки Steam!' 🎮\n"
                         "Этот бот поможет вам выбрать, в какую игру поиграть из вашей коллекции в Steam.\n"
                         "Просто отправьте команду /randomgame, "
                         "и бот случайным образом выберет игру из вашей библиотеки.\n"
                         "Но перед этим отправьте ссылку на ваш аккаунт в стиме!", reply_markup=inline_keyboard)


@router.callback_query(F.data == 'randomgame')
async def randomgame(callback: types.CallbackQuery) -> None:
    kb = [
        [
            types.KeyboardButton(text="Спасибо!")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )

    try:
        await callback.message.answer("Анализирую библиотеку стим и подбираю игру")
        cursor = mydb.cursor()
        cursor.execute(f"SELECT steam_id FROM Steams_id WHERE id = {callback.from_user.id}")
        id_steam = cursor.fetchall()
        await callback.message.answer(f'{random(id_steam[0][0])}', reply_markup=keyboard)
    except NameError:
        await callback.message.answer('Вы еще не отправляли ссылку на стим профиль')


@router.message(F.text.lower() == "спасибо!")
async def answer(message: types.Message) -> None:
    await message.reply('Не за что! Обращайтесь ещё', reply_markup=inline_keyboard)


@router.message()
async def echo_handler(message: types.Message) -> None:
    try:
        if re.search(r'/id/', message.text) or re.search(r'/profiles/\d+', message.text):
            cursor = mydb.cursor()
            sql = "INSERT INTO Steams_id (id, steam_id) VALUES (%s, %s)"
            if re.search(r'/id/\w+', message.text) is None:
                user = GameSteam(re.search(r'/profiles/\d+', message.text).group()[10:])
                val = (message.from_user.id, user.user_id)
            else:
                user = GameSteam(re.search(r'/id/\w+', message.text).group()[4:])
                val = (message.from_user.id, user.user_id)
            try:
                cursor.execute(sql, val)
            except mysql.connector.errors.IntegrityError:
                sql = "UPDATE Steams_id SET steam_id = %s WHERE id = %s"
                val = (user.user_id, message.from_user.id)
                cursor.execute(sql, val)
            mydb.commit()
            await message.answer('ID успешно обработан')
        else:
            await message.reply('Неверная ссылка')
    except TypeError as err:
        print(err)
        await message.answer("Nice try!")
