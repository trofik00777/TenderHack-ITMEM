from multiprocessing import Process

from Player import Player


class Regulator:
    def __init__(self, system):
        self.system = system
        self.threads = []

    def play(self, id, price, timedelta):  # асинхронная
        result = 0
        player = Player(id, price, timedelta, self.system)
        while (result == 0):
            result = player.play()
        print(f"Result of session id {id} is {result}")


    def newsession(self, id, price, timedelta):
        thread = Process(target=self.play, args=(id, price, timedelta))
        thread.start()
        thread.join()
        self.threads.append(thread)