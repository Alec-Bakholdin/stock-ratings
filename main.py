from zacks import get_zacks_data
from tipRanks import get_tip_ranks_data
from model import *
from db import save_data_rows, close_db

zacks_data = get_zacks_data()
target_companies = list(map(lambda row: Company(row.symbol, row.company, row.price), zacks_data))
save_data_rows(target_companies, Company)
save_data_rows(zacks_data, ZacksRow)
tip_ranks_data = get_tip_ranks_data(target_companies)
save_data_rows(tip_ranks_data, TipRanksRow)

close_db()
