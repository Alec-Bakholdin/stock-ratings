from dataclasses import dataclass
from .data_row import DataRow


@dataclass
class Company(DataRow):
    symbol: str
    company_name: str
    latest_price: float

    @classmethod
    def table_name(cls):
        return 'companies'

    def __init__(self, symbol: str, company: str, latest_price: float):
        self.symbol = symbol
        self.company_name = company
        self.latest_price = latest_price
