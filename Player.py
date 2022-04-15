class Player:
    def __init__(self, id, minprice, timetoend, system):
        self.id = id
        self.minprice = minprice
        self.timetoend = timetoend
        self.status = 0  # 0 - в ожидание, 1 - выйгран, 2 - проигран
        self.system = system

    def play(self):
        data = self.system.getItem(self.id)
        status = data['status']
        time = data['time']
        price = data['price']
        procent = data['procent']
        new_price = price - price * procent
        if (status == 1):
            return status
        if (status == 0):
            return status
        if (new_price > self.minprice):
            if (time < self.timetoend):
                self.bid()
            else:
                print("sleep")
                # sleep
        else:
            print("we don't need it...")
            return 0

    def bid(self):
        print("Поставил бабло")