from multiprocessing import Process

from Player import Player


class Regulator:
    def __init__(self, system):
        self.system = system
        self.threads = {}

    def play(self, sessionid: str, price: float, timedelta: float, delay: float):  # асинхронная
        result = 0
        player = Player(sessionid, price, timedelta, delay, self.system)
        while (result == 0):
            result = player.play()
        del self.threads[sessionid]
        self.system.sender.template(result, sessionid)

    def newsession(self, sessionid: str, price: float, sendmessage: float, delay: float):
        if (sessionid not in self.threads):
            self.threads[sessionid] = Process(target=self.play, args=(sessionid, price, sendmessage, delay))
            self.threads[sessionid].start()
        else:
            if self.system.log:
                print("You're now upd this!")

    def getactivities(self):
        return self.threads.keys()

    def kill(self, sessionid: str):
        if (sessionid in self.threads):
            self.threads[sessionid].kill()
        else:
            print("Can't find this id to kill someone")
