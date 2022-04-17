from asyncio import sleep
from datetime import datetime
from random import randint


class Player:
    def __init__(self, sessionid: str, minprice: float, timetosend: float, delay: float, system):
        self.sessionid = sessionid
        self.minprice = minprice
        self.timetosend = timetosend
        self.status = 0
        self.system = system
        self.delay = float(delay)
        self.notification = 0
        self.firstdelay = delay

    async def play(self):
        data = await self.system.getItem(self.sessionid)
        while data.get('message', '') == 'Необходимо пройти проверку':
            await sleep(self.delay)
            if self.system.log:
                print("We are waiting")
            data = await self.system.getItem(self.sessionid)
        version = data['rowVersion']
        bets = data['bets']
        if len(bets) == 0:
            winner = None
        else:
            winner = data['bets'][0]['supplier']['id']
        status = data['state']['name']
        cost = data['nextCost']
        time = datetime.strptime(data['endDate'], "%d.%m.%Y %H:%M:%S")
        time_now = datetime.now()
        timedelta = (time - time_now).seconds
        if not self.notification and timedelta <= float(self.timetosend):
            if self.system.log:
                print("Start send!")
            self.notification = 1
            await self.system.sender.notification(self.sessionid, timedelta)
        price = data['nextCost']
        if status != "Активная":
            if winner is None:
                return 1
            else:
                return 2
        if self.system.log:
            print("Wait delay")
        await sleep(self.delay)
        if self.system.log:
            print("End delay")
        if float(price) >= self.minprice:
            if winner is None:
                if self.system.log:
                    print("We need bit it!")
                await self.system.getBet(self.sessionid, version, cost)
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
