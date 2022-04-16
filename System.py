import requests

class System:
    @staticmethod
    def __checkNet():  # проверяем работает ли интернет
        try:
            requests.get("https://edu.pp24.dev/ru", timeout=10)
            return 1  # работает
        except requests.ConnectionError:
            return 0  # не работает

    def __init__(self, login: str, password: str):
        self.active = 1
        self.session = requests.Session()
        resp = self.session.get("https://old.edu.pp24.dev/api/Cssp/Authentication/BeginAuthentication?type=Password")
        token = resp.text
        token = token[1:-1]
        self.error = self.__login(password, login, token)

    # 0 - successful, -1 - error
    def __login(self, password: str, login: str, token: str):
        url = "https://old.edu.pp24.dev/api/Cssp/Authentication/PerformAuthentication"
        data = {"token": token, "operation": "LogIn",
                "argument": {"values": {"login": f"{login}", "password": f"{password}"}}}
        resp = self.session.post(url, json=data)  # work with this!
        resp = resp.json()
        if (resp['isSessionComplete'] == True):
            url = "https://old.edu.pp24.dev/api/Cssp/Authentication/CheckAuthentication"
            resp = self.session.get(url)  # work with this!
            resp = resp.json()
            print(resp)
            if (resp['isAuthenticated'] == False):
                print("failed to login")
                return -1
            print("We succesfully login")
            return 0
        else:
            print("Something wrong with login =(")
            return -1

    def getItem(self, id: str):
        URL = f"https://edu.pp24.dev/newapi/api/Auction/Get?auctionId={id}"
        response = self.session.get(URL)
        response = response.json()  # work with this!
        print(response)
        return response

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
            print("not available site")
