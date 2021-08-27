import csv
from requests import post
from io import StringIO
from typing import List
from model import ZacksRow
from time import perf_counter


def get_zacks_data() -> List[ZacksRow]:
    print(" * * * * * * * * * * * * * * * * * * * *\nFetching Zacks data...")
    start = perf_counter()

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
    data = list(map(ZacksRow, reader[1:]))

    end = perf_counter()
    print("Success!")
    print("    Elapsed time: %f s" % (end - start))
    print("    Number of entries: %d" % (len(data)))
    return data
