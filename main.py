import requests
from bs4 import BeautifulSoup
from datetime import datetime, date as dt
URL = 'https://www.diariolibre.com/'


# FILE_NAME = f'{datetime.now().strftime("%d%m%Y-%H%M%S")}'

def card_html_to_obj(card):
    try:
        titular = card.find(class_='priority-content').text
        news_link = card.find('a')['href']
        description = card.find(class_='cutline-text').text
        tag = card.find(class_='row info-container py-2 px-3').find('a').text
        # eslint-disable next line
        tag_link = card.find(
            class_='row info-container py-2 px-3').find('a')['href']
        img = card.find('img')['data-srcset']
        # date = dt.today().strftime("%d/%m/%Y")

    except:
        titular = ''
        news_link = ''
        description = ''
        tag = ''
        tag_link = ''
        img = ''

    return {
        'titular': titular,
        'news_link': news_link,
        'description': description,
        'tag': tag,
        'tag_link': tag_link,
        'img': img,
        # 'date': date,
    }


def main():
    page = requests.get(URL)

    # headers_res = page.headers
    # headers_req = page.request.headers
    # status_code = page.status_code
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'lxml')
        all_items_news = soup.find_all(
            "article",
            class_="article element full-access norestricted"
        )

    # print(card_html_to_obj(all_items_news[0]))

    item = all_items_news[1]
    titular = item.find(class_='priority-content').text
    news_link = item.find('a')['href']
    description = item.find(class_='cutline-text').text
    try:
        tag = item.find(class_='row info-container py-2 px-3').find('a').text
        tag_link = item.find(
            class_='row info-container py-2 px-3').find('a')['href']
    except:
        tag = item.find(class_='float-left mr-1 author').find('a').text
        tag_link = item.find(
            class_='float-left mr-1 author').find('a')['href']
        img = item.find('img')['data-srcset']
    # date = dt.today().strftime("%d/%m/%Y")

    print({
        'titular': titular,
        'news_link': news_link,
        'description': description,
        'tag': tag,
        'tag_link': tag_link,
        'img': img,
    })

    # for item in all_items_news:
    #     try:
    #         item.find('img')['data-srcset']
    #     except:
    #         print(all_items_news.index(item))
    #         # continue


if __name__ == '__main__':
    main()
