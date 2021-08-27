from requests import get
from typing import List
from model import TipRanksRow, Company
from json import loads
from time import perf_counter


def get_tip_ranks_data(companies: List[Company]) -> List[TipRanksRow]:
    print("\n\n* * * * * * * * * * * * * * * * * * * *\nFetching TipRanks data...")
    start = perf_counter()
    symbols = ",".join(list(map(lambda co: co.symbol, companies)))
    url = f"https://www.tipranks.com/api/portfolio/getPortfolioHoldingStockData/?tickers={symbols}"
    response = get(url)
    json_arr = loads(response.text)
    data = list(map(TipRanksRow, json_arr))

    end = perf_counter()
    print("Success!")
    print("    Elapsed time: %f s" % (end - start))
    print("    Number of entries: %d" % (len(data)))
    return data
