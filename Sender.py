from aiohttp import ClientSession

from config import BOT_TOKEN


class Sender:
    def __init__(self, receiver_email, telegram_message, sender_email: str = "thefroggylovers@gmail.com",
                 password: str = "a4+hPuC!X5j_tQKk*9geaQB"):
        self.sender_email = sender_email  # Enter your address
        self.telegram_message = telegram_message
        self.password = password
        self.receiver_email = receiver_email

    async def sendMessage(self, html):
        try:
            async with ClientSession() as session:
                async with session.post(url='https://api.telegram.org/bot{0}/sendMessage'.format(BOT_TOKEN),
                                        data={'chat_id': self.telegram_message.from_user.id,
                                              'text': html}) as resp:
                    print(await resp.text())
        except Exception as e:
            print("Something went wrong")
            print(e)

    async def send_telegram(self):
        await self.telegram_message.answer(f"Oops...", parse_mode="MarkDownV2")

    async def template(self, status: int, href: str):
        href = "https://edu.pp24.dev/auction/" + href
        html = ""
        if (status == 1):
            html = f"""You are win, Check you progress in {href}"""
        elif (status == 2):
            html = f"""We leave session, Check you progress in {href}"""
        else:
            print("Problem with sender")
        await self.sendMessage(html)

    async def notification(self, href: str, timedelta: str):
        href = "https://edu.pp24.dev/auction/" + href
        html = f"""Session soon will be close , It's near {timedelta} seconds to end <br>
                       Check you progress in {href}
                """
        await self.sendMessage(html)
