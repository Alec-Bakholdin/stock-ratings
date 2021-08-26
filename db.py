from typing import List
from model import *
from datetime import date
import mysql.connector
import configparser

todayStr = str(date.today())
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


def close_db():
    conn.commit()
    conn.close()


def save_companies(companies: List[Company]):
    list_of_sql_values = list(map(lambda co: f"('{co.symbol}', '{co.company}')", companies))
    insert_query = "INSERT IGNORE INTO companies (symbol, company_name) values " + ", ".join(list_of_sql_values)
    cursor.execute(insert_query)


def save_zacks_data(zacks_rows: List[ZacksRow]):
    def map_zacks_row(row: ZacksRow) -> str:
        zacks_str = f"('{row.symbol}', '{todayStr}', {row.industry_rank}, {row.zacks_rank}, '{row.value_score}', '{row.growth_score}', '{row.momentum_score}', '{row.vgm_score}')";
        return zacks_str.replace("'None'", "null").replace("None", "null")
    list_of_sql_values = list(map(map_zacks_row, zacks_rows))
    insert_query = "INSERT IGNORE INTO zacks (symbol, date_retrieved, industry_rank, zacks_rank, value_score, growth_score, momentum_score, vgm_score) VALUES " + ", ".join(list_of_sql_values)
    cursor.execute(insert_query)


def save_tip_ranks_data(tip_ranks_rows: List[TipRanksRow]):
    def map_tip_ranks_row(row: TipRanksRow) -> str:
        return f"('{row.symbol}', '{todayStr}', '{row.analyst_consensus}', '{row.best_analyst_consensus}')"
    list_of_sql_values = list(map(map_tip_ranks_row, tip_ranks_rows))
    insert_query = "INSERT IGNORE INTO tip_ranks (symbol, date_retrieved, analyst_consensus, best_analyst_consensus) VALUES " + ", ".join(list_of_sql_values)
    cursor.execute(insert_query)
