from Regulator import Regulator
from System import System


def main():
    system = System()
    regulator = Regulator([], system)
    while (True):
        id = input("Input id of cat session\n")
        price = int(input("Input price of cat session\n"))
        timedelta = int(input("Input time to end cat session\n"))
        regulator.newsession(id, price, timedelta)
        regulator.play()


if __name__ == '__main__':
    main()