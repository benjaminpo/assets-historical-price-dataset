import configparser
import logging

from src.module.common import save_spx_components_stock_to_file, save_nasdaq_components_stock_to_file, \
    fetch_spx_components_stock_price, fetch_nasdaq_components_stock_price, fetch_fx_components_stock_price


def main():
    config= configparser.ConfigParser()
    config.read('../config/local.ini')
    logging_main_path= config.get('LOGGING', 'MAIN_PATH')
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
    # fetch_nasdaq_components_stock_price('1d', 'max')
    # fetch_nasdaq_components_stock_price('1m', '7d')
    # fetch_spx_components_stock_price('1d', 'max')
    # fetch_spx_components_stock_price('1m', '7d')


main()
