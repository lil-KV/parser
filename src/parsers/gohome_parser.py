import requests
from bs4 import BeautifulSoup
from src.parsers.pars_model import Flat, ParserFather
from datetime import datetime
import time
from tqdm import tqdm

PARSER_NAME = 'gohome.by'  # reference


class ParserGohomeBy(ParserFather):

    def parser_name(self):
        return PARSER_NAME

    def get_all_flats_links(self, page_from=1, page_to=2):
        links = []
        while page_from < page_to:
            resp = requests.get(f'https://gohome.by/sale?{page_from}')
            html = BeautifulSoup(resp.content, 'html.parser')
            for a in html.find_all('a', href=True, class_='name__link'):
                links.append('https://gohome.by' + a['href'])  # /ads/view/586754
            page_from += 1
        return links

    def turn_links_to_flats(self, links):
        flats = []
        for counter, link in enumerate(links):
            resp = requests.get(link)
            html = BeautifulSoup(resp.content, 'html.parser')
            try:
                title = html.find('h1').text.strip()
                price = html.find(class_='price big').text.strip()
                if price == '':
                    price = 'договорная'
                description = html.find('p').text.strip()
                date = datetime.strptime(html.find_all(class_='description')[5].text.strip(), '%d.%m.%Y')
                number = html.find('a', class_='phone__link').text.strip()
                square = html.find_all(class_='feature')[1].text.strip()
                city = html.find_all('div', {'class': 'description'})[8].text.strip()
                street_house = html.find_all(class_='description')[10].text.strip()
                district = html.find_all(class_='description')[9].text.strip()
                try:
                    year = html.find_all(class_='feature')[5].text.strip()
                except IndexError:
                    year = 'не указано'
                rooms = html.find_all(class_='feature')[0].text.strip()
                photos = list()
                first_photos = html.find_all('div', {'class': "responsive-image"})[:4]
                try:
                    for photo in first_photos:
                        img = photo.img['data-webp']
                        photos.append('https://gohome.by' + img)
                except TypeError:
                    pass
            except AttributeError:
                pass

            flats.append(Flat(
                reference=PARSER_NAME,
                link=link,
                title=title,
                price=price,
                description=description,
                date=date,
                number=number,
                square=square,
                city=city,
                street_house=street_house,
                district=district,
                year=year,
                rooms=rooms,
                photos=photos
            ))
            for item in tqdm(flats):
                time.sleep(0.01)
        return flats


ParserGohomeBy().update_with_last_flats()
