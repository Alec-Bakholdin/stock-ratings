from zacks import get_zacks_data
from tipRanks import get_tip_ranks_data
from model import Company
from db import save_companies, save_zacks_data, save_tip_ranks_data, close_db

zacks_data = get_zacks_data()
target_companies = list(map(lambda row: Company(row.symbol, row.company), zacks_data))
save_companies(target_companies)
save_zacks_data(zacks_data)
tip_ranks_data = get_tip_ranks_data(target_companies)
save_tip_ranks_data(tip_ranks_data)

close_db()
