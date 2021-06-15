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
            soup = BeautifulSoup(res.content.decode(
                encoding='utf-8'), 'html.parser')

            try:
                title = soup.find(
                    'span', attrs={'class': 'priority-content'}).text.replace(' |', ',')
            except:
                title = ''
                # print(f'Title not found in: {link_to_scrap}')

            # if not soup.find('span', attrs={'class': 'priority-content'}):
            #     title = ''
            # else:
            #     title = soup.find(
            #         'span', attrs={'class': 'priority-content'}).text.replace(' |', ',')

            try:
                sub_title = soup.find(
                    'ul', attrs={'class': 'list-subtitle'}).find('li').text
            except:
                sub_title = ''
                # print(f'Sub title not found in: {link_to_scrap}')

            # if not soup.find('ul', attrs={'class': 'list-subtitle'}):
            #     sub_title = ''
            # else:
            #     sub_title = soup.find(
            #         'ul', attrs={'class': 'list-subtitle'})

            try:
                author = soup.find(
                    'span', attrs={'class': 'author-date'}).find('strong').text
                author_articles = f"{URL}{soup.find('span', attrs={'class': 'author-date'}).find('a')['href']}"
                datetime = soup.find(
                    'span', attrs={'class': 'author-date'}).find('time').text

            except:
                author = ''
                author_articles = ''
                datetime = ''
                # print(f'Data author not found in: {link_to_scrap}')

            # if not soup.find('span', attrs={'class': 'author-date'}):
            #     author = ''
            #     author_articles = ''
            # else:
            #     author = soup.find(
            #         'span', attrs={'class': 'author-date'}).find('strong').text
            #     author_articles = f"{URL}{soup.find('span', attrs={'class': 'author-date'}).find('a')['href']}"

            try:
                article = ''
                paragraphos = soup.find(
                    'div', attrs={'class': 'text'}).find_all('p')
                for p in paragraphos:
                    article += f'{p.text} '

            except:
                article = ''
                # print(f'Article not found in: {link_to_scrap}')

            # if soup.find('div', attrs={'class': 'text'}) != None:
                # article = ''
            #     paragraphos = soup.find(
            #         'div', attrs={'class': 'text'}).find_all('p')
            #     for p in paragraphos:
            #         article += f'{p.text} '
            # else:
                # article = ''

            try:
                tags = soup.find(
                    'div', attrs={'class': 'categoryTitle'}).find_all('a')
                tags = [tag.text for tag in tags]
                tags = '. '.join(tags)
            except:
                tags = ''
                # print(f'Tags not found in: {link_to_scrap}')

            # if not soup.find('div', attrs={'class': 'categoryTitle'}):
            #     tags = ''
            # else:
            #     tags = soup.find(
            #         'div', attrs={'class': 'categoryTitle'}).find_all('a')
            #     tags = [tag.text for tag in tags]
            #     tags = '. '.join(tags)

            try:
                img = soup.find('div', attrs={'class': 'img-container'}).find(
                    'img')['data-srcset'].split(' ')[0].replace('//', '')
            except:
                if soup.find('video', attrs={'class': 'jw-video jw-reset'}) != None:
                    img = '(Video) - Unsupported format'
                else:
                    img = ''

            # if soup.find(
            #         'span', attrs={'class': 'author-date'}).find('time') != None:
            #     datetime = soup.find(
            #         'span', attrs={'class': 'author-date'}).find('time').text
            # else:
            #     datetime = ''

            if ((title == '') or (sub_title == '') or (author == '') or (author_articles == '') or (datetime == '') or (article == '') or (tags == '') or (img == '')):
                bad_data = {
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
                write_file_with_error(bad_data, file_name)

            elif (title and sub_title and author and author_articles and datetime and article and tags and img):
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
            print(f'Error:\n{e}\n')


def write_data_into_file(obj, file_name):
    with open(file=f'./public/{file_name}', mode='a', encoding='utf-8') as f:
        f.write(
            f'{obj["title"]}|{obj["sub_title"]}|{obj["article"]}|{obj["author"]}|{obj["author_articles"]}|{obj["tags"]}|{obj["img"]}|{obj["link"]}|{obj["datetime"]}\n')
        f.close()
        print(f'writing...')


def write_file_with_error(obj, file_name):
    with open(file=f'./errors/{file_name}', mode='a', encoding='utf-8') as f:
        f.write(
            f'{obj["title"]}|{obj["sub_title"]}|{obj["article"]}|{obj["author"]}|{obj["author_articles"]}|{obj["tags"]}|{obj["img"]}|{obj["link"]}|{obj["datetime"]}\n')
        f.close()


def main(url, file_name):
    links_articles = get_links_from_main_page(url)

    for link in links_articles:
        if ("encuestas" not in link) and ("/horoscopo/" not in link) and ("/opinion/" not in link) and ("/cronologia-autor/" not in link):
            get_data_from_link(link, file_name)
        else:
            print(f'Skiping: {link}')
            continue

    print(f'Time: {time.time() - START} seg')


if __name__ == '__main__':
    URL = 'https://www.diariolibre.com'
    FILE_NAME = f'{datetime.now().strftime("%d%m%Y%H%M%S")}.csv'
    START = time.time()

    with open(file=f'./public/{FILE_NAME}', mode='w', encoding='utf-8') as f:
        f.write(
            'title|sub_title|article|author|author_articles|tags|img|link|datetime\n')
        f.close()

    with open(file=f'./errors/{FILE_NAME}', mode='w', encoding='utf-8') as f:
        f.write(
            'title|sub_title|article|author|author_articles|tags|img|link|datetime\n')
        f.close()

    main(URL, FILE_NAME)
