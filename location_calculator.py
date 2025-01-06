import haversine as hs
from scrapper import Scrapper
from decimal import Decimal
from haversine import Unit
import itertools as itr
from car_data_model import CarDataModel, CarLocationDetailsDataModel
import googlemaps
import math
from google.maps import routing_v2


class UserInputModel:
    def __init__(self, max_allowed_wight: int, max_distance_pickup: int, max_distance_delivery: int, price_per_mile: Decimal) -> None:
        self.max_allowed_wight = max_allowed_wight
        self.max_distance_pickup = max_distance_pickup
        self.max_distance_delivery = max_distance_delivery
        self.price_per_mile = price_per_mile


class LocationCalculator:
    ApiKey = 'AIzaSyDDp3PRIJDWTG7m15LzGX1xDalj1wT2OTc'

    def __init__(self, data: dict[str, CarDataModel], settings: UserInputModel) -> None:
        self.data = data
        self.gmaps = googlemaps.Client(key=self.ApiKey)
        self.settings = settings
        routing_v2.RoutesClient()

    def create(self):
        res = list(itr.combinations(self.data, 3))
        data = []
        for ids in res:
            if self.__filter(ids):
                data.append(ids)
                m1 = self.data[ids[0]]
                # print(m1.location.destination)
                # print("car 1 from:" + m1.location.location)
                m2 = self.data[ids[1]]
                # print(m2.location.destination)
                # print("car 1 from:" + m2.location.location)
                m3 = self.data[ids[2]]
                # print(m3.location.destination)
                # print("car 1 from:" + m3.location.location)
        return data
        

    def __filter(self, ids: tuple[str, str, str]) -> bool:
        cargo_a = self.data[ids[0]]
        cargo_b = self.data[ids[1]]
        cargo_c = self.data[ids[2]]
        # filter max allowed wight
        if cargo_a.car.weight + cargo_b.car.weight + cargo_c.car.weight >= self.settings.max_allowed_wight:
            return False
        
        pick_up1 = self.__calculate_distance(
            cargo_a.location.location, cargo_b.location.location)
        pick_up2 = self.__calculate_distance(
            cargo_a.location.location, cargo_c.location.location)
        pick_up3 = self.__calculate_distance(
            cargo_b.location.location, cargo_c.location.location)

        # filter max pick up location range
        if (pick_up1 > self.settings.max_distance_pickup or
            pick_up2 > self.settings.max_distance_pickup or
            pick_up3 > self.settings.max_distance_pickup):
            return False
        if pick_up1 == 0 or pick_up2 == 0 or pick_up3 == 0:
            return False
        # print("from A -> B: " + str(cargo_a.location.location.address) + " from A -> C: " +
        #       str(cargo_b.location.location.address) + " from B -> C: " + str(cargo_c.location.location.address))

        delivery1 = self.__calculate_distance(
            cargo_a.location.destination, cargo_b.location.destination)
        delivery2 = self.__calculate_distance(
            cargo_a.location.destination, cargo_c.location.destination)
        delivery3 = self.__calculate_distance(
            cargo_b.location.destination, cargo_c.location.destination)
        
        if (delivery1 == 0 or delivery2 == 0 or delivery3 == 0):
            return False

        # filter max pick up location range
        if (delivery1 > self.settings.max_distance_delivery or
            delivery2 > self.settings.max_distance_delivery or
            delivery3 > self.settings.max_distance_delivery):
            return False

        return True

    def __calculate_distance_in_range(self, ids: tuple[str, str, str]):
        cargo_a = self.data[ids[0]]
        cargo_b = self.data[ids[1]]
        cargo_c = self.data[ids[2]]
        d1 = self.__calculate_distance(
            cargo_a.location.location, cargo_b.location.location)
        d2 = self.__calculate_distance(
            cargo_a.location.location, cargo_c.location.location)
        d3 = self.__calculate_distance(
            cargo_b.location.location, cargo_c.location.location)
        # print("from A -> B: " + str(d1) + " from A -> C: " +
        #       str(d2) + " from B -> C: " + str(d3))

    def __calculate_distance(self, first_car: CarLocationDetailsDataModel, second_car: CarLocationDetailsDataModel) -> int:
        res = hs.haversine((first_car.latitude, first_car.longitude), (
            second_car.latitude, second_car.longitude), unit=Unit.MILES)
        return math.ceil(res)


scrp = Scrapper()
sett = UserInputModel(13500, 50, 200, 0.1)
data = scrp.get_cars()
loc = LocationCalculator(data, sett)
# loc.calculate()
result = loc.create()
for car in result:
    print(data[car[0]].location.location.map_url)
    print(data[car[1]].location.location.map_url)
    print(data[car[2]].location.location.map_url)
    print("end of group" + str(car))
