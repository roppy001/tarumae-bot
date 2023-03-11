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
    common.SEARCH_WISDOM_KEY : "6"
}
RED_TYPE_INDEX_STR = {
    common.SEARCH_TURF_KEY : "2",
    common.SEARCH_DIRT_KEY : "3",
    common.SEARCH_SHORT_KEY : "4",
    common.SEARCH_MILE_KEY : "5",
    common.SEARCH_MIDDLE_KEY : "6",
    common.SEARCH_LONG_KEY : "7",
    common.SEARCH_NIGE_KEY : "8",
    common.SEARCH_SENKOU_KEY : "9",
    common.SEARCH_SASHI_KEY : "10",
    common.SEARCH_OIKOMI_KEY : "11",
}

async def scrape(config, search, driver, id_history_list):

    # ウマ娘DBを開く
    driver.get("https://uma.pure-db.com/#/search")

    blue_factor_list = []
    for k in [common.SEARCH_SPEED_KEY, common.SEARCH_STAMINA_KEY, common.SEARCH_POWER_KEY, common.SEARCH_GUTS_KEY, common.SEARCH_WISDOM_KEY]:
        tmp = search[k]
        if tmp!=0:
            blue_factor_list.append((k, tmp))

    common.scroll_element(driver, driver.find_element(By.CSS_SELECTOR,"#__BVID__34"))

    i = 1
    for blue_factor in blue_factor_list:
        blue_add_element = driver.find_element(By.CSS_SELECTOR,
            "#__BVID__34 > div > button")
        blue_add_element.click()
        await asyncio.sleep(1)

        blue_type_pulldown_element = driver.find_element(By.CSS_SELECTOR,
            "#__BVID__34 > div > div:nth-child("+str(i)+") > div:nth-of-type(1) > div > div > div.gb-field-select__field.js-tag-for-autofocus > i")
        blue_type_pulldown_element.click()
        await asyncio.sleep(1)

        blue_type_item_element = driver.find_element(By.CSS_SELECTOR,
            "#__BVID__34 > div > div:nth-child("+str(i)+") > div:nth-of-type(1) > div > div > div.gb-field-select__options > div:nth-child("+BLUE_TYPE_INDEX_STR[blue_factor[0]]+")")
        blue_type_item_element.click()

        Select(driver.find_element(By.CSS_SELECTOR,
            "#__BVID__34 > div > div:nth-child("+str(i)+") > div:nth-of-type(2) > select")).select_by_value(str(blue_factor[1]))

        #Select(driver.find_element(By.CSS_SELECTOR,
        #    "#__BVID__34 > div > div:nth-child("+str(i)+") > div:nth-of-type(3) > select")).select_by_value("1")

        i = i + 1

    red_factor_list = []
    for k in [common.SEARCH_TURF_KEY, common.SEARCH_DIRT_KEY, 
              common.SEARCH_SHORT_KEY, common.SEARCH_MILE_KEY, common.SEARCH_MIDDLE_KEY, common.SEARCH_LONG_KEY,
              common.SEARCH_NIGE_KEY, common.SEARCH_SENKOU_KEY, common.SEARCH_SASHI_KEY, common.SEARCH_OIKOMI_KEY]:
        tmp = search[k]
        if tmp!=0:
            red_factor_list.append((k, tmp))

    common.scroll_element(driver, driver.find_element(By.CSS_SELECTOR,"#__BVID__35"))

    i = 1
    for red_factor in red_factor_list:
        red_add_element = driver.find_element(By.CSS_SELECTOR,
            "#__BVID__35 > div > button")
        red_add_element.click()
        await asyncio.sleep(1)

        red_type_pulldown_element = driver.find_element(By.CSS_SELECTOR,
            "#__BVID__35 > div > div:nth-child("+str(i)+") > div:nth-of-type(1) > div > div > div.gb-field-select__field.js-tag-for-autofocus > i")
        red_type_pulldown_element.click()
        await asyncio.sleep(1)

        red_type_item_element = driver.find_element(By.CSS_SELECTOR,
            "#__BVID__35 > div > div:nth-child("+str(i)+") > div:nth-of-type(1) > div > div > div.gb-field-select__options > div:nth-child("+RED_TYPE_INDEX_STR[red_factor[0]]+")")
        red_type_item_element.click()

        Select(driver.find_element(By.CSS_SELECTOR,
            "#__BVID__35 > div > div:nth-child("+str(i)+") > div:nth-of-type(2) > select")).select_by_value(str(red_factor[1]))

        #Select(driver.find_element(By.CSS_SELECTOR,
        #    "#__BVID__35 > div > div:nth-child("+str(i)+") > div:nth-of-type(3) > select")).select_by_value("1")

        i = i + 1

    search_element = driver.find_element(By.CSS_SELECTOR,
            "#app > div > div > div.btn-group > button.btn.btn-primary")

    common.scroll_element(driver, search_element)
    search_element.click()

    await asyncio.sleep(100)

    return []

async def send(config, channel, role_id, elm):
    message = f'<@&{role_id}> \n'

    # await channel.send(message)

    return
