import logging
import os
from os import path
import sqlite3
from terminaltables import DoubleTable
import argparse
from urllib.parse import urlsplit, urljoin


class DatabaseLogs:
    def __init__(self):
        self.connection = sqlite3.connect(':memory:')
        self.cursor = self.connection.cursor()

        self.cursor.execute('''
            CREATE TABLE logs (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')

    def add_name(self, record):
        try:
            self.cursor.execute('INSERT INTO logs (name) VALUES (?)', (name,))
            self.connection.commit()
            print(f"Имя '{name}' успешно добавлено.")
        except Exception as e:
            print(f"Ошибка при добавлении имени: {e}")

    def get_all_names(self):
        self.cursor.execute('SELECT * FROM names')
        return self.cursor.fetchall()

    def close(self):
        """Закрывает соединение с базой данных."""
        self.connection.close()


    # db = DatabaseLogs()
    # db.add_name("Alice")
    # db.add_name("Bob")
    # names = db.get_all_names()
    # print("Список имен в базе данных:")
    # for id, name in names:
    #     print(f"{id}: {name}")
    # db.close()



def file_exists(path):
    return os.path.isfile(path)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Анализ журнала логирования django-приложения"
    )

    parser.add_argument('log_files',
                        nargs='+',
                        help='Список лог-файлов для обработки')

    parser.add_argument(
        '--report',
        default='Отчет django-приложения',
        type=str,
        help='Укажите название отчета',
    )
    args = parser.parse_args()
    return args

def read_logs_to_list(file_path):
    try:
        with open(file_path, 'r') as file:
            records = file.readlines()
        return [rec.strip() for rec in records]
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d - %(levelname)-8s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    base_dir = path.dirname(path.abspath(__file__))
    parsed_arguments = parse_arguments()
    logging.info(f"Запуск программы {parsed_arguments.report}")

    try:
        for log_file in parsed_arguments.log_files:
            logging.info(f'Обрабатываем файл: {log_file}')
            if file_exists(log_file):
                print(f"Файл '{log_file}' существует.")
                logs_list = read_logs_to_list(log_file)
                for line in logs_list[:5]:
                    print(line)

            else:
                logging.error(f"Файл '{log_file}' не найден.")

    except Exception as ex:
        print(f"Ошибка {ex}")


