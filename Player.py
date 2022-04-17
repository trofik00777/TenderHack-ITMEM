from datetime import datetime
from random import randint
from time import sleep


class Player:
    def __init__(self, sessionid: str, minprice: float, timetosend: float, delay: float, system):
        self.sessionid = sessionid
        self.minprice = minprice
        self.timetosend = timetosend
        self.status = 0  # 0 - в ожидание, 1 - выйгран, 2 - проигран
        self.system = system
        self.delay = delay
        self.notification = 0
        self.firstdelay = delay

    def play(self):
        data = self.system.getItem(self.sessionid)
        while data.get('message', '') == 'Необходимо пройти проверку':
            sleep(self.delay)
            if self.system.log:
                print("We are waiting")
            data = self.system.getItem(self.sessionid)
        version = data['rowVersion']
        bets = data['bets']
        if (len(bets) == 0):
            winner = None
        else:
            winner = data['bets'][0]['supplier']['id']
        status = data['state']['name']
        cost = data['nextCost']
        time = datetime.strptime(data['endDate'], "%d.%m.%Y %H:%M:%S")
        time_now = datetime.now()
        timedelta = (time - time_now).seconds
        if (not self.notification and timedelta <= self.timetosend):
            self.notification = 1
            self.system.sender.notification(self.sessionid, timedelta)
        price = data['nextCost']
        if (status != "Активная"):
            if (winner is None):
                return 1
            else:
                return 2
        sleep(self.delay)
        if (float(price) >= self.minprice):
            if (winner is None):
                if self.system.log:
                    print("We need bit it!")
                self.system.getBet(self.sessionid, version, cost)
                self.delay = self.firstdelay + randint(int(-timedelta * 0.01), int(timedelta * 0.01))
                self.delay = max(self.delay, 60)
                self.delay = min(self.delay, timedelta - 60)
            else:
                if self.system.log:
                    print("We last player")
            return 0
        else:
            if self.system.log:
                print("This not for us")
            return 2
