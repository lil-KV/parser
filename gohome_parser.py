import requests
from bs4 import BeautifulSoup
from pars_model import Flat
import re
from datetime import datetime
import db_client
import psycopg2


PARSER_NAME = 'gohome.by'  # reference

def get_all_flats_links(page_from=0, page_to=1):
    links = []
    while page_from < page_to:
        resp = requests.get(f'https://gohome.by/sale?{page_from}')
        html = BeautifulSoup(resp.content, 'html.parser')
        for a in html.find_all('a', href=True, class_='name__link'):
            links.append('https://gohome.by'+a['href'])  # /ads/view/586754
        page_from += 1
    return links


def turn_links_to_flats(links):
    flats = []
    for counter, link in enumerate(links):
        resp = requests.get(link)
        html = BeautifulSoup(resp.content, 'html.parser')
        title = html.find('h1').text.strip()
        try:
            price = re.sub('[^0-9]', '', html.find(class_='price big').text.strip())
        except Exception:
            price = 'договорная'
        description = html.find('p').text.strip()
        date = datetime.strptime(html.find_all(class_='description')[5].text.strip(), '%d.%m.%Y')
        number = html.find('a', class_='phone__link').text.strip()
        square = html.find_all(class_='feature')[1].text.strip()
        city = html.find_all('a', href=True)[95].text.strip()
        street_house = html.find_all(class_='description')[10].text.strip()
        district = html.find_all(class_='description')[9].text.strip()
        try:
            year = html.find_all(class_='feature')[5].text.strip()
        except IndexError:
            year = 'не указано'
        rooms = html.find_all(class_='feature')[0].text.strip()

        try:
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
                rooms=rooms
                        ))
        except psycopg2.errors.StringDataRightTruncation:
            pass

        print(f'спаршено {counter} из {len(links)}')
    return flats


# функция для загрузки данных квартиры в БД
def save_flats(flats):
    for flat in flats:
        db_client.insert_flat(flat)


def get_last_flats(page_from=0, page_to=1):
    links = get_all_flats_links(page_from, page_to)
    flats = turn_links_to_flats(links)
    save_flats(flats)


get_last_flats()
