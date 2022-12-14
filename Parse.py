import requests
from bs4 import BeautifulSoup
from cat_db import insert_db

URLS = ('moizver.com/catalog/item/6069/',
        'moizver.com/catalog/item/103094/',
        'moizver.com/catalog/item/86217/',
        'mirhvost.ru/catalog/koshki/korma_dlya_koshek/vlazhnye_korma_dlya_koshek'
        '/pauch_royal_canin_dlya_britanskoy_korotkosherstnoy_kusochki_v_souse.html',

        )
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/102.0.0.0 ''Safari/537.36',
           'accept': '*/*'}


def get_html(url, params=None):
    req = requests.get(url, headers=HEADERS, params=params)
    return req


def get_content_moizver(html):
    soup = BeautifulSoup(html, 'html.parser')
    content_page = soup.find_all("div", attrs={'class': "wraps hover_shine"})
    for item in content_page:
        item_name = item.find("div", attrs={"class": "page-top-main"}).find(
            'h1', attrs={"id": "pagetitle"}).get_text(strip=True)
        item_price = item.find("div", attrs={"class": "cost prices clearfix"}).find('span', style="display:none;").text
        insert_db(item_name=item_name, shop_name="Мой Зверь", item_price=item_price)


def get_content_mirhvost(html):
    soup = BeautifulSoup(html, 'html.parser')
    content_page = soup.find_all("div", attrs={'id': "catalogElement"})
    for item in content_page:
        item_name = item.find("h1", attrs={"itemprop": "name"}).get_text(strip=True)
        item_price = item.find("li", attrs={"class": "price"}).get_text(strip=True)
        insert_db(item_name=item_name, shop_name="Мир Хвостатых", item_price=item_price)


def parse():
    for url in URLS:
        if url.startswith('moizver'):
            html = get_html('https://' + url)
            if html.status_code == 200:
                get_content_moizver(html.text)
            else:
                print('404 error')
        if url.startswith('mirhvost'):
            html = get_html('https://' + url)
            if html.status_code == 200:
                get_content_mirhvost(html.text)
            else:
                print('404 error')


parse()
