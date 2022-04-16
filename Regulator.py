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
            print(self.threads)
        print(self.threads)
        self.system.sender.template(result, id)
        # print(f"Result of session id {id} is {result}")

    def newsession(self, id: str, price: str, timedelta: str):
        if (id not in self.threads):
            thread = Process(target=self.play, args=(id, price, timedelta))
            thread.start()
            self.threads[id] = thread
            print(self.threads)
        else:
            if self.system.log:
                print("You're now upd this!")

    def getactivities(self):
        return self.threads.keys()
