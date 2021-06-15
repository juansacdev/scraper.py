import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_links_from_main_page(url):
    try:
        # Peticion a la main page
        res = requests.get(url)
        assert res.status_code == 200, 'Error in request'
        soup = BeautifulSoup(res.content.decode('utf-8'), 'html.parser')
        articles = soup.find_all(
            name='div',
            attrs={'class': 'article-box'}
        )
        link_list = [
            f'{URL}{link.find("a")["href"]}' for link in articles if link.find('a') != None]

        return link_list

    except AssertionError as ae:
        print(ae)
        return False


def get_data_from_link(link_to_scrap):
    try:
        # request al link
        res = requests.get(link_to_scrap)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content.decode(
                encoding='utf-8'), 'html.parser')

            bad_links = []

            if not soup.find('span', attrs={'class': 'priority-content'}):
                title = ''
            else:
                title = soup.find(
                    'span', attrs={'class': 'priority-content'}).text.replace(' |', ',')

            if not soup.find('ul', attrs={'class': 'list-subtitle'}):
                sub_title = ''
            else:
                sub_title = soup.find(
                    'ul', attrs={'class': 'list-subtitle'}).find('li').text

            if not soup.find('span', attrs={'class': 'author-date'}):
                author = ''
                author_articles = ''
            else:
                author = soup.find(
                    'span', attrs={'class': 'author-date'}).find('strong').text
                author_articles = f"{URL}{soup.find('span', attrs={'class': 'author-date'}).find('a')['href']}"

            article = ''
            if soup.find('div', attrs={'class': 'text'}) != None:
                paragraphos = soup.find(
                    'div', attrs={'class': 'text'}).find_all('p')
                for p in paragraphos:
                    article += f'{p.text} '

            if not soup.find('div', attrs={'class': 'categoryTitle'}):
                tags = ''
            else:
                tags = soup.find(
                    'div', attrs={'class': 'categoryTitle'}).find_all('a')
                tags = [tag.text for tag in tags]
                tags = '. '.join(tags)
                tags

            try:
                if not soup.find('div', attrs={'class': 'img-container'}):
                    raise AttributeError('No image')
                else:
                    img = soup.find('div', attrs={'class': 'img-container'}).find(
                        'img')['data-srcset'].split(' ')[0].replace('//', '')
            except:
                img = '(Video) - Unsupported format'

            if soup.find(
                    'span', attrs={'class': 'author-date'}).find('time') != None:
                datetime = soup.find(
                    'span', attrs={'class': 'author-date'}).find('time').text
            else:
                datetime = ''

            if (title and sub_title and author and author_articles and article) != '':
                return {
                    'title': title,
                    'sub_title': sub_title,
                    'article': article,
                    'author': author,
                    'author_articles': author_articles,
                    'tags': tags,
                    'img': img,
                    'link': link_to_scrap,
                    'datetime': datetime,
                }

            else:
                return False

    except:
        bad_links.append(link_to_scrap)


def write_data_into_file(obj, file_name):
    with open(file=f'./public/{file_name}', mode='a', encoding='utf-8') as f:
        f.write(
            f'{obj["title"]}|{obj["sub_title"]}|{obj["article"]}|{obj["author"]}|{obj["author_articles"]}|{obj["tags"]}|{obj["img"]}|{obj["link"]}|{obj["datetime"]}\n')
        f.close()
        print(f'writing...')


def main(url, file_name):
    links_articles = get_links_from_main_page(url)

    for link in links_articles:
        if ("encuestas" or "horoscopo") in link:
            continue

        data = get_data_from_link(link)

        if not data:
            continue

        else:
            write_data_into_file(data, file_name)

    print(f'Time: {time.time() - START} seg')


if __name__ == '__main__':
    URL = 'https://www.diariolibre.com'
    FILE_NAME = f'{datetime.now().strftime("%d%m%Y%H%M%S")}.csv'
    START = time.time()

    with open(file=f'./public/{FILE_NAME}', mode='w', encoding='utf-8') as f:
        f.write(
            'title|sub_title|article|author|author_articles|tags|img|link|datetime\n')
        f.close()

    main(URL, FILE_NAME)
