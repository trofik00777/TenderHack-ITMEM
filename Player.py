from _datetime import datetime


class Player:
    def __init__(self, id, minprice, timetoend, system):
        self.id = id
        self.minprice = minprice
        self.timetoend = timetoend
        self.status = 0  # 0 - в ожидание, 1 - выйгран, 2 - проигран
        self.system = system

    def play(self):
        data = self.system.getItem(self.id)
        print("-----")
        print(data)
        print('-----')
        version = data['rowVersion']
        try:
            winner = data['bets'][0]['supplier']['id']  # if null not we
        except:
            winner = None
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
        if (price > self.minprice):
            if (timedelta < self.timetoend):
                if(winner==None):
                    print("Stavka sdelana")
                    self.system.getBet(self.id, version, cost)
                    return 3
                else:
                    print("we uzhe postavili")
                    return 0
            else:
                print("sleep")
                return 0
        else:
            print("we don't need it...")
            return 2
