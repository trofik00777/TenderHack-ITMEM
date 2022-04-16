import requests


class System:
    def __init__(self, login, password):
        self.active = 1
        self.session = requests.Session()
        resp = self.session.get("https://old.edu.pp24.dev/api/Cssp/Authentication/BeginAuthentication?type=Password")
        token = resp.text
        token = token[1:-1]
        self.__login(password, login, token)

    def __login(self, password, login, token):
        url = "https://old.edu.pp24.dev/api/Cssp/Authentication/PerformAuthentication"
        data = {"token": token, "operation": "LogIn",
                "argument": {"values": {"login": f"{login}", "password": f"{password}"}}}
        resp = self.session.post(url, json=data)
        resp = resp.json()
        if (resp['isSessionComplete'] == True):
            print("We succesfully login")
            url = "https://old.edu.pp24.dev/api/Cssp/Authentication/CheckAuthentication"
            resp = self.session.get(url) # work with this!
            resp = resp.json()
            print(resp)
        else:
            print("Something wrong with login =(")

    def getItem(self, id):
        URL = f"https://edu.pp24.dev/newapi/api/Auction/Get?auctionId={id}"
        response = self.session.get(URL)
        response = response.json() # work with this!
        return response

    def getBet(self, id, rowversion, value):
        url = "https://edu.pp24.dev/newapi/api/Auction/CreateBet"
        data = {
            'auctionId': id,
            'rowVersion': rowversion,
            'value': value
        }
        resp = self.session.post(url, json=data) # work this!
