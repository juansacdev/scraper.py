import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date as dt
URL = 'https://www.diariolibre.com'
FILE_NAME = f'{datetime.now().strftime("%d%m%Y%H%M%S")}.csv'
START = time.time()


with open(f'./public/{FILE_NAME}', 'w', encoding='utf-8') as f:
    f.write('title|link|description|tag|tag_link|image|date\n')
    f.close()


def card_html_to_obj(card):
    # caching error with title
    if card.find('span', attrs={'class': 'priority-content'}) != None:
        title = card.find(
            'span', attrs={'class': 'priority-content'}).text.replace(' |', ',')
    else:
        title = None

    # caching error with link
    if card.find('a', attrs={'class': 'cutlineShow'}) != None:
        link = f"{URL}{card.find('a', attrs={'class': 'cutlineShow'})['href']}"
    elif card.find('div', attrs={'class': 'article-box'}) != None:
        link = f"{URL}{card.find('div', attrs={'class': 'article-box'}).find('a')['href']}"
    else:
        link = None

    # # caching error with description
    if card.find('span', attrs={'class': 'cutline-text'}) != None:
        description = card.find('span', attrs={'class': 'cutline-text'}).text
    else:
        description = None

    # caching error with tag
    if card.find('div', attrs={'class': 'row info-container py-2 px-3'}) != None:
        tag = card.find(
            'div', attrs={'class': 'row info-container py-2 px-3'}).find('a').text
        tag_link = f'{URL}{card.find("div", attrs={"class": "row info-container py-2 px-3"}).find("a")["href"]}'

    elif card.find('div', attrs={'class': 'float-left mr-1 author'}) != None:
        tag = card.find(
            'div', attrs={'class': 'float-left mr-1 author'}).find('a').text
        tag_link = f'{URL}{card.find("div", attrs={"class": "float-left mr-1 author"}).find("a")["href"]}'
    else:
        tag = None
        tag_link = None

    # caching error with img
    if card.find('div', attrs={'class': 'img-container'}) != None:
        img = card.find('div', attrs={'class': 'img-container'}).find(
            'img')['data-srcset'].split(' ')[0].replace('//', '')
    else:
        img = None

    date = dt.today().strftime("%d/%m/%Y")

    with open(f'./public/{FILE_NAME}', 'a', encoding='utf-8') as f:
        f.write(f'{title}|{link}|{description}|{tag}|{tag_link}|{img}|{date}\n')
        f.close()


def main():
    page = requests.get(URL)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'lxml')
        all_items_news = soup.find_all(
            "article",
            class_="article element full-access norestricted"
        )

    for card in all_items_news:
        card_html_to_obj(card)

    print(time.time() - START)


if __name__ == '__main__':
    main()
