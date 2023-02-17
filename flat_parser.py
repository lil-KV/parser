import requests
from bs4 import BeautifulSoup

def get_all_flats_links(page_from=0, page_to=1):
    flats_links = []
    while page_from < page_to:
        resp = requests.get(f'https://edc.sale/ru/by/real-estate/sale/?{page_from}')
        html = BeautifulSoup(resp.content, 'html.parser')
        for a in html.find_all('a', href=True, class_='it-item-title'):
            flats_links.append(a['href'])
        page_from += 1
    return flats_links

get_all_flats_links()
