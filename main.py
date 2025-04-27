import logging
import os
import re
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
                log_level TEXT NOT NULL,
                api TEXT NOT NULL
            )
        ''')
    def get_total_count(self):
        try:
            self.cursor.execute('SELECT COUNT(*) AS total_records FROM logs')
            return self.cursor.fetchone()[0]
        except Exception as e:
            print(f"Ошибка при добавлении имени: {e}")

    def add_loglevel(self, log_level, api):
        try:
            self.cursor.execute('INSERT INTO logs (log_level, api) VALUES (?,?)', (log_level, api))
            self.connection.commit()
        except Exception as e:
            print(f"Ошибка при добавлении имени: {e}")

    def get_all(self):
        self.cursor.execute('SELECT * FROM logs')
        return self.cursor.fetchall()

    def get_report(self):
        self.cursor.execute(

            """
            SELECT 
            api,
            SUM(CASE WHEN log_level = 'DEBUG' THEN 1 ELSE 0 END) AS debug,
            SUM(CASE WHEN log_level = 'INFO' THEN 1 ELSE 0 END) AS info,
            SUM(CASE WHEN log_level = 'WARNING' THEN 1 ELSE 0 END) AS warning,
            SUM(CASE WHEN log_level = 'ERROR' THEN 1 ELSE 0 END) AS error,
            SUM(CASE WHEN log_level = 'CRITICAL' THEN 1 ELSE 0 END) AS critical
        FROM 
            logs
        GROUP BY 
            api
        ORDER BY 
            api
            """
        )
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

def is_valid_name(name):
    pattern = r'^[A-Za-z0-9]+$'
    if re.match(pattern, name):
        return name
    else:
        return ''

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

def get_only_api(data):
    position1 = data.find('/')
    position2 = len(data) - data[::-1].find('/')
    return data[position1:position2]


def convert_log(log_record):
    template = 'django.request'
    if template in log_record:
        correct_rec = log_record.split('000')[1]
        correct_rec = correct_rec.split(template)
        return correct_rec[0].strip() + ' ' + get_only_api(correct_rec[1])
    else:
        return ''


def read_logs_to_list(file_path):
    try:
        with open(file_path, 'r') as file:
            records = file.readlines()
        return [convert_log(rec) for rec in records if len(convert_log(rec))>0]
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []

def show_table(report:list, count:int, title:str):
    report = db.get_report()
    table = [['HANDLER', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']]
    sum_debug = sum_info = sum_warning = sum_error = sum_critical = 0
    for row in report:
        table_row = [row[0], row[1], row[2], row[3], row[4], row[5]]
        sum_debug = sum_debug + row[1]
        sum_info = sum_info + row[2]
        sum_warning = sum_warning + row[3]
        sum_error = sum_error + row[4]
        sum_critical = sum_critical + row[5]
        table.append(table_row)
    table_row = ['', '', '', '', '', '']
    table.append(table_row)
    table_row = ['', sum_debug, sum_info, sum_warning, sum_error, sum_critical]
    table.append(table_row)
    table_instance = DoubleTable(table, f" Total requests: {count}. {is_valid_name(title)} ")
    table_instance.justify_columns[2] = 'center'
    print()
    print(table_instance.table)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d - %(levelname)-8s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    base_dir = path.dirname(path.abspath(__file__))
    parsed_arguments = parse_arguments()
    logging.info(f"Запуск программы {parsed_arguments.report}")
    os.system('clear')
    db = DatabaseLogs()
    try:
        for log_file in parsed_arguments.log_files:
            logging.info(f'Обрабатываем файл: {log_file}')
            if file_exists(log_file):
                logs_list = read_logs_to_list(log_file)
                for log_line in logs_list:
                    db_rec = log_line.split(' ')
                    db.add_loglevel(db_rec[0], db_rec[1])
            else:
                logging.error(f"Файл '{log_file}' не найден.")

        show_table(db.get_report(), db.get_total_count(), parsed_arguments.report)

    except Exception as ex:
        print(f"Ошибка {ex}")
    db.close()

