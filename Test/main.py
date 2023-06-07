import argparse
import requests
from bs4 import BeautifulSoup


def parse_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')
        valid_links = []
        broken_links = []

        for link in links:
            href = link.get('href')
            if href:
                if href.startswith('http://') or href.startswith('https://'):
                    if requests.get(href).status_code == 200:
                        valid_links.append(href)
                    else:
                        broken_links.append(href)

        with open('valid_links.txt', 'w') as f:
            for link in valid_links:
                f.write(link + '\n')

        with open('broken_links.txt', 'w') as f:
            for link in broken_links:
                f.write(link + '\n')

        print('Парсинг завершен. Найденные ссылки сохранены в файлы valid_links.txt и broken_links.txt.')
    else:
        print('Не удалось выполнить запрос. Проверьте ссылку и попробуйте снова.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HTML страницы парсера')
    parser.add_argument('-url', type=str, help='URL HTML страницы')

    args = parser.parse_args()

    if args.url:
        parse_html(args.url)
    else:
        url = input('Введите URL HTML страницы: ')
        parse_html(url)
