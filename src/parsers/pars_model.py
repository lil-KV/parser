from abc import ABC, abstractmethod
from src import db_client


class Flat:
    def __init__(self, link=None, reference=None, title=None, price=None, description=None, date=None, number=None,
                 square=None, city=None, street_house=None, district=None, year=None, rooms=None, photos=[]):
        self.link = link
        self.reference = reference
        self.title = title
        self.price = price
        self.description = description
        self.date = date
        self.number = number
        self.square = square
        self.city = city
        self.street_house = street_house
        self.district = district
        self.year = year
        self.rooms = rooms
        self.photos = photos


class ParserFather(ABC):

    @abstractmethod
    def parser_name(self):
        return 'unnamed parser'

    @abstractmethod
    def get_all_flats_links(self, page_from=1, page_to=2):
        return []

    @abstractmethod
    def turn_links_to_flats(self, links: list):
        return []

    @staticmethod
    # функция для загрузки данных квартиры в БД
    def save_flats(flats):
        for counter, flat in enumerate(flats):
            db_client.insert_flat(flat)

    def update_with_last_flats(self, page_from=1, page_to=2):
        links = self.get_all_flats_links(page_from, page_to)
        flats = self.turn_links_to_flats(links)
        self.save_flats(flats)


