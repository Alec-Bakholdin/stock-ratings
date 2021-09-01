from requests import get
from typing import List
from model import TipRanksRow, Company
from json import loads
from time import perf_counter


def get_stock_data(symbols: List[str]) -> dict:
    symbols_str = ",".join(symbols)
    url = f"https://www.tipranks.com/api/portfolio/getPortfolioHoldingStockData/?tickers={symbols_str}"
    response = get(url)
    return dict((company["ticker"], company) for company in loads(response.text))


def get_news_sentiments(symbols: List[str]) -> dict:
    symbols_str = ",".join(symbols)
    url = f"https://www.tipranks.com/api/stocks/GetTickersNewsSentiments?tickers={symbols_str}"
    response = get(url)
    return dict((company["ticker"], company) for company in loads(response.text))


def get_tip_ranks_data(companies: List[Company]) -> List[TipRanksRow]:
    print("\n\n* * * * * * * * * * * * * * * * * * * *\nFetching TipRanks data...")
    start = perf_counter()
    symbols = list(map(lambda co: co.symbol, companies))
    stock_data = get_stock_data(symbols)
    news_sentiments = get_news_sentiments(symbols)

    tip_ranks_rows = list(map(lambda ticker: TipRanksRow(ticker, stock_data.get(ticker), news_sentiments.get(ticker)), symbols))

    end = perf_counter()
    print("Success!")
    print("    Elapsed time: %f s" % (end - start))
    print("    Number of entries: %d" % (len(tip_ranks_rows)))
    return tip_ranks_rows
