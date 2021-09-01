from dataclasses import dataclass
from typing import Optional
from .data_row import DataRow
from jsonpath_ng import jsonpath, parse


def get_val(json_obj: dict, path: str):
    if json_obj is None:
        return None
    jsonpath_obj = parse(path)
    match = jsonpath_obj.find(json_obj)
    if len(match) == 0:
        return None
    return match[0].value


@dataclass
class TipRanksRow(DataRow):
    symbol: str
    news_sentiment: float = None
    analyst_consensus: str = None
    analyst_price_target: float = None
    best_analyst_consensus: str = None
    best_analyst_price_target: float = None
    estimated_dividend_yield: float = None

    @classmethod
    def table_name(cls):
        return 'tip_ranks'

    def __init__(self, ticker: str, stock_data: dict, news_sentiment: dict):
        self.symbol = ticker
        if news_sentiment is not None:
            self.news_sentiment = news_sentiment.get("score")
        if stock_data is not None:
            self.analyst_consensus = get_val(stock_data, "$.analystConsensus.consensus")
            self.analyst_price_target = stock_data.get("priceTarget")
            self.best_analyst_consensus = get_val(stock_data, "$.bestAnalystConsensus.consensus")
            self.best_analyst_price_target = stock_data.get("bestPriceTarget")
            self.estimated_dividend_yield = stock_data.get("dividendYield")
