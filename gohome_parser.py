import requests
from bs4 import BeautifulSoup
from pars_model import Flat
import re
from datetime import datetime
import db_client

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
    for link in links:
        resp = requests.get(link)
        html = BeautifulSoup(resp.content, 'html.parser')
        title = html.find('h1').text.strip()

        raw_price = html.find('span', class_='price big')
        if raw_price is not None:
            price = re.sub('[^0-9]', '', raw_price.text.strip()) # что не цифра, становится пробелом
        else:
            price = 000
        description = html.find('p').text.strip()
        date = datetime.strptime(html.find_all(class_='description')[5].text.strip(), '%d.%m.%Y')
        number = re.sub('[^0-9]', '', html.find('a', class_='phone__link').text.strip())

        flats.append(Flat(
            link=link,
            title=title,
            price=price,
            description=description,
            date=date,
            number=number,
            reference=PARSER_NAME

        ))
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
