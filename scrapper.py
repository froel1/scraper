from bs4 import BeautifulSoup
import re
from decimal import Decimal
from urllib.parse import urlparse
from urllib.parse import parse_qs
from car_data_model import CarDetailsDataModel, CarLocationDataModel, CarLocationDetailsDataModel, CarDataModel


class Scrapper:
    def __parse_locations(self, car) -> CarLocationDataModel:
        origin = car.find('a', attrs={'data-orgn-cv': True})
        destination = car.find('a', attrs={'data-dest-cv': True})

        loc_from = CarLocationDetailsDataModel(self.__format_special(
            origin.text), origin['href'], self.__get_geo_location(origin['href']))

        loc_to = CarLocationDetailsDataModel(self.__format_special(
            destination.text), destination['href'], self.__get_geo_location(destination['href']))

        return CarLocationDataModel(loc_from, loc_to)

    def __get_geo_location(self, url):
        parsed_url = urlparse(url)
        return parse_qs(parsed_url.query)['q'][0]

    def __parse_price(self, car) -> Decimal:
        car_price = car.find('div', attrs={'data-pc': True}).text
        price = re.findall('[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+', car_price)
        return price[0]

    def __parse_car_type(self, car) -> CarDetailsDataModel:
        car_type = car.find(
            'div', attrs={'data-vh': True}).parent.find_all('div')

        vehicle = CarDetailsDataModel()

        if 1 < len(car_type):
            vehicle.vehicle = self.__format_special(car_type[1].text)
        if 2 < len(car_type):
            vehicle.weight = int(re.findall('[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+', car_type[2].text)[0])
        if 3 < len(car_type):
            vehicle.size = self.__format_special(car_type[3].text)

        return vehicle

    def __format_special(self, data):
        return ' '.join(data.split())

    def __get_data(self):
        html = open('/Users/dundutso/Repos/Test Projects/ttt.html', 'r').read()
        data = BeautifulSoup(html, 'html.parser')
        return data

    def get_cars(self) -> dict[str, CarDataModel]:
        data = self.__get_data()
        result = {}
        for car in data.find_all('div', attrs={'data-listing-id': True}):
            price = self.__parse_price(car)
            locations = self.__parse_locations(car)
            company = self.__format_special(
                car.find('a', attrs={'data-cn-cv': True}).text)
            vehicle = self.__parse_car_type(car)
            id = car['data-listing-id']

            # result[id] = {
            #     'price': price,
            #     'location': locations,
            #     'company': company,
            #     'vehicle': vehicle
            # }
            result[id] = CarDataModel(id, company, price, locations, vehicle)
        return result
