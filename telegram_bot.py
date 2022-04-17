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
                ["add <id сессии> <минимальная цена> <время отправки сообщения> <X минут на обновление цены>",
                 "(Добавить бота в сессию)"],
                ["del <id сессии>", "(Удалить бота из сессии)"],
                # ["menu_bots", "(Управление ботами)"],
                ["get_active", "(Список текущих сессий)"]]

    text = []
    for comm, desc in commands:
        decript = desc.replace('(', r'\(').replace(')', r'\)')
        text.append(fr"`/{comm}` \-\- _{decript}_")
    await message.answer('\n'.join(text), parse_mode="MarkDownV2")


@dp.callback_query_handler(lambda x: x.data.endswith("del"))
async def del_bot(call: types.CallbackQuery):
    bot_id = call.data.split("_")[1]
    await delete_bot(call.from_user.id, bot_id, call)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer(text=f"Бот успешно удален из сессии id={bot_id}", show_alert=True)


@dp.callback_query_handler(lambda x: x.data.endswith("settings"))
async def del_bot(call: types.CallbackQuery):
    bot_id = call.data.split("_")[1]
    await call.message.edit_reply_markup(reply_markup=None)
    lines = ["Используйте команды:", f"`/settings_update {bot_id} <new_price> <new_send_time> <new_delay_X>`"]
    await call.message.answer(text="\n".join(lines), parse_mode="MArkDownV2")


@dp.message_handler(commands="settings_update")
async def get_active(message: types.Message):
    try:
        bot_id = message.text.split()[1]
        await delete_bot(message.from_user.id, bot_id, message)

        user_id = message.from_user.id
        if user_id in USERS:
            try:
                id, price, sendmessage, time = message.text.split()[1:]
            except Exception as e:
                await message.answer("Что-то пошло не так...")
                print(e)
                return
            regulator = USERS[user_id]
            price = DEFAULT_PRICE if price == "-" else price
            time = DEFAULT_TIME if time == "-" else time
            await regulator.newsession(sessionid=id, price=price, sendmessage=sendmessage, delay=time)

            await message.reply(fr"Бот успешно изменен\!", parse_mode="MarkDownV2")
        else:
            await message.reply(
                r"Для начала зарегистрируйтесь\! Используйте команду `/login <login> <password> <email>`",
                parse_mode="MarkDownV2")
    except Exception as e:
        print(e)


@dp.message_handler(commands="get_active")
async def get_active(message: types.Message):
    user_id = message.from_user.id
    if user_id in USERS:
        regulator = USERS[user_id]
        bots = await regulator.getactivities()
        # bots = [1, 2, 3]
        count_ = 3
        keyboard = types.InlineKeyboardMarkup(row_width=count_)
        for index, curr_bot_id in enumerate(bots):
            line = [types.InlineKeyboardButton(text=f"{curr_bot_id}", callback_data=f"{index}_{curr_bot_id}_link"),
                    types.InlineKeyboardButton(text=f"settings", callback_data=f"{index}_{curr_bot_id}_settings"),
                    types.InlineKeyboardButton(text=f"del", callback_data=f"{index}_{curr_bot_id}_del")]
            keyboard.add(*line)
        await message.answer("List of bots:", reply_markup=keyboard)
    else:
        await message.reply(r"Для начала зарегистрируйтесь\! Используйте команду `/login <login> <password> <email>`",
                            parse_mode="MarkDownV2")


@dp.callback_query_handler(lambda x: x.data.endswith("link"))
async def del_bot(call: types.CallbackQuery):
    bot_id = call.data.split("_")[1]
    await call.answer(text=f"Ссылка на сессию: https://edu.pp24.dev/auction/{bot_id}", show_alert=True)


@dp.message_handler(commands="login")
async def login(message: types.Message):
    # log, passw, email = message.text.split()[1:]
    log = "pp.user.supplier@gmail.com"
    passw = "Ulcc1044"
    email = "denchicez@gmail.com"
    system = System(log, passw, email, message)
    await system.create()
    USERS[message.from_user.id] = Regulator(system)
    print(USERS)
    await message.answer(f"Вы успешно зарегистрированы `{log}`", parse_mode="MarkDownV2")


@dp.message_handler(commands="add")
async def add_bot(message: types.Message):
    user_id = message.from_user.id
    if user_id in USERS:
        try:
            id, price, sendmessage, time = message.text.split()[1:]
        except Exception as e:
            await message.answer("Что-то пошло не так...")
            print(e)
            return
        regulator = USERS[user_id]
        price = DEFAULT_PRICE if price == "-" else price
        time = DEFAULT_TIME if time == "-" else time
        await regulator.newsession(sessionid=id, price=price, sendmessage=sendmessage, delay=time)

        await message.reply(fr"Бот успешно добавлен в сессию `id={id}`\!", parse_mode="MarkDownV2")
    else:
        await message.reply(r"Для начала зарегистрируйтесь\! Используйте команду `/login <login> <password> <email>`",
                            parse_mode="MarkDownV2")


@dp.message_handler(commands="del")
async def del_bot(message: types.Message):
    try:
        await delete_bot(message.from_user.id, message.text.split()[1], message)
    except Exception as e:
        print("bad input for delete")
        print(e)


async def delete_bot(user_id, bot_id, message):
    if user_id in USERS:
        regulator = USERS[user_id]
        try:
            await regulator.kill(bot_id)
        except Exception as e:
            print("bad del...")
            print(e)
    else:
        await message.answer(r"Для начала зарегистрируйтесь\! Используйте команду `/login <login> <password> <email>`",
                             parse_mode="MarkDownV2")


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer(r"Добро пожаловать\! Используйте команду `/login <login> <password> <email>` для регистрации",
                         parse_mode="MarkDownV2")


if __name__ == "__main__":
    # set_default_commands()
    executor.start_polling(dp, skip_updates=True)
