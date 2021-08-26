from typing import List
from requests import get

def get_yahoo_data() -> List[YahooRow]:
    url = "https://query2.finance.yahoo.com/v7/finance/spark?symbols=TSLA,AAPL,VZ&range=1d&indicators=close&includeTimestamps=false&includePrePost=false&interval=1d&includeMeta=false"
    response = get(url)
    print(response.text)
    