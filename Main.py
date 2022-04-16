from Regulator import Regulator
from System import System


def main():
    login = "pp.user.supplier@gmail.com"
    password = "Ulcc1044"
    mail = "denchicez@gmail.com"
    system = System(login, password, mail, log=True)
    if system.error != 0:
        print("end of program")
        return
    regulator = Regulator(system)
    while (True):
        id = input("Input id of cat session\n")
        price = input("Input price of cat session\n")
        timedelta = input("Input time to end cat session\n")
        regulator.newsession(id, price, timedelta)


if __name__ == '__main__':
    main()
