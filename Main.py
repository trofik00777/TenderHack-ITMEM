from System import System
from Regulator import Regulator

def main():
    login = "pp.user.supplier@gmail.com"
    password = "Ulcc1044"
    system = System(login, password)
    regulator = Regulator(system)
    while (True):
        id = input("Input id of cat session\n")
        price = input("Input price of cat session\n")
        timedelta = input("Input time to end cat session\n")
        regulator.newsession(id, price, timedelta)


if __name__ == '__main__':
    main()
