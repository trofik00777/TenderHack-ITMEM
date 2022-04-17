from datetime import datetime
from random import randint
from time import sleep


class Player:
    def __init__(self, id: str, minprice: str, timetosend: str, delay, system):
        self.id = id
        self.minprice = minprice
        self.timetosend = timetosend
        self.status = 0  # 0 - в ожидание, 1 - выйгран, 2 - проигран
        self.system = system
        self.delay = delay
        self.notification = 0
        self.firstdelay = delay

    def play(self):
        data = self.system.getItem(self.id)
        while data.get('message', '') == 'Необходимо пройти проверку':
            sleep(10)
            if self.system.log:
                print("We are waiting")
            data = self.system.getItem(self.id)
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
        if (not self.notification and timedelta <= float(self.timetosend)):
            self.notification = 1
            self.system.sender.notification(id, timedelta)
        price = data['nextCost']
        if (status != "Активная"):
            if (winner == None):
                return 1
            else:
                return 2
        if (float(price) >= float(self.minprice)):
            if (timedelta <= float(self.delay)):
                if (winner == None):
                    if self.system.log:
                        print("We need bit it!")
                    sleep(5)
                    self.system.getBet(self.id, version, cost)
                    self.delay = self.firstdelay + randint(-timedelta * 0.01, timedelta * 0.01)
                    self.delay = max(self.delay, 60)
                    self.delay = min(self.delay, timedelta - 60)

                else:
                    if self.system.log:
                        print("We last player")
                    sleep(10)
                return 0
            else:
                print("sleep")
                sleep(5)
                return 0
        else:
            if self.system.log:
                print("This not for us")
            sleep(5)
            return 2
