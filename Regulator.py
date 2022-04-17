import asyncio

from Player import Player


class Regulator:
    def __init__(self, system):
        self.system = system
        self.threads = {}

    async def play(self, sessionid: str, price: float, timedelta: float, delay: float):  # асинхронная
        result = 0
        player = Player(sessionid, price, timedelta, delay, self.system)
        while (result == 0):
            result = await player.play()
        print(f"RESULT IS {result}")
        del self.threads[sessionid]
        self.system.sender.template(result, sessionid)

    async def newsession(self, sessionid: str, price: float, sendmessage: float, delay: float):
        if (sessionid not in self.threads):
            self.threads[sessionid] = asyncio.create_task(self.play(sessionid, price, sendmessage, delay))
        else:
            if self.system.log:
                print("You're now upd this!")

    async def getactivities(self):
        return self.threads.keys()

    async def kill(self, sessionid: str):
        if (sessionid in self.threads):
            self.threads[sessionid].cancel()
            del self.threads[sessionid]
        else:
            print("Can't find this id to kill someone")
