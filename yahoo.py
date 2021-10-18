from typing import List
from requests import get
from model import YahooRow, Company
from lxml import etree
from time import sleep


def get_yahoo_data(companies: List[Company]) -> List[YahooRow]:
    yahoo_rows = []
    for company in companies:
        row = get_yahoo_stock_data(company.symbol)
        if row is not None:
            yahoo_rows.append(row)
        sleep(0.1)
    return yahoo_rows


def get_yahoo_stock_data(symbol: str) -> YahooRow:
    url = f"https://finance.yahoo.com/quote/{symbol}"
    response = get(url, {'User-Agent': 'PostmanRuntime/7.28.4', 'Cookie': 'B=21ka2flgmgph7&b=3&s=d4'})
    yahoo_row = YahooRow(symbol)
    if response.status_code != 200:
        return yahoo_row

    tree = etree.HTML(response.text)
    assign_performance_outlook(tree, response, yahoo_row)
    assign_fair_value(tree, yahoo_row)

    return yahoo_row


def assign_performance_outlook(tree, response, yahoo_row):
    xpath = "//h5[text()[contains(., 'Performance Outlook')]]/following-sibling::ul/li/a/div[1]/div[2]/svg"
    performance_outlooks = tree.xpath(xpath)
    performance_outlook_classes = list(map(lambda x: x.attrib['class'], performance_outlooks))
    yahoo_row.short_term = get_single_performance_outlook(performance_outlook_classes, 0)
    yahoo_row.mid_term = get_single_performance_outlook(performance_outlook_classes, 1)
    yahoo_row.long_term = get_single_performance_outlook(performance_outlook_classes, 2)


def get_single_performance_outlook(performance_outlook_classes: List[str], index: int) -> str:
    if len(performance_outlook_classes) == 0:
        return "Neutral"
    if performance_outlook_classes[index].find('RotateZ(180deg)') >= 0:
        return "Bearish"
    return "Bullish"


def assign_fair_value(tree, yahoo_row):
    est_ret_xpath = '//div[@id="fr-val-mod"]/div[3]/div[1]'
    est_ret_elements = tree.xpath(est_ret_xpath)
    est_ret_str = str(est_ret_elements[0].text) if len(est_ret_elements) > 0 else ''
    yahoo_row.estimated_return = float(est_ret_str[0:est_ret_str.index('%')]) if est_ret_str.find('%') > 0 else None
    if yahoo_row.estimated_return == float('Inf'):
        yahoo_row.estimated_return = 1000
    elif yahoo_row.estimated_return == float('-Inf'):
        yahoo_row.estimated_return = -1000
    fair_val_xpath = '//div[@id="fr-val-mod"]/div[2]/div[2]'
    fair_val_elements = tree.xpath(fair_val_xpath)
    yahoo_row.fair_value = str(fair_val_elements[0].text) if len(fair_val_elements) > 0 else None
