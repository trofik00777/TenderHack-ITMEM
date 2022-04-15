from Player import Player


class Regulator:
    def __init__(self, ids, system):
        self.system = system
        self.players = []
        for id in ids:
            self.players.append(Player(id, 100, 5, system))

    def play(self): # асинхронная
        while (len(self.players)):
            for player in self.players:
                player.play()

    def newsession(self, id, price, timedelta):
        self.players.append(Player(id, price, timedelta, self.system))
