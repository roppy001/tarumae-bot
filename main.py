import time
import json

import chromedriver_binary

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import common
import gamewith_scraper


def load_config():
    fp = open(common.CONFIG_PATH, 'r', encoding="utf-8")

    data =json.load(fp)

    fp.close()

    return data


def main():
    config = load_config()

    gw_config = config[common.CONFIG_GW_KEY]

    search_list = config[common.CONFIG_SEARCH_LIST_KEY]

    driver = webdriver.Chrome()

    for search in search_list:
        gamewith_scraper.scrape(gw_config, search, driver)

    driver.quit()

main()