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
NASDAQ_CONSTITUENTS_URL = CONFIG.get('NASDAQ', 'CONSTITUENTS_URL')
SPX_CONSTITUENTS_PATH = CONFIG.get('SPX', 'CONSTITUENTS_PATH')
SPX_CONSTITUENTS_URL = CONFIG.get('SPX', 'CONSTITUENTS_URL')
DATA_PATH = CONFIG.get('DATA', 'PATH')


def download_and_save(url, path):
    """Return nothing."""
    req = requests.get(url)
    url_content = req.content
    file = open(path, 'wb')
    file.write(url_content)
    file.close()


def save_spx_components_stock_to_file():
    """Return nothing."""
    download_and_save(SPX_CONSTITUENTS_URL, SPX_CONSTITUENTS_PATH)


def save_nasdaq_components_stock_to_file():
    """Return nothing."""
    download_and_save(NASDAQ_CONSTITUENTS_URL, NASDAQ_CONSTITUENTS_PATH)


def fetch_spx_components_stock_price(interval='1d', period='max'):
    """Return nothing."""
    ticker_list = []
    with open(SPX_CONSTITUENTS_PATH, newline='', encoding=FILE_ENCODING) as file:
        my_list = csv.reader(file)
        next(my_list)
        for ticker in my_list:
            ticker_list.append(ticker[0].replace(".", "-"))
    data = yf.download(
        tickers=ticker_list,
        period=period,
        interval=interval,
        group_by='ticker',
        threads=True
    )
    data = data.T
    data = data.sort_index()
    for ticker in ticker_list:
        filename = ticker.replace("=", "-").replace(".", "-")
        data.loc[(ticker,), ].T.to_csv(DATA_PATH + interval + '/' + filename + '.csv', sep=',', encoding='utf-8')


def fetch_nasdaq_components_stock_price(interval='1d', period='max'):
    """Return nothing."""
    ticker_list = []
    with open(NASDAQ_CONSTITUENTS_PATH, newline='', encoding=FILE_ENCODING) as file:
        my_list = csv.reader(file)
        next(my_list)
        for ticker in my_list:
            ticker_list.append(ticker[0].replace(".", "-"))
    data = yf.download(
        tickers=ticker_list,
        period=period,
        interval=interval,
        group_by='ticker',
        threads=True
    )
    data = data.T
    data = data.sort_index()
    for ticker in ticker_list:
        filename = ticker.replace("=", "-").replace(".", "-")
        data.loc[(ticker,), ].T.to_csv(DATA_PATH + interval + '/' + filename + '.csv', sep=',', encoding='utf-8')


def fetch_fx_components_stock_price(interval='1d', period='max'):
    """Return nothing."""
    ticker_list = []
    with open(FX_CONSTITUENTS_PATH, newline='', encoding=FILE_ENCODING) as file:
        my_list = csv.reader(file)
        next(my_list)
        for ticker in my_list:
            ticker_list.append(ticker[0].replace(".", "-"))
    data = yf.download(
        tickers=ticker_list,
        period=period,
        interval=interval,
        group_by='ticker',
        threads=True
    )
    data = data.T
    data = data.sort_index()
    for ticker in ticker_list:
        filename = ticker.replace("=", "-").replace(".", "-")
        data.loc[(ticker,), ].T.to_csv(DATA_PATH + interval + '/' + filename + '.csv', sep=',', encoding='utf-8')


def main():
    logging_main_path = CONFIG.get('LOGGING', 'MAIN_PATH')
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M',
        handlers=[logging.FileHandler(logging_main_path, 'w', 'utf-8'), ]
    )
    save_spx_components_stock_to_file()
    save_nasdaq_components_stock_to_file()
    fetch_fx_components_stock_price('1d', 'max')
    fetch_fx_components_stock_price('1m', '7d')
    fetch_nasdaq_components_stock_price('1d', 'max')
    fetch_nasdaq_components_stock_price('1m', '7d')
    fetch_spx_components_stock_price('1d', 'max')
    fetch_spx_components_stock_price('1m', '7d')


if __name__ == "__main__":
    main()
