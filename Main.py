from System import System
from Player import Player

def main():
    login = "pp.user.supplier@gmail.com"
    password = "Ulcc1044"
    system = System(login, password)
    player = Player(8914838, 1, 1000000000000000000000000, system)
    result = player.play()
    print(result)
    # regulator = Regulator(system, 1)
    # while (True):
    #     id = input("Input id of cat session\n")
    #     price = int(input("Input price of cat session\n"))
    #     timedelta = int(input("Input time to end cat session\n"))
    #     regulator.newsession(id, price, timedelta)


if __name__ == '__main__':
    main()
