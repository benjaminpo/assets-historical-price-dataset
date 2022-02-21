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


def load_config():
    return yaml.safe_load(open('./config/local.yml', 'r'))


def save_spx_components_stock_to_file():
    """Return nothing."""
    config = load_config()
    download_and_save(config['SPX']['CONSTITUENTS_URL'], config['SPX']['CONSTITUENTS_PATH'])


def save_nasdaq_components_stock_to_file():
    """Return nothing."""
    config = load_config()
    download_and_save(config['NASDAQ']['CONSTITUENTS_URL'], config['NASDAQ']['CONSTITUENTS_PATH'])


def fetch_assets(config, constituents_path, interval, period):
    ticker_list = []
    file_encoding = config['FILE']['ENCODING']
    data_path = config['DATA']['PATH']
    with open(constituents_path, newline='', encoding=file_encoding) as file:
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
        data.loc[(ticker,),].T.to_csv(data_path + interval + '/' + filename + '.csv', sep=',', encoding='utf-8')


def fetch_spx_components_stock_price(interval='1d', period='max'):
    """Return nothing."""
    config = load_config()
    constituents_path = config['SPX']['CONSTITUENTS_PATH']
    fetch_assets(config, constituents_path, interval, period)


def fetch_nasdaq_components_stock_price(interval='1d', period='max'):
    """Return nothing."""
    config = load_config()
    constituents_path = config['NASDAQ']['CONSTITUENTS_PATH']
    fetch_assets(config, constituents_path, interval, period)


def fetch_fx_components_stock_price(interval='1d', period='max'):
    """Return nothing."""
    config = load_config()
    constituents_path = config['FX']['CONSTITUENTS_PATH']
    fetch_assets(config, constituents_path, interval, period)


def fetch_etf_components_stock_price(interval='1d', period='max'):
    """Return nothing."""
    config = load_config()
    constituents_path = config['ETF']['CONSTITUENTS_PATH']
    fetch_assets(config, constituents_path, interval, period)
