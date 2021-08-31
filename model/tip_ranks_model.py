from dataclasses import dataclass
from typing import Optional
from .data_row import DataRow


def get_val(json_obj: dict, consensus_type: str) -> Optional[str]:
    if json_obj[consensus_type] is None:
        return None
    return json_obj[consensus_type]["consensus"]


@dataclass
class TipRanksRow(DataRow):
    symbol: str
    analyst_consensus: str
    best_analyst_consensus: str

    @classmethod
    def table_name(cls):
        return 'tip_ranks'

    def __init__(self, json_obj: dict):
        self.symbol = json_obj["ticker"]
        self.analyst_consensus = get_val(json_obj, "analystConsensus")
        self.best_analyst_consensus = get_val(json_obj, "bestAnalystConsensus")
