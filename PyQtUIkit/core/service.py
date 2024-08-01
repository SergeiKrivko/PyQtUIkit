class KitService:
    __services = {}

    def __init__(self):
        if self.__class__ in KitService.__services:
            raise Exception("KitService is already initialized")
        KitService.__services[self.__class__] = self

    @staticmethod
    def inject(self):
        return KitService.__services[self]
