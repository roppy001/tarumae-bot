import time
import json
import asyncio

import chromedriver_binary

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

import discord

import common

BLUE_TYPE_INDEX_STR = {
    common.SEARCH_SPEED_KEY : "2",
    common.SEARCH_STAMINA_KEY : "3",
    common.SEARCH_POWER_KEY : "4",
    common.SEARCH_GUTS_KEY : "5",
    common.SEARCH_WISDOM_KEY : "6",
}

async def scrape(config, search, driver, id_history_list):

    # ウマ娘DBを開く
    driver.get("https://uma.pure-db.com/#/search")

    blue_factor_list = [ (common.SEARCH_STAMINA_KEY, "3"),(common.SEARCH_SPEED_KEY, "2"),(common.SEARCH_WISDOM_KEY, "1"),(common.SEARCH_POWER_KEY, "3"),(common.SEARCH_GUTS_KEY, "2")]
    #blue_factor_list = [ (common.SEARCH_STAMINA_KEY, "3"),(common.SEARCH_SPEED_KEY, "2")]

    i = 1

    for blue_factor in blue_factor_list:
        blue_add_element = driver.find_element(By.CSS_SELECTOR,
            "#__BVID__34 > div > button")
        blue_add_element.click()

        blue_type_pulldown_element = driver.find_element(By.CSS_SELECTOR,
            "#__BVID__34 > div > div:nth-child("+str(i)+") > div:nth-of-type(1) > div > div > div.gb-field-select__field.js-tag-for-autofocus > i")
        blue_type_pulldown_element.click()
        await asyncio.sleep(1)

        blue_type_item_element = driver.find_element(By.CSS_SELECTOR,
            "#__BVID__34 > div > div:nth-child("+str(i)+") > div:nth-of-type(1) > div > div > div.gb-field-select__options > div:nth-child("+BLUE_TYPE_INDEX_STR[blue_factor[0]]+")")
        blue_type_item_element.click()

        Select(driver.find_element(By.CSS_SELECTOR,
            "#__BVID__34 > div > div:nth-child("+str(i)+") > div:nth-of-type(2) > select")).select_by_value(blue_factor[1])

        #Select(driver.find_element(By.CSS_SELECTOR,
        #    "#__BVID__34 > div > div:nth-child("+str(i)+") > div:nth-of-type(3) > select")).select_by_value("1")

        i = i + 1

    await asyncio.sleep(100)

    return []

async def send(config, channel, role_id, elm):
    message = f'<@&{role_id}> \n'

    # await channel.send(message)

    return
