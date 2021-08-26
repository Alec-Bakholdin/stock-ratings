from requests import get
from typing import List
from model import TipRanksRow, Company
from json import loads


def get_tip_ranks_data(companies: List[Company]) -> List[TipRanksRow]:
    symbols = ",".join(list(map(lambda co: co.symbol, companies)))
    url = f"https://www.tipranks.com/api/portfolio/getPortfolioHoldingStockData/?tickers={symbols}"
    response = get(url)
    json_arr = loads(response.text)
    return list(map(TipRanksRow, json_arr))
