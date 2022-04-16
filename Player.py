from datetime import datetime
from time import sleep


class Player:
    def __init__(self, id: str, minprice: str, timetoend: str, system):
        self.id = id
        self.minprice = minprice
        self.timetoend = timetoend
        self.status = 0  # 0 - в ожидание, 1 - выйгран, 2 - проигран
        self.system = system

    def play(self):
        data = self.system.getItem(self.id)
        print(data)
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

        price = data['nextCost']
        if (status != "Активная"):
            if (winner == None):
                return 1
            else:
                return 2
        if (float(price) >= float(self.minprice)):
            if (timedelta <= float(self.timetoend)):
                if (winner == None):
                    print("Stavka sdelana")
                    sleep(5)
                    self.system.getBet(self.id, version, cost)
                else:
                    print("we uzhe postavili")
                    sleep(10)
                return 0
            else:
                print("sleep")
                sleep(5)
                return 0
        else:
            print("we don't need it...")
            sleep(5)
            return 2
