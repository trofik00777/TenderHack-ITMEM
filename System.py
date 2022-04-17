from aiohttp import ClientSession

from Sender import Sender


class System:
    @staticmethod
    async def __checkNet():  # проверяем работает ли интернет
        async with ClientSession() as session:
            try:
                async with session.get("https://edu.pp24.dev/ru") as resp:
                    return 1
            except:
                return 0

    async def create(self):
        async with ClientSession() as session:
            self.cookies = session.cookie_jar
        if self.log:
            print("Start login in account")
        url = "https://old.edu.pp24.dev/api/Cssp/Authentication/BeginAuthentication?type=Password"
        while True:
            if await self.__checkNet():
                async with ClientSession(cookie_jar=self.cookies) as session:
                    async with session.get(url) as resp:
                        if self.log:
                            print(await resp.text())
                        self.cookies = session.cookie_jar
                        token = await resp.text()
                        token = token[1:-1]
                        self.error = await self.__login(self.password, self.login, token)
                        if self.error == 0:
                            print("Succesfully login")
                        else:
                            print("Unseccusfully login")
            if self.log:
                print("Problem with internet")

    def __init__(self, login: str, password: str, receive_mail, telegram_message, log: bool = False):
        self.active = 1
        self.log = log
        self.password = password
        self.login = login
        self.telegram_message = telegram_message
        self.sender = Sender(receive_mail, telegram_message)

    # 0 - successful, -1 - error
    async def __login(self, password: str, login: str, token: str):
        url = "https://old.edu.pp24.dev/api/Cssp/Authentication/PerformAuthentication"
        data = {"token": token, "operation": "LogIn",
                "argument": {"values": {"login": f"{login}", "password": f"{password}"}}}
        while True:
            if await self.__checkNet():
                async with ClientSession(cookie_jar=self.cookies) as session:
                    async with session.post(url, json=data) as response:
                        resp = await response.json()
                        self.cookies = session.cookie_jar
                break
            if self.log:
                print("Problem with internet")
        if (resp['isSessionComplete'] == True):
            url = "https://old.edu.pp24.dev/api/Cssp/Authentication/CheckAuthentication"
            while True:
                if await self.__checkNet():
                    async with ClientSession(cookie_jar=self.cookies) as session:
                        async with session.get(url) as response:
                            if self.log:
                                print(await response.text())
                            resp = await response.json()
                            if (resp['isAuthenticated'] == False):
                                if self.log:
                                    print("Failed login")
                                return -1
                            if self.log:
                                print("We succesfully login")
                            self.cookies = session.cookie_jar
                            return 0
                if self.log:
                    print("Problem with internet")
        else:
            if self.log:
                print("Something went wrong")
            return -1

    async def getItem(self, id: str):
        URL = f"https://edu.pp24.dev/newapi/api/Auction/Get?auctionId={id}"
        while True:
            if await self.__checkNet():
                async with ClientSession(cookie_jar=self.cookies) as session:
                    async with session.get(URL) as response:
                        if self.log:
                            print(await response.text())
                        resp = await response.json()
                        self.cookies = session.cookie_jar
                        return resp
            if self.log:
                print("Problem with internet")

    async def getBet(self, id: str, rowversion: str, value: str):
        url = "https://edu.pp24.dev/newapi/api/Auction/CreateBet"
        data = {
            'auctionId': id,
            'rowVersion': rowversion,
            'value': value
        }
        while True:
            if self.__checkNet():
                async with ClientSession(cookie_jar=self.cookies) as session:
                    async with session.post(url, json=data) as response:
                        if self.log:
                            print(await response.text())
                            self.cookies = session.cookie_jar
                        break
            if self.log:
                print("Problem with internet")
