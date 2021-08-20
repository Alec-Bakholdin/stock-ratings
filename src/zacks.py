import typing
from helper import LetterRating
from dataclasses import dataclass
from requests import post
import csv


@dataclass(init=False)
class ZacksRow:
    ticker: str
    industry_rank: int
    zacks_rank: int
    value_score: LetterRating
    growth_score: LetterRating
    momentum_score: LetterRating
    VGM_score: LetterRating


def csv_row_to_zacks_row(csv_row: typing.List[str]) -> ZacksRow:
    zacks_row = ZacksRow()

    zacks_row.ticker = csv_row[0]
    zacks_row.industry_rank = -1 if csv_row[6] == 'NA' else int(csv_row[6])
    zacks_row.zacks_rank = -1 if csv_row[7] == 'NA' else int(csv_row[7])
    zacks_row.value_score = csv_row[8]
    zacks_row.growth_score = csv_row[9]
    zacks_row.momentum_score = csv_row[10]
    zacks_row.VGM_score = csv_row[11]

    return zacks_row


def get_data() -> typing.List[ZacksRow]:
    url = "https://www.zacks.com/portfolios/tools/ajxExportExel.php"

    payload = 'export_data_init_tab=2282242_update_zYjM1ADO0kjN&export_data_rest_tab=&XLS_FILE=Oleg%2BHoldings%2B-%2Bupdate'
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://www.zacks.com',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/9',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = post(url, headers=headers, data=payload)

    csv_rows = list(csv.reader(response.text.split('\n')));
    header_row = csv_rows[0]
    print(header_row)
    data_rows = filter(lambda x: len(x) == 12, csv_rows[1:])
    return list(map(csv_row_to_zacks_row, data_rows))