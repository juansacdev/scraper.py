import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_links_from_main_page(url):
    # Peticion a la main page
    res = requests.get(url)
    if res.status_code != 200:
        return False
    else:
        soup = BeautifulSoup(res.content.decode('utf-8'), 'html.parser')
        articles = soup.find_all(
            name='div',
            attrs={'class': 'article-box'}
        )
        link_list = [
            f'{url}{link.find("a")["href"]}' for link in articles if link.find('a') != None]

        return link_list


def get_data_from_link(link_to_scrap, file_name):
    try:
        # request al link
        res = requests.get(link_to_scrap)
        if res.status_code != 200:
            return False

        else:
            soup = BeautifulSoup(res.content.decode('utf-8'), 'html.parser')

            try:
                title = soup.find(
                    'span', attrs={'class': 'priority-content'}).text.replace(' |', ',')
            except:
                title = ''

            try:
                sub_title = soup.find(
                    'ul', attrs={'class': 'list-subtitle'}).find('li').text
            except:
                sub_title = ''

            try:
                author = soup.find(
                    'span', attrs={'class': 'author-date'}).find('strong').text
            except:
                author = ''

            try:
                author_articles = f"{URL}{soup.find('span', attrs={'class': 'author-date'}).find('a')['href']}"
            except:
                author_articles = ''

            try:
                datetime = soup.find(
                    'span', attrs={'class': 'author-date'}).find('time').text
            except:
                datetime = ''

            try:
                article = ''
                if soup.find(
                        'div', attrs={'class': 'text'}).find_all('p'):
                    paragraphos = soup.find(
                        'div', attrs={'class': 'text'}).find_all('p')
                    for p in paragraphos:
                        article += f'{p.text} '
                elif (soup.find('div', attrs={'class': 'text'}).find('h2').text):
                    article = soup.find(
                        'div', attrs={'class': 'text'}).find('h2').text
                else:
                    article = ''

            except:
                article = ''

            try:
                if soup.find(
                        'div', attrs={'class': 'categoryTitle'}).find_all('a'):
                    tags = soup.find(
                        'div', attrs={'class': 'categoryTitle'}).find_all('a')
                    tags = [
                        tag.text for tag in tags if tag != None]
                    tags = '. '.join(tags)
                elif (len(soup.find_all('article', attrs={
                        'class': 'categoryListItem categoryArticleItem'})) > 0):
                    tags = soup.find_all(
                        'article', attrs={'class': 'categoryListItem categoryArticleItem'})
                    tags = [tag.find('a').text.strip() for tag in tags]
                    tags = '. '.join(tags)
                else:
                    tags = ''
            except:
                tags = ''

            try:
                img = soup.find('div', attrs={'class': 'img-container'}).find(
                    'img')['data-srcset'].split(' ')[0].replace('//', '')
            except:
                img = ''

                data = {
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
                write_data_into_file(data, file_name)

    except Exception as e:
        if 'Exceeded 30 redirects.' in e.args:
            print(e)
            print(link_to_scrap)

        else:
            print(link_to_scrap)
            print(f'Error:\n{e}\n')


def write_data_into_file(obj, file_name):
    with open(file=f'./public/{file_name}', mode='a', encoding='utf-8') as f:
        f.write(
            f'{obj["title"]}|{obj["sub_title"]}|{obj["article"]}|{obj["author"]}|{obj["author_articles"]}|{obj["tags"]}|{obj["img"]}|{obj["link"]}|{obj["datetime"]}\n')
        f.close()
        print(f'writing...')


def main(url, file_name):
    links_articles = get_links_from_main_page(url)
    links_articles = list(filter(lambda link: ("encuestas" not in link) and (
        "/horoscopo/" not in link) and ("/opinion/" not in link) and ("/cronologia-autor/" not in link) and ("/fotos/" not in link), links_articles))

    for link in links_articles:
        get_data_from_link(link, file_name)

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
