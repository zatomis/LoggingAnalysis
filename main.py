import logging
import os
from os import path
from terminaltables import DoubleTable
import argparse
from urllib.parse import urlsplit, urljoin


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Анализ журнала логирования django-приложения"
    )

    parser.add_argument('log_files', nargs='+', help='Список лог-файлов для обработки')

    parser.add_argument(
        '--report',
        default='Отчет django-приложения',
        type=str,
        help='Укажите название отчета',
    )
    args = parser.parse_args()
    return args


def get_file_path(url):
    path, filename = os.path.split(urlsplit(url).path)
    return filename


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d - %(levelname)-8s - %(message)s'
    )

    logger = logging.getLogger(__name__)
    base_dir = path.dirname(path.abspath(__file__))
    parsed_arguments = parse_arguments()

    books_descriptions = []
    book_id = 0
    print(parsed_arguments.report)

    for log_file in parsed_arguments.log_files:
        print(f'Обрабатываем файл: {log_file}')





