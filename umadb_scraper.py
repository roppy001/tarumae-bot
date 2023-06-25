import sys
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
    search_wait = config[common.CONFIG_UMADB_SEARCH_WAIT_KEY]

    # ウマ娘DBを開く
    driver.get("https://uma.pure-db.com/#/search")

    blue_factor_list = []
    for k in [common.SEARCH_SPEED_KEY, common.SEARCH_STAMINA_KEY, common.SEARCH_POWER_KEY, common.SEARCH_GUTS_KEY, common.SEARCH_WISDOM_KEY]:
        tmp = search[k]
        if tmp!=0:
            blue_factor_list.append((k, tmp))

    common.scroll_element(driver, driver.find_element(By.CSS_SELECTOR,"#blue_factor"))

    i = 1
    for blue_factor in blue_factor_list:
        # 追加ボタン選択
        blue_add_element = driver.find_element(By.CSS_SELECTOR,
            "#blue_factor + button")
        blue_add_element.click()
        await asyncio.sleep(1)

        # 因子種類選択
        blue_type_pulldown_element = driver.find_element(By.CSS_SELECTOR,
            "#blue_factor > div:nth-child("+str(i)+") > div:nth-of-type(1) > div > div > div.gb-field-select__field.js-tag-for-autofocus > i")
        blue_type_pulldown_element.click()
        await asyncio.sleep(1)

        blue_type_item_element = driver.find_element(By.CSS_SELECTOR,
            "#blue_factor > div:nth-child("+str(i)+") > div:nth-of-type(1) > div > div > div.gb-field-select__options > div:nth-child("+BLUE_TYPE_INDEX_STR[blue_factor[0]]+")")
        blue_type_item_element.click()

        # 星数選択
        Select(driver.find_element(By.CSS_SELECTOR,
            "#blue_factor > div:nth-child("+str(i)+") > div:nth-of-type(2) > select")).select_by_value(str(blue_factor[1]))

        # 代表条件選択
        if(search[common.SEARCH_DAIHYO_KEY]):
            Select(driver.find_element(By.CSS_SELECTOR,
                "#blue_factor > div:nth-child("+str(i)+") > div:nth-of-type(3) > select")).select_by_value("1")

        i = i + 1

    red_factor_list = []
    for k in [common.SEARCH_TURF_KEY, common.SEARCH_DIRT_KEY, 
              common.SEARCH_SHORT_KEY, common.SEARCH_MILE_KEY, common.SEARCH_MIDDLE_KEY, common.SEARCH_LONG_KEY,
              common.SEARCH_NIGE_KEY, common.SEARCH_SENKOU_KEY, common.SEARCH_SASHI_KEY, common.SEARCH_OIKOMI_KEY]:
        tmp = search[k]
        if tmp!=0:
            red_factor_list.append((k, tmp))

    common.scroll_element(driver, driver.find_element(By.CSS_SELECTOR,"#red_factor"))

    i = 1
    for red_factor in red_factor_list:
        # 追加ボタン選択
        red_add_element = driver.find_element(By.CSS_SELECTOR,
            "#red_factor + button")
        red_add_element.click()
        await asyncio.sleep(1)

        # 因子種類選択
        red_type_pulldown_element = driver.find_element(By.CSS_SELECTOR,
            "#red_factor > div:nth-child("+str(i)+") > div:nth-of-type(1) > div > div > div.gb-field-select__field.js-tag-for-autofocus > i")
        red_type_pulldown_element.click()
        await asyncio.sleep(1)

        red_type_item_element = driver.find_element(By.CSS_SELECTOR,
            "#red_factor > div:nth-child("+str(i)+") > div:nth-of-type(1) > div > div > div.gb-field-select__options > div:nth-child("+RED_TYPE_INDEX_STR[red_factor[0]]+")")
        red_type_item_element.click()

        # 星数選択
        Select(driver.find_element(By.CSS_SELECTOR,
            "#red_factor > div:nth-child("+str(i)+") > div:nth-of-type(2) > select")).select_by_value(str(red_factor[1]))

        # 代表条件選択
        if(search[common.SEARCH_DAIHYO_KEY]):
            Select(driver.find_element(By.CSS_SELECTOR,
                "#red_factor > div:nth-child("+str(i)+") > div:nth-of-type(3) > select")).select_by_value("1")

        i = i + 1

    # 共通スキル選択
    i = 1
    for skill_factor in search[common.SEARCH_SKILL_KEY]:
        # 追加ボタン選択
        skill_add_element = driver.find_element(By.CSS_SELECTOR,
            "#common_factor_skill + button")
        skill_add_element.click()
        await asyncio.sleep(1)

        # 因子種類選択
        skill_type_pulldown_element = driver.find_element(By.CSS_SELECTOR,
            "#common_factor_skill > div:nth-child("+str(i)+") > div:nth-of-type(1) > div > div > div.gb-field-select__field.js-tag-for-autofocus > i")
        skill_type_pulldown_element.click()
        await asyncio.sleep(1)

        skill_type_item_elements = driver.find_elements(By.CSS_SELECTOR,
            "#common_factor_skill > div:nth-child("+str(i)+") > div:nth-of-type(1) > div > div > div.gb-field-select__options > div > span")

        for skill_type_item_element in skill_type_item_elements:
            if (skill_type_item_element.text == skill_factor[common.SEARCH_FACTOR_NAME_KEY]):
                skill_type_item_element.click()

        # 星数選択
        Select(driver.find_element(By.CSS_SELECTOR,
            "#common_factor_skill > div:nth-child("+str(i)+") > div:nth-of-type(2) > select")).select_by_value(str(skill_factor[common.SEARCH_FACTOR_STAR_KEY]))

        # 代表条件選択
        if(search[common.SEARCH_DAIHYO_KEY]):
            Select(driver.find_element(By.CSS_SELECTOR,
                "#common_factor_skill > div:nth-child("+str(i)+") > div:nth-of-type(3) > select")).select_by_value("1")

        i = i + 1

    # 検索ボタン押下
    search_element = driver.find_element(By.CSS_SELECTOR,
            "#app > div > div > div.btn-group > button.btn.btn-success")

    common.scroll_element(driver, search_element)
    search_element.click()

    # 検索結果出力待機
    try:
        for i in range(search_wait):
            await asyncio.sleep(1)
            driver.find_element(By.CSS_SELECTOR,"#app tbody > tr.b-table-busy-slot")
    except NoSuchElementException:
        pass
    await asyncio.sleep(1)

    result_list = []

    result_player_elements = driver.find_elements(By.CSS_SELECTOR, "#app tbody > tr")

    if len(result_player_elements) == 0:
        print("searching result is empty:" + json.dumps(search), file=sys.stderr)

    for result_player_element in result_player_elements:
        id = result_player_element.find_element(By.CSS_SELECTOR,"td > div.header > span").text

        # もし履歴にあるIDにヒットした場合はスキップする
        if id in id_history_list:
            continue

        elm = {}
        
        elm[common.RESULT_TYPE_KEY] = common.TYPE_UMADB

        elm[common.RESULT_ID_KEY] = id

        elm[common.RESULT_MAIN_IMG_KEY] = { common.IMG_URL_KEY : result_player_element.find_element(By.CSS_SELECTOR,"td > div.row > div.col-md-auto.col-2 > div:nth-child(1) > img").get_attribute("src") }

        elm[common.RESULT_FACTOR_LIST_KEY] = []

        for f in result_player_element.find_elements(By.CSS_SELECTOR, "td > div.row > div.col-10 span > span"):
            elm[common.RESULT_FACTOR_LIST_KEY].append({ common.FACTOR_NAME_KEY : f.text})

        result_list.append(elm)

    return result_list

async def send(config, channel, role_id, elm, test_mode):
    message = f'<@&{role_id}> 抽出元:ウマ娘DB \n'
    message += "トレーナーID: " + elm[common.RESULT_ID_KEY] + "\n"
    message += "因子: "
    for factor in elm[common.RESULT_FACTOR_LIST_KEY]:
        message += factor[common.FACTOR_NAME_KEY] + " "
    message += "\n"

    img = elm[common.RESULT_MAIN_IMG_KEY]

    if common.IMG_URL_KEY in img:
        message += img[common.IMG_URL_KEY] + "\n"

    if test_mode:
        print(message)
    else:
        await channel.send(message)

    return
