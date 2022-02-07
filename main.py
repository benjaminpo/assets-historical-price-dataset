from datetime import datetime
from dateutil.relativedelta import relativedelta

import configparser
import csv
import logging
import yfinance as yf
import requests

CONFIG = configparser.ConfigParser()
CONFIG.read('config/local.ini')


def save_spx_components_stock_to_csv():
    """Return nothing."""
    CONSTITUENTS_URL = CONFIG.get('SPX', 'CONSTITUENTS_URL')
    CONSTITUENTS_PATH = CONFIG.get('SPX', 'CONSTITUENTS_PATH')

    req = requests.get(CONSTITUENTS_URL)
    url_content = req.content
    csv_file = open(CONSTITUENTS_PATH, 'wb')
    csv_file.write(url_content)
    csv_file.close()


def save_nasdaq_components_stock_to_csv():
    """Return nothing."""
    CONSTITUENTS_URL = CONFIG.get('NASDAQ', 'CONSTITUENTS_URL')
    CONSTITUENTS_PATH = CONFIG.get('NASDAQ', 'CONSTITUENTS_PATH')

    req = requests.get(CONSTITUENTS_URL)
    url_content = req.content
    csv_file = open(CONSTITUENTS_PATH, 'wb')
    csv_file.write(url_content)
    csv_file.close()


def fetch_spx_components_stock_price():
    """Return nothing."""

    FILE_ENCODING = CONFIG.get('FILE', 'ENCODING')
    MAIN_GET_MAX_NUMBER_OF_YEAR_DATA = CONFIG.get('MAIN', 'GET_MAX_NUMBER_OF_YEAR_DATA')
    CONSTITUENTS_PATH = CONFIG.get('SPX', 'CONSTITUENTS_PATH')
    STOCK_US_PATH = CONFIG.get('STOCK_US', 'PATH')

    pass_years = datetime.now() - relativedelta(years=int(MAIN_GET_MAX_NUMBER_OF_YEAR_DATA))
    pass_years = pass_years.strftime('%Y-%m-%d')
    ticker_list = []
    with open(CONSTITUENTS_PATH, newline='', encoding=FILE_ENCODING) as file:
        list = csv.reader(file)
        next(list)
        for ticker in list:
            ticker_list.append(ticker[0].replace(".", "-"))
    data = yf.download(
        tickers = ticker_list,
        period = MAIN_GET_MAX_NUMBER_OF_YEAR_DATA + 'y',
        interval = '1d',
        group_by = 'ticker',
        auto_adjust = False,
        prepost = False,
        threads = True,
        proxy = None
    )
    data = data.T
    data = data.sort_index()

    for ticker in ticker_list:
        data.loc[(ticker,),].T.to_csv(STOCK_US_PATH + ticker + '.csv', sep=',', encoding='utf-8')


def fetch_nasdaq_components_stock_price():
    """Return nothing."""

    FILE_ENCODING = CONFIG.get('FILE', 'ENCODING')
    MAIN_GET_MAX_NUMBER_OF_YEAR_DATA = CONFIG.get('MAIN', 'GET_MAX_NUMBER_OF_YEAR_DATA')
    CONSTITUENTS_PATH = CONFIG.get('NASDAQ', 'CONSTITUENTS_PATH')
    STOCK_US_PATH = CONFIG.get('STOCK_US', 'PATH')

    pass_years = datetime.now() - relativedelta(years=int(MAIN_GET_MAX_NUMBER_OF_YEAR_DATA))
    pass_years = pass_years.strftime('%Y-%m-%d')
    ticker_list = []
    with open(CONSTITUENTS_PATH, newline='', encoding=FILE_ENCODING) as file:
        list = csv.reader(file)
        next(list)
        for ticker in list:
            ticker_list.append(ticker[0].replace(".", "-"))
    data = yf.download(
        tickers = ticker_list,
        period = MAIN_GET_MAX_NUMBER_OF_YEAR_DATA + 'y',
        interval = '1d',
        group_by = 'ticker',
        auto_adjust = False,
        prepost = False,
        threads = True,
        proxy = None
    )
    data = data.T
    data = data.sort_index()

    for ticker in ticker_list:
        data.loc[(ticker,),].T.to_csv(STOCK_US_PATH + ticker + '.csv', sep=',', encoding='utf-8')


def main():
    LOGGING_MAIN_PATH = CONFIG.get('LOGGING', 'MAIN_PATH')
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M',
        handlers=[logging.FileHandler(LOGGING_MAIN_PATH, 'w', 'utf-8'), ]
    )
    save_spx_components_stock_to_csv()
    save_nasdaq_components_stock_to_csv()
    fetch_spx_components_stock_price()
    fetch_nasdaq_components_stock_price()


if __name__ == "__main__":
    main()
