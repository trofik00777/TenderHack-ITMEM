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
                ["add <id сессии> <минимальная цена> <время отправки сообщения> <X минут на обновление цены>", "(Добавить бота в сессию)"],
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

    # await call.message.answer(str(randint(1, 10)))
    bot_id = call.data.split("_")[1]
    await delete_bot(call.from_user.id, bot_id, call)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer(text=f"Бот успешно удален из сессии id={bot_id}", show_alert=True)
    # или просто await call.answer()


@dp.callback_query_handler(lambda x: x.data.endswith("settings"))
async def del_bot(call: types.CallbackQuery):

    # await call.message.answer(str(randint(1, 10)))
    bot_id = call.data.split("_")[1]
    # await delete_bot(call.from_user.id, bot_id, call)

    await call.message.edit_reply_markup(reply_markup=None)
    lines= [f"Используйте команды:"]
    lines.append(f"`/settings_update {bot_id} <new_price> <new_send_time> <new_delay_X>`")
    await call.message.answer(text="\n".join(lines), parse_mode="MArkDownV2")
    # или просто await call.answer()


@dp.message_handler(commands="settings_update")
async def get_active(message: types.Message):
    try:
        bot_id = message.text.split()[1]
        await delete_bot(message.from_user.id, bot_id, message)

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
            await regulator.newsession(sessionid=id, price=price, sendmessage=sendmessage, delay=time)

            await message.reply(fr"Бот успешно изменен\!", parse_mode="MarkDownV2")
        else:
            await message.reply(
                r"Для начала зарегистрируйтесь\! Используйте команду `/login <login> <password> <email>`",
                parse_mode="MarkDownV2")
    except Exception as e:
        print(e)


@dp.message_handler(commands="get_active")  # coming soon
async def get_active(message: types.Message):
    user_id = message.from_user.id
    if user_id in USERS:
        regulator = USERS[user_id]
        bots = await regulator.getactivities()
        # bots = [1, 2, 3]
        count_ = 3
        keyboard = types.InlineKeyboardMarkup(row_width=count_)
        for index, curr_bot_id in enumerate(bots):
            line = []
            line.append(types.InlineKeyboardButton(text=f"{curr_bot_id}", callback_data=f"{index}_{curr_bot_id}"))
            line.append(types.InlineKeyboardButton(text=f"settings", callback_data=f"{index}_{curr_bot_id}_settings"))
            line.append(types.InlineKeyboardButton(text=f"del", callback_data=f"{index}_{curr_bot_id}_del"))
            # line.append(types.InlineKeyboardButton(text=f"analyze", callback_data=f"{index}_{curr_bot_id}_analyze"))
            keyboard.add(*line)
        # a = []
        # for i in range(5):
        #     pass
        # keyboard.add(*a)
        await message.answer("List of bots:", reply_markup=keyboard)
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
        except:
            await message.answer("Что-то пошло не так...")
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
    except:
        print("bad input for delete")
    # user_id = message.from_user.id
    # if user_id in USERS:
    #     regulator = USERS[user_id]
    #     try:
    #         regulator.kill(message.text.split()[1])
    #     except:
    #         print("bad del...")
    # else:
    #     await message.reply(r"Для начала зарегистрируйтесь\! Используйте команду `/login <login> <password> <email>`",
    #                         parse_mode="MarkDownV2")


async def delete_bot(user_id, bot_id, message):
    if user_id in USERS:
        regulator = USERS[user_id]
        try:
            await regulator.kill(bot_id)
        except:
            print("bad del...")
    else:
        await message.answer(r"Для начала зарегистрируйтесь\! Используйте команду `/login <login> <password> <email>`",
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
