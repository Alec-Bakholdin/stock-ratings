from dataclasses import dataclass
from .data_row import DataRow


@dataclass
class YahooRow(DataRow):
    symbol: str
    short_term: str = None
    mid_term: str = None
    long_term: str = None
    estimated_return: float = None
    fair_value: str = None

    @classmethod
    def table_name(cls):
        return 'yahoo'

    def __init__(self, symbol):
        self.symbol = symbol
