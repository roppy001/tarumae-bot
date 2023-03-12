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

FACTOR_STRINGS = ["-","☆1","☆2","☆3","☆4","☆5","☆6","☆7","☆8","☆9"]

async def scrape(config, search, driver, id_history_list):
    max_next_count = config[common.CONFIG_GW_MAX_NEXT_COUNT_KEY]

    # フレンド募集掲示板を開く
    driver.get("https://gamewith.jp/uma-musume/article/show/260740")

    # 詳細条件を指定して検索の画面に遷移してクリック
    friends_list = driver.find_element(By.CSS_SELECTOR, "gds-umamusume-friends-list")
    common.scroll_element(driver, friends_list)
    await asyncio.sleep(1)
    friends_list_sr = friends_list.shadow_root
    friends_list_sr.find_element(By.CSS_SELECTOR, ".-r-umamusume-friends-list__search-wrap button").click()
    await asyncio.sleep(1)

    # 育成ウマ娘指定
    tmp = search[common.SEARCH_NAME_KEY]
    if tmp!="":
        name_element = friends_list_sr.find_element(By.CSS_SELECTOR,
            "div.-r-common-modal__container ul > li:nth-of-type(3)")
        Select(name_element.find_element(By.CSS_SELECTOR,
            "div > select")).select_by_visible_text(tmp)
    
    # 代表フラグ
    tmp = search[common.SEARCH_DAIHYO_KEY]
    if tmp:
        daihyo_element = friends_list_sr.find_element(By.CSS_SELECTOR,
            "div.-r-common-modal__container ul > li:nth-of-type(4)")
        daihyo_element.find_element(By.CSS_SELECTOR,
            "#mainOnly").click()
        
    # 青因子選択位置にスクロール
    blue_element = friends_list_sr.find_element(By.CSS_SELECTOR,
        "div.-r-common-modal__container ul > li:nth-of-type(5)")
    common.scroll_element(driver, blue_element)
    await asyncio.sleep(1)

    # スピード因子
    tmp = search[common.SEARCH_SPEED_KEY]
    if tmp!=0:
        Select(blue_element.find_element(By.CSS_SELECTOR,"div > div:nth-of-type(1) > div > select")).select_by_visible_text(FACTOR_STRINGS[tmp])

    # スタミナ因子
    tmp = search[common.SEARCH_STAMINA_KEY]
    if tmp!=0:
        Select(blue_element.find_element(By.CSS_SELECTOR,"div > div:nth-of-type(2) > div > select")).select_by_visible_text(FACTOR_STRINGS[tmp])

    # パワー因子
    tmp = search[common.SEARCH_POWER_KEY]
    if tmp!=0:
        Select(blue_element.find_element(By.CSS_SELECTOR,"div > div:nth-of-type(3) > div > select")).select_by_visible_text(FACTOR_STRINGS[tmp])
    # 根性因子
    tmp = search[common.SEARCH_GUTS_KEY]
    if tmp!=0:
        Select(blue_element.find_element(By.CSS_SELECTOR,"div > div:nth-of-type(4) > div > select")).select_by_visible_text(FACTOR_STRINGS[tmp])

    # 賢さ因子
    tmp = search[common.SEARCH_WISDOM_KEY]
    if tmp!=0:
        Select(blue_element.find_element(By.CSS_SELECTOR,"div > div:nth-of-type(5) > div > select")).select_by_visible_text(FACTOR_STRINGS[tmp])

    # 赤因子選択位置にスクロール
    red_element = friends_list_sr.find_element(By.CSS_SELECTOR,
        "div.-r-common-modal__container ul > li:nth-of-type(6)")
    common.scroll_element(driver, red_element)
    await asyncio.sleep(1)

    # 芝因子
    tmp = search[common.SEARCH_TURF_KEY]
    if tmp!=0:
        Select(red_element.find_element(By.CSS_SELECTOR,"div > div:nth-of-type(1) > div > select")).select_by_visible_text(FACTOR_STRINGS[tmp])

    # ダート因子
    tmp = search[common.SEARCH_DIRT_KEY]
    if tmp!=0:
        Select(red_element.find_element(By.CSS_SELECTOR,"div > div:nth-of-type(2) > div > select")).select_by_visible_text(FACTOR_STRINGS[tmp])

    # 短距離因子
    tmp = search[common.SEARCH_SHORT_KEY]
    if tmp!=0:
        Select(red_element.find_element(By.CSS_SELECTOR,"div > div:nth-of-type(3) > div > select")).select_by_visible_text(FACTOR_STRINGS[tmp])

    # マイル因子
    tmp = search[common.SEARCH_MILE_KEY]
    if tmp!=0:
        Select(red_element.find_element(By.CSS_SELECTOR,"div > div:nth-of-type(4) > div > select")).select_by_visible_text(FACTOR_STRINGS[tmp])

    # 中距離因子
    tmp = search[common.SEARCH_MIDDLE_KEY]
    if tmp!=0:
        Select(red_element.find_element(By.CSS_SELECTOR,"div > div:nth-of-type(5) > div > select")).select_by_visible_text(FACTOR_STRINGS[tmp])

    # 長距離因子
    tmp = search[common.SEARCH_LONG_KEY]
    if tmp!=0:
        Select(red_element.find_element(By.CSS_SELECTOR,"div > div:nth-of-type(6) > div > select")).select_by_visible_text(FACTOR_STRINGS[tmp])

    # 逃げ因子
    tmp = search[common.SEARCH_NIGE_KEY]
    if tmp!=0:
        Select(red_element.find_element(By.CSS_SELECTOR,"div > div:nth-of-type(7) > div > select")).select_by_visible_text(FACTOR_STRINGS[tmp])

    # 先行因子
    tmp = search[common.SEARCH_SENKOU_KEY]
    if tmp!=0:
        Select(red_element.find_element(By.CSS_SELECTOR,"div > div:nth-of-type(8) > div > select")).select_by_visible_text(FACTOR_STRINGS[tmp])

    # 差し因子
    tmp = search[common.SEARCH_SASHI_KEY]
    if tmp!=0:
        Select(red_element.find_element(By.CSS_SELECTOR,"div > div:nth-of-type(9) > div > select")).select_by_visible_text(FACTOR_STRINGS[tmp])

    # 追込因子
    tmp = search[common.SEARCH_OIKOMI_KEY]
    if tmp!=0:
        Select(red_element.find_element(By.CSS_SELECTOR,"div > div:nth-of-type(10) > div > select")).select_by_visible_text(FACTOR_STRINGS[tmp])

    search_element = friends_list_sr.find_element(By.CSS_SELECTOR,
        "div.-r-common-modal__container .-r-umamusume-friends-button")
    common.scroll_element(driver, search_element)
    await asyncio.sleep(1)

    search_element.click()
    await asyncio.sleep(1)

    result = []

    for next_count in range(max_next_count):
        if next_count!=0:
            try:
                result_next = friends_list_sr.find_element(By.CSS_SELECTOR, "div > div.-r-umamusume-friends-list__list-wrap > button.-r-umamusume-friends-button")
                common.scroll_element(driver, result_next)
                common.scroll(driver, 0, -100)
                await asyncio.sleep(1)
                result_next.click()
                await asyncio.sleep(1)
            except NoSuchElementException:
                break

        result_list = []

        result_player_elements = friends_list_sr.find_elements(By.CSS_SELECTOR, "div > div.-r-umamusume-friends-list__list-wrap > ul > li")
        time.sleep(1)

        for result_player_element in result_player_elements:

            player_id_element = result_player_element.find_element(By.CSS_SELECTOR, "div.-r-umamusume-friends-list-item__contents div > p")

            player_factor_elements = result_player_element.find_elements(By.CSS_SELECTOR, "div.-r-umamusume-friends-list-item__contents ul > li > span")

            # 代表ウマ娘情報を取れた場合はurl情報を、取れなかった場合は空の連想配列を設定
            main_img={}
            try:
                player_icon_element = result_player_element.find_element(By.CSS_SELECTOR, "div.-r-umamusume-friends-list-item__mainUmaMusume-wrap > img")
                img_url = player_icon_element.get_attribute("src")
                main_img[common.IMG_URL_KEY] = img_url
            except NoSuchElementException:
                pass

            id = player_id_element.text

            # もし履歴にあるIDにヒットした場合は検索を終了する
            if id in id_history_list:
                return result_list

            elm = {}
            
            elm[common.RESULT_TYPE_KEY] = common.TYPE_GW

            elm[common.RESULT_ID_KEY] = id

            elm[common.RESULT_MAIN_IMG_KEY] = main_img

            elm[common.RESULT_FACTOR_LIST_KEY] = []

            for player_factor_element in player_factor_elements:
                f = {}
                f[common.FACTOR_NAME_KEY] = player_factor_element.text
                elm[common.RESULT_FACTOR_LIST_KEY].append(f)

            result_list.append(elm)

    return result_list

async def send(config, channel, role_id, elm):
    message = f'<@&{role_id}> 抽出元:gamewith \n'
    message += "トレーナーID: " + elm[common.RESULT_ID_KEY] + "\n"
    message += "因子: "
    for factor in elm[common.RESULT_FACTOR_LIST_KEY]:
        message += factor[common.FACTOR_NAME_KEY] + " "
    message += "\n"

    img = elm[common.RESULT_MAIN_IMG_KEY]

    if common.IMG_URL_KEY in img:
        message += img[common.IMG_URL_KEY] + "\n"

    await channel.send(message)

    return
