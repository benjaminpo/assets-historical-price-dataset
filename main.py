import logging

from pack.util import save_spx_components_stock_to_file, save_nasdaq_components_stock_to_file, \
    fetch_fx_components_stock_price, load_config, fetch_nasdaq_components_stock_price, fetch_etf_components_stock_price, \
    fetch_spx_components_stock_price


def main():
    config = load_config()
    logging_main_path = config['LOGGING']['MAIN_PATH']
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M',
        handlers=[logging.FileHandler(logging_main_path, 'w', 'utf-8'), ]
    )
    save_spx_components_stock_to_file()
    save_nasdaq_components_stock_to_file()
    fetch_fx_components_stock_price()
    fetch_nasdaq_components_stock_price()
    fetch_spx_components_stock_price()
    fetch_etf_components_stock_price()


if __name__ == "__main__":
    main()
