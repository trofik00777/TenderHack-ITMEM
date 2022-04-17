from Regulator import Regulator
from System import System


def main():
    login = "pp.user.supplier@gmail.com"
    password = "Ulcc1044"
    mail = "denchicez@gmail.com"
    system = System(login, password, mail, "", log=True)
    if system.error != 0:
        print("end of program")
        return
    regulator = Regulator(system)
    while True:
        id = input("Input id of cat session\n")
        price = float(input("Input price of cat session\n"))
        sendmessage = float(input("Input time to send annatation about end of cat session\n"))
        delay = float(input("Input about time to get bit. It must in be [60 : endTime]\n"))

        regulator.newsession(id, price, sendmessage, delay)


if __name__ == '__main__':
    main()
