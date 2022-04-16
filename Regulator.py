from multiprocessing import Process

from Player import Player


class Regulator:
    def __init__(self, system):
        self.system = system
        self.threads = {}

    def play(self, id: str, price: str, timedelta: str):  # асинхронная
        result = 0
        player = Player(id, price, timedelta, self.system)
        while (result == 0):
            result = player.play()
        del self.threads[id]
        self.system.sender.template(result, id)

    def newsession(self, id: str, price: str, timedelta: str):
        if (id not in self.threads):
            self.threads[id] = Process(target=self.play, args=(id, price, timedelta))
            self.threads[id].start()
            print(self.threads)
        else:
            if self.system.log:
                print("You're now upd this!")

    def getactivities(self):
        return self.threads.keys()

    def kill(self, id: str):
        if (id in self.threads):
            self.threads[id].kill()
        else:
            print("Can't find this id to kill someone")
