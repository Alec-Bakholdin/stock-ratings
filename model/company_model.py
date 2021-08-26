from dataclasses import dataclass

@dataclass
class Company:
    symbol: str
    company: str

    def __init__(self, symbol: str, company: str):
        self.symbol = symbol
        self.company = company
