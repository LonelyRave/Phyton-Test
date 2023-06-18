# import argparse
# import os
# import requests
# import fitz
# from bs4 import BeautifulSoup
#
#
# class LinkParser:
#     def __init__(self, file_path):
#         self.file_path = file_path
#
#     def parse_links(self):
#         file_extension = os.path.splitext(self.file_path)[1]
#
#         if file_extension == '.html':
#             with open(self.file_path, 'r') as f:
#                 soup = BeautifulSoup(f, 'html.parser')
#                 links = soup.find_all('a')
#                 return [link.get('href') for link in links]
#
#         elif file_extension == '.pdf':
#             links = extract_links_from_pdf(self.file_path)
#             return links
#
#         else:
#             print('Неподдерживаемый формат файла.')
#             return []
#
#
# def extract_links_from_pdf(file_path):
#     doc = fitz.open(file_path)
#     links = []
#
#     for page in doc:
#         page_links = page.get_links()
#         for link in page_links:
#             if link['kind'] == 1:
#                 uri = link['uri']
#                 links.append(uri)
#
#     doc.close()
#     return links
#
#
# class LinkValidator:
#     def is_valid(self, link):
#         response = requests.get(link)
#         return response.status_code == 200
#
#
# class LinkProcessor:
#     def __init__(self, link_parser, link_validator):
#         self.link_parser = link_parser
#         self.link_validator = link_validator
#
#     def process_links(self):
#         links = self.link_parser.parse_links()
#         valid_links = []
#         broken_links = []
#
#         for link in links:
#             if self.link_validator.is_valid(link):
#                 valid_links.append(link)
#             else:
#                 broken_links.append(link)
#
#         return valid_links, broken_links
#
#
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='HTML и PDF парсер ссылок')
#     parser.add_argument('-html', type=str, help='Путь к HTML файлу')
#     parser.add_argument('-pdf', type=str, help='Путь к PDF файлу')
#     parser.add_argument('-url', type=str, help='URL для парсинга')
#
#     args = parser.parse_args()
#
#     if args.html:
#         file_path = args.html
#     elif args.pdf:
#         file_path = args.pdf
#     elif args.url:
#         file_path = args.url
#     else:
#         file_path = input('Введите путь к HTML или PDF файлу или введите URL: ')
#
#     link_parser = LinkParser(file_path)
#     link_validator = LinkValidator()
#     link_processor = LinkProcessor(link_parser, link_validator)
#     valid_links, broken_links = link_processor.process_links()
#
#     print('Найденные ссылки:')
#     for link in valid_links:
#         print(link)
#
#     print('Нерабочие ссылки:')
#     for link in broken_links:
#         print(link)
import argparse
import os
import requests
import fitz
from bs4 import BeautifulSoup
import logging

logging.basicConfig(filename='logfile.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class LinkParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse_links(self):
        file_extension = os.path.splitext(self.file_path)[1]

        if file_extension == '.html':
            with open(self.file_path, 'r') as f:
                soup = BeautifulSoup(f, 'html.parser')
                links = soup.find_all('a')
                return [link.get('href') for link in links]

        elif file_extension == '.pdf':
            links = extract_links_from_pdf(self.file_path)
            return links

        else:
            logging.warning('Неподдерживаемый формат файла.')
            return []


def extract_links_from_pdf(file_path):
    doc = fitz.open(file_path)
    links = []

    for page in doc:
        page_links = page.get_links()
        for link in page_links:
            if link['kind'] == 1:
                uri = link['uri']
                links.append(uri)

    doc.close()
    return links




class LinkValidator:
    def is_valid(self, link):
        response = requests.get(link)
        return response.status_code == 200


class LinkProcessor:
    def __init__(self, link_parser, link_validator):
        self.link_parser = link_parser
        self.link_validator = link_validator

    def process_links(self):
        links = self.link_parser.parse_links()
        valid_links = []
        broken_links = []

        for link in links:
            if self.link_validator.is_valid(link):
                valid_links.append(link)
            else:
                broken_links.append(link)

        return valid_links, broken_links


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HTML и PDF парсер ссылок')
    parser.add_argument('-html', type=str, help='Путь к HTML файлу')
    parser.add_argument('-pdf', type=str, help='Путь к PDF файлу')
    parser.add_argument('-url', type=str, help='URL для парсинга')

    args = parser.parse_args()

    if args.html:
        file_path = args.html
    elif args.pdf:
        file_path = args.pdf
    elif args.url:
        file_path = args.url
    else:
        file_path = input('Введите путь к HTML или PDF файлу или введите URL: ')

    link_parser = LinkParser(file_path)
    link_validator = LinkValidator()
    link_processor = LinkProcessor(link_parser, link_validator)
    valid_links, broken_links = link_processor.process_links()

    logging.info('Найденные ссылки:')
    for link in valid_links:
        logging.info(link)

    logging.info('Нерабочие ссылки:')
    for link in broken_links:
        logging.info(link)

