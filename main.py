import configparser
import csv
import logging

import requests
import yfinance as yf

CONFIG = configparser.ConfigParser()
CONFIG.read('config/local.ini')

FILE_ENCODING = CONFIG.get('FILE', 'ENCODING')
FX_CONSTITUENTS_PATH = CONFIG.get('FX', 'CONSTITUENTS_PATH')
NASDAQ_CONSTITUENTS_PATH = CONFIG.get('NASDAQ', 'CONSTITUENTS_PATH')
NASDAQ_CONSTITUENTS_PATH = CONFIG.get('NASDAQ', 'CONSTITUENTS_PATH')
NASDAQ_CONSTITUENTS_URL = CONFIG.get('NASDAQ', 'CONSTITUENTS_URL')
SPX_CONSTITUENTS_PATH = CONFIG.get('SPX', 'CONSTITUENTS_PATH')
SPX_CONSTITUENTS_PATH = CONFIG.get('SPX', 'CONSTITUENTS_PATH')
SPX_CONSTITUENTS_URL = CONFIG.get('SPX', 'CONSTITUENTS_URL')
DATA_PATH = CONFIG.get('DATA', 'PATH')

def save_spx_components_stock_to_csv():
    """Return nothing."""
    req = requests.get(SPX_CONSTITUENTS_URL)
    url_content = req.content
    csv_file = open(SPX_CONSTITUENTS_PATH, 'wb')
    csv_file.write(url_content)
    csv_file.close()


def save_nasdaq_components_stock_to_csv():
    """Return nothing."""
    req = requests.get(NASDAQ_CONSTITUENTS_URL)
    url_content = req.content
    csv_file = open(NASDAQ_CONSTITUENTS_PATH, 'wb')
    csv_file.write(url_content)
    csv_file.close()


def fetch_spx_components_stock_price(interval = '1d', period = 'max'):
    """Return nothing."""
    ticker_list = []
    with open(SPX_CONSTITUENTS_PATH, newline='', encoding=FILE_ENCODING) as file:
        list = csv.reader(file)
        next(list)
        for ticker in list:
            ticker_list.append(ticker[0].replace(".", "-"))
    data = yf.download(
        tickers = ticker_list,
        period = period,
        interval = interval,
        group_by = 'ticker',
        threads = True
    )
    data = data.T
    data = data.sort_index()
    for ticker in ticker_list:
        filename = ticker.replace("=", "-").replace(".", "-")
        data.loc[(ticker,),].T.to_csv(DATA_PATH + interval + '/' + filename + '.csv', sep=',', encoding='utf-8')


def fetch_nasdaq_components_stock_price(interval = '1d', period = 'max'):
    """Return nothing."""
    ticker_list = []
    with open(NASDAQ_CONSTITUENTS_PATH, newline='', encoding=FILE_ENCODING) as file:
        list = csv.reader(file)
        next(list)
        for ticker in list:
            ticker_list.append(ticker[0].replace(".", "-"))
    data = yf.download(
        tickers = ticker_list,
        period = period,
        interval = interval,
        group_by = 'ticker',
        threads = True
    )
    data = data.T
    data = data.sort_index()
    for ticker in ticker_list:
        filename = ticker.replace("=", "-").replace(".", "-")
        data.loc[(ticker,),].T.to_csv(DATA_PATH + interval + '/' + filename + '.csv', sep=',', encoding='utf-8')


def fetch_fx_components_stock_price(interval = '1d', period = 'max'):
    """Return nothing."""
    ticker_list = []
    with open(FX_CONSTITUENTS_PATH, newline='', encoding=FILE_ENCODING) as file:
        list = csv.reader(file)
        next(list)
        for ticker in list:
            ticker_list.append(ticker[0].replace(".", "-"))
    data = yf.download(
        tickers = ticker_list,
        period = period,
        interval = interval,
        group_by = 'ticker',
        threads = True
    )
    data = data.T
    data = data.sort_index()
    for ticker in ticker_list:
        filename = ticker.replace("=", "-").replace(".", "-")
        data.loc[(ticker,),].T.to_csv(DATA_PATH + interval + '/' + filename + '.csv', sep=',', encoding='utf-8')


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
    fetch_fx_components_stock_price('1d', 'max')
    fetch_fx_components_stock_price('1m', '7d')
    fetch_nasdaq_components_stock_price('1d')
    fetch_nasdaq_components_stock_price('1m', '7d')
    fetch_spx_components_stock_price('1d')
    fetch_spx_components_stock_price('1m', '7d')

if __name__ == "__main__":
    main()
