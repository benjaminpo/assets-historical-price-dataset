from datetime import datetime
from dateutil.relativedelta import relativedelta

import configparser
import csv
import logging
import yfinance as yf


CONFIG = configparser.ConfigParser()
CONFIG.read('config/local.ini')
FILE_ENCODING = CONFIG.get('FILE', 'ENCODING')
LOGGING_MAIN_PATH = CONFIG.get('LOGGING', 'MAIN_PATH')
MAIN_GET_MAX_NUMBER_OF_YEAR_DATA = CONFIG.get('MAIN', 'GET_MAX_NUMBER_OF_YEAR_DATA')
SPX_CONSTITUENTS_PATH = CONFIG.get('SPX', 'CONSTITUENTS_PATH')
STOCK_US_PATH = CONFIG.get('STOCK_US', 'PATH')


def fetch_spx_components_stock_price():
    """Return nothing."""
    today = datetime.today().strftime('%Y-%m-%d')
    pass_years = datetime.now() - relativedelta(years=int(MAIN_GET_MAX_NUMBER_OF_YEAR_DATA))
    pass_years = pass_years.strftime('%Y-%m-%d')
    with open(SPX_CONSTITUENTS_PATH, newline='', encoding=FILE_ENCODING) as file:
        spx = csv.reader(file)
        next(spx)
        for spx_row in spx:
            stock = spx_row[0].replace(".", "-")
            data = yf.download(stock, pass_years, today)
            data.to_csv(STOCK_US_PATH + spx_row[0] + ".csv")
            print("Downloaded {} data".format(spx_row[0]))
            logging.info("Downloaded %s data", spx_row[0])


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M',
        handlers=[logging.FileHandler(LOGGING_MAIN_PATH, 'w', 'utf-8'), ]
    )
    fetch_spx_components_stock_price()


if __name__ == "__main__":
    main()
