from decimal import Decimal
from typing import Tuple


class CarLocationDetailsDataModel:
    def __init__(self, address: str, map_url: str, geo_loc: str) -> None:
        self.address = address
        self.map_url = map_url
        location = self.__parse_geo_location(geo_loc)
        self.latitude = location[0]
        self.longitude = location[1]

    def __parse_geo_location(self, loc: str) -> Tuple[Decimal, Decimal]:
        res = loc.split(',')
        return (Decimal(res[0]), Decimal(res[1]))
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class CarLocationDataModel:
    def __init__(self, location: CarLocationDetailsDataModel, destination: CarLocationDetailsDataModel) -> None:
        self.location = location
        self.destination = destination

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class CarDetailsDataModel:
    def __init__(self) -> None:
        self.car_model: str = None
        self.weight: int = 0
        self.size: str = None


class CarDataModel:
    def __init__(self, id: str, company: str, price: Decimal, location: CarLocationDataModel, car: CarDetailsDataModel) -> None:
        self.id = id
        self.company = company
        self.location = location
        self.price = price
        self.car = car
