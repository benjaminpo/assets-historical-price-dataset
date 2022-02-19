import csv

import requests
import yaml
import yfinance as yf


def download_and_save(url, path):
    """Return nothing."""
    req = requests.get(url)
    url_content = req.content
    file = open(path, 'wb')
    file.write(url_content)
    file.close()


def save_spx_components_stock_to_file():
    """Return nothing."""
    config = yaml.safe_load(open('../config/local.yml', 'r'))
    download_and_save(config['SPX']['CONSTITUENTS_URL'], config['SPX']['CONSTITUENTS_PATH'])


def save_nasdaq_components_stock_to_file():
    """Return nothing."""
    config = yaml.safe_load(open('../config/local.yml', 'r'))
    download_and_save(config['NASDAQ']['CONSTITUENTS_URL'], config['NASDAQ']['CONSTITUENTS_PATH'])


def fetch_spx_components_stock_price(interval='1d', period='max'):
    """Return nothing."""
    ticker_list = []
    config = yaml.safe_load(open('../config/local.yml', 'r'))
    file_encoding = config['FILE']['ENCODING']
    spx_constituents_path = config['SPX']['CONSTITUENTS_PATH']
    data_path = config['DATA']['PATH']
    with open(spx_constituents_path, newline='', encoding=file_encoding) as file:
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
        data.loc[(ticker,), ].T.to_csv(data_path + interval + '/' + filename + '.csv', sep=',', encoding='utf-8')


def fetch_nasdaq_components_stock_price(interval='1d', period='max'):
    """Return nothing."""
    ticker_list = []
    config = yaml.safe_load(open('../config/local.yml', 'r'))
    file_encoding = config['FILE']['ENCODING']
    nasdaq_constituents_path = config['NASDAQ']['CONSTITUENTS_PATH']
    data_path = config['DATA']['PATH']
    with open(nasdaq_constituents_path, newline='', encoding=file_encoding) as file:
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
        data.loc[(ticker,), ].T.to_csv(data_path + interval + '/' + filename + '.csv', sep=',', encoding='utf-8')


def fetch_fx_components_stock_price(interval='1d', period='max'):
    """Return nothing."""
    ticker_list = []
    config = yaml.safe_load(open('../config/local.yml', 'r'))
    file_encoding = config['FILE']['ENCODING']
    fx_constituents_path = config['FX']['CONSTITUENTS_PATH']
    data_path = config['DATA']['PATH']
    with open(fx_constituents_path, newline='', encoding=file_encoding) as file:
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
        data.loc[(ticker,), ].T.to_csv(data_path + interval + '/' + filename + '.csv', sep=',', encoding='utf-8')
