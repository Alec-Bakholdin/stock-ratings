import csv
from requests import post
from io import StringIO
from typing import List
from model import ZacksRow



def get_zacks_data() -> List[ZacksRow]:
    url = "https://www.zacks.com/portfolios/tools/ajxExportExel.php"
    payload = 'export_data_init_tab=2282242_update_zYjM1ADO0kjN&export_data_rest_tab=&XLS_FILE=Oleg%2BHoldings%2B-%2Bupdate'
    headers = {
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://www.zacks.com',
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'PostmanRuntime/7.28.3',
        'Connection': 'keep-alive'
    }
    response = post(url, headers=headers, data=payload)
    if response.status_code != 200:
        print("Error", response.status_code, response.text)

    reader = list(csv.reader(StringIO(str(response.text)), delimiter=','))
    ZacksRow.validate_headers((reader[0]))
    return list(map(ZacksRow, reader[1:]))
