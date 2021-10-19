from typing import List
from model import DataRow
from datetime import date
import mysql.connector
import configparser

today_str = str(date.today())
today_str_f = f"'{today_str}'"
config = configparser.ConfigParser()
config.read_file(open("./application.cfg"))
profile = 'REMOTE'
conn = mysql.connector.connect(
    host=config[profile]['host'],
    user=config[profile]['user'],
    password=config[profile]['password'],
    database=config[profile]['database'],
    port=config[profile]['port']
)
cursor = conn.cursor()
cursor.execute('set max_allowed_packet=67108864')


def close_db():
    conn.commit()
    conn.close()


def save_data_rows(data_rows: List[DataRow], data_type, include_date: bool = True):
    table_name = data_type.table_name()
    fields_list = data_type.field_names_list()
    fields_str = f"({', '.join(fields_list)}{', date_retrieved' if include_date else ''})"

    def row_to_sql_value(row):
        return f"({','.join(row.field_values() + ([today_str_f] if include_date else []))})"

    values_str = ", ".join(list(map(row_to_sql_value, data_rows)))
    on_duplicate_str = ", ".join(list(map(lambda x: f"{x} = VALUES({x})", fields_list)))
    sql_command = f"INSERT IGNORE INTO {table_name} {fields_str} " \
                  f"VALUES {values_str} " \
                  f"ON DUPLICATE KEY UPDATE {on_duplicate_str};"
    print(f"\nExecuting SQL Query: {sql_command}")
    cursor.execute(sql_command)
    conn.commit()
