class System:
    def __init__(self):
        self.__catsessions = {
            '0': {
                'status': 0,
                'time': 360,
                'price': 1000,
                'last_price': 1000,
                'procent': 0.001,
                'who_last_send': None,
                'winner': None
            },
            '1': {
                'status': 0,
                'time': 1000,
                'price': 2475,
                'last_price': 2475,
                'procent': 0.0005,
                'who_last_send': None,
                'winner': None
            },
            '2': {
                'status': 0,
                'time': 834,
                'price': 774,
                'last_price': 774,
                'procent': 0.0005,
                'who_last_send': None,
                'winner': None
            },
            '3': {
                'status': 0,
                'time': 243,
                'price': 1378,
                'last_price': 1378,
                'procent': 0.001,
                'who_last_send': None,
                'winner': None
            },
            '4': {
                'status': 0,
                'time': 133,
                'price': 937,
                'last_price': 937,
                'procent': 0.001,
                'who_last_send': None,
                'winner': None
            },
            '5': {
                'status': 0,
                'time': 3600,
                'price': 5001,
                'last_price': 5001,
                'procent': 0.001,
                'who_last_send': None,
                'winner': None
            },
        }

    def __upd(self):
        self.__catsessions['1']['price'] = 200  # API

    def getItem(self, id):
        self.__upd()
        return self.__catsessions.get(id, {})
