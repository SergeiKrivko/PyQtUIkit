from typing import Type


class KitService:
    __services = {}

    def __init__(self):
        if self.__class__ in KitService.__services:
            raise Exception("KitService is already initialized")
        KitService.__services[self.__class__] = self

    @staticmethod
    def inject(service_type: Type['KitService']):
        if service_type not in KitService.__services:
            KitService.__services[service_type] = service_type()
        return KitService.__services[service_type]
