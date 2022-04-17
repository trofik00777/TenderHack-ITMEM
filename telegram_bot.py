#!venv/bin/python
# import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types

from Regulator import Regulator
from System import System
from config import BOT_TOKEN, DEFAULT_PRICE, DEFAULT_TIME

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

USERS = dict()  # id_user : Regulator()


async def set_default_commands():
    await bot.set_my_commands([
        types.BotCommand("/start", "Запустить бота"),
        types.BotCommand("/help", "Помощь"),
        types.BotCommand("/add", "Добавить бота в сессию"),
        types.BotCommand("/del", "Удалить бота из сессии"),
        types.BotCommand("/getActive", "Текущие сессии"),
    ])


@dp.message_handler(commands="help")
async def help(message: types.Message):
    commands = [["help", "(Помощь)"],
                ["login <login> <password> <email>", "(Вход в систему)"],
                ["add <id сессии>", "(Добавить бота в сессию)"],
                ["del <id сессии>", "(Удалить бота из сессии)"],
                # ["menu_bots", "(Управление ботами)"],
                ["get_active", "(Список текущих сессий)"]]

    text = []
    for comm, desc in commands:
        decript = desc.replace('(', r'\(').replace(')', r'\)')
        text.append(fr"`/{comm}` \-\- _{decript}_")
    await message.answer('\n'.join(text), parse_mode="MarkDownV2")


@dp.message_handler(commands="get_active")  # coming soon
async def get_active(message: types.Message):
    user_id = message.from_user.id
    if user_id in USERS:
        regulator = USERS[user_id]
        regulator.getactivities()

        # await message.reply(f"Бот успешно добавлен в сессию `id={id}`!", parse_mode="MarkDownV2")
    else:
        await message.reply(r"Для начала зарегистрируйтесь\! Используйте команду `/login <login> <password> <email>`",
                            parse_mode="MarkDownV2")


@dp.message_handler(commands="login")
async def login(message: types.Message):
    # log, passw, email = message.text.split()[1:]
    log = "pp.user.supplier@gmail.com"
    passw = "Ulcc1044"
    email = "denchicez@gmail.com"
    USERS[message.from_user.id] = Regulator(System(log, passw, email, message))
    print(USERS)
    await message.answer(f"Вы успешно зарегистрированы `{log}`", parse_mode="MarkDownV2")


@dp.message_handler(commands="add")
async def add_bot(message: types.Message):
    user_id = message.from_user.id
    if user_id in USERS:
        try:
            id, price, sendmessage, time = message.text.split()[1:]
        except:
            await message.answer("Что-то пошло не так...")
            return
        regulator = USERS[user_id]
        price = DEFAULT_PRICE if price == "-" else price
        time = DEFAULT_TIME if time == "-" else time
        regulator.newsession(sessionid=id, price=price, sendmessage=sendmessage, delay=time)

        await message.reply(fr"Бот успешно добавлен в сессию `id={id}`\!", parse_mode="MarkDownV2")
    else:
        await message.reply(r"Для начала зарегистрируйтесь\! Используйте команду `/login <login> <password> <email>`",
                            parse_mode="MarkDownV2")


@dp.message_handler(commands="del")
async def del_bot(message: types.Message):
    user_id = message.from_user.id
    if user_id in USERS:
        regulator = USERS[user_id]
        try:
            regulator.kill(message.text.split()[1])
        except:
            print("bad del...")
    else:
        await message.reply(r"Для начала зарегистрируйтесь\! Используйте команду `/login <login> <password> <email>`",
                            parse_mode="MarkDownV2")


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # buttons = ["/test1", "/test2"]
    # keyboard.add(*buttons)
    await message.answer(r"Добро пожаловать\! Используйте команду `/login <login> <password> <email>` для регистрации",
                         parse_mode="MarkDownV2")


# async def main():
#     await set_default_commands()
#
#     # Запуск поллинга
#     # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
#     await dp.start_polling()
#
#
# if __name__ == '__main__':
#     asyncio.run(main())


if __name__ == "__main__":
    # Запуск бота
    # set_default_commands()
    executor.start_polling(dp, skip_updates=True)
