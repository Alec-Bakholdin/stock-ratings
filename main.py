from zacks import get_zacks_data
from tip_ranks import get_tip_ranks_data
from yahoo import get_yahoo_data
from model import *
from db import open_db, close_db, save_data_rows


def print_divider(header: str):
    divider = 160*"="
    print(divider)
    print(divider)
    print(header)


print_divider("Fetching Zacks Data...")
zacks_data = get_zacks_data()
target_companies = list(map(lambda row: Company(row.symbol, row.company, row.price), zacks_data))
print_divider("Fetching TipRanks Data...")
tip_ranks_data = get_tip_ranks_data(target_companies)
print_divider("Fetching Yahoo Data...")
yahoo_data = get_yahoo_data(target_companies)


conn = open_db()
print_divider("Saving Companies to Database...")
save_data_rows(conn, target_companies, Company, False)
print_divider("Saving Zacks Data to Database...")
save_data_rows(conn, zacks_data, ZacksRow)
print_divider("Saving TipRanks Data to Database...")
save_data_rows(conn, tip_ranks_data, TipRanksRow)
print_divider("Saving Yahoo Data to Database...")
save_data_rows(conn, yahoo_data, YahooRow)
close_db(conn)

print_divider("SUCCESSFULLY COMPLETED ALL OPERATIONS")
