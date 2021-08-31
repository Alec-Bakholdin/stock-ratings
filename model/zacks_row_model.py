from dataclasses import dataclass
from typing import List
from .data_row import DataRow

indices = {
    "symbol": 0,
    "company": 1,
    "price": 2,
    "industry_rank": 6,
    "zacks_rank": 7,
    "value_score": 8,
    "growth_score": 9,
    "momentum_score": 10,
    "vgm_score": 11
}


@dataclass
class ZacksRow(DataRow):
    symbol: str
    price: float
    industry_rank: int
    zacks_rank: int
    value_score: str
    growth_score: str
    momentum_score: str
    vgm_score: str
    _company: str

    @property
    def company(self) -> str:
        return self._company

    @classmethod
    def table_name(cls):
        return 'zacks'

    @staticmethod
    def validate_headers(header_row):
        keys = list(indices.keys())
        for i in range(len(keys)):
            header_name = keys[i]
            if str(header_row[indices[header_name]]).lower().replace(" ", "_") != header_name:
                raise Exception('invalid header row! Something changed')

    @staticmethod
    def get_val(csv_row: List[str], header_name: str, is_int: bool = False, is_float: bool = False):
        val = csv_row[indices[header_name]]
        if val == 'NA':
            return None
        elif is_int:
            return int(val)
        elif is_float:
            return float(val.replace(',', ''))
        return val

    def __init__(self, csv_row: List[str]):
        self.symbol = self.get_val(csv_row, "symbol")
        self.price = self.get_val(csv_row, "price", False, True)
        self.industry_rank = self.get_val(csv_row, "industry_rank", True)
        self.zacks_rank = self.get_val(csv_row, "zacks_rank", True)
        self.value_score = self.get_val(csv_row, "value_score")
        self.growth_score = self.get_val(csv_row, "growth_score")
        self.momentum_score = self.get_val(csv_row, "momentum_score")
        self.vgm_score = self.get_val(csv_row, "vgm_score")
        self._company = self.get_val(csv_row, "company")
