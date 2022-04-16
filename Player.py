class Player:
    def __init__(self, id, minprice, timetoend, system, userid):
        self.id = id
        self.minprice = minprice
        self.timetoend = timetoend
        self.status = 0  # 0 - в ожидание, 1 - выйгран, 2 - проигран
        self.system = system
        self.userid = userid

    def play(self):
        data = self.system.getItem(self.id)
        winner = data['winner']
        status = data['status']
        time = data['time']
        price = data['price']
        procent = data['procent']
        if(status==1):
            if(winner == self.userid):
                return 1
            elif(winner!=None):
                return 2
        new_price = price - price * procent
        if (new_price > self.minprice):
            if (time < self.timetoend):
                self.bid()
            else:
                print("sleep")
                return 0
        else:
            print("we don't need it...")
            return 2

    def bid(self):
        print("Поставил бабло")
