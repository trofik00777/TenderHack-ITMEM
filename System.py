import requests

from Sender import Sender


class System:
    @staticmethod
    def __checkNet():  # проверяем работает ли интернет
        try:
            requests.get("https://edu.pp24.dev/ru", timeout=10)
            return 1  # работает
        except requests.ConnectionError:
            return 0  # не работает

    def __init__(self, login: str, password: str, receive_mail, telegram_message, log: bool = False):
        self.active = 1
        self.log = log
        self.telegram_message = telegram_message
        self.session = requests.Session()
        self.sender = Sender(receive_mail, telegram_message)
        if self.log:
            print("Start login in account")
        while True:
            if self.__checkNet():
                resp = self.session.get(
                    "https://old.edu.pp24.dev/api/Cssp/Authentication/BeginAuthentication?type=Password")
                if self.log:
                    print(resp)
                break
            if self.log:
                print("Problem with internet")
        token = resp.text
        token = token[1:-1]
        self.error = self.__login(password, login, token)
        if self.error == 0:
            print("Succesfully login")
        else:
            print("Unseccusfully login")

    # 0 - successful, -1 - error
    def __login(self, password: str, login: str, token: str):
        url = "https://old.edu.pp24.dev/api/Cssp/Authentication/PerformAuthentication"
        data = {"token": token, "operation": "LogIn",
                "argument": {"values": {"login": f"{login}", "password": f"{password}"}}}
        while True:
            if self.__checkNet():
                resp = self.session.post(url, json=data)  # work with this!
                break
            if self.log:
                print("Problem with internet")
        resp = resp.json()
        if (resp['isSessionComplete'] == True):
            url = "https://old.edu.pp24.dev/api/Cssp/Authentication/CheckAuthentication"
            while True:
                if self.__checkNet():
                    resp = self.session.get(url)
                    break
                if self.log:
                    print("Problem with internet")
            resp = resp.json()
            if (resp['isAuthenticated'] == False):
                if self.log:
                    print("Failed login")
                return -1
            if self.log:
                print("We succesfully login")
            return 0
        else:
            if self.log:
                print("Something went wrong")
            return -1

    def getItem(self, id: str):
        URL = f"https://edu.pp24.dev/newapi/api/Auction/Get?auctionId={id}"
        while True:
            if self.__checkNet():
                resp = self.session.get(URL)
                break
            if self.log:
                print("Problem with internet")
        resp = resp.json()  # work with this!
        return resp

    def getBet(self, id: str, rowversion: str, value: str):
        url = "https://edu.pp24.dev/newapi/api/Auction/CreateBet"
        data = {
            'auctionId': id,
            'rowVersion': rowversion,
            'value': value
        }
        while True:
            if self.__checkNet():
                resp = self.session.post(url, json=data)  # work this!
                break
            if self.log:
                print("Problem with internet")
