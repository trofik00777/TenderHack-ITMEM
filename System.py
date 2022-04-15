class System:
    def __init__(self, ):
        self.__catsessions = {'1': {}, '2': {}, '3': {}} # API

    def __upd(self):
        self.__catsessions['1']['price'] = 200 # API

    def getItem(self, id):
        self.__upd()
        return self.__catsessions.get(id, {})
