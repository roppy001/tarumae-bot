import time
import json

import chromedriver_binary

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

import common

FACTOR_STRINGS = ["-","☆1","☆2","☆3","☆4","☆5","☆6","☆7","☆8","☆9"]

def scrape(gw_config, search, driver):
    max_next_count = gw_config[common.CONFIG_GW_MAX_NEXT_COUNT_KEY]

    # フレンド募集掲示板を開く
    driver.get("https://gamewith.jp/uma-musume/article/show/260740")
    time.sleep(1)

    # 詳細条件を指定して検索の画面に遷移してクリック
    friends_list = driver.find_element(By.CSS_SELECTOR, "gds-umamusume-friends-list")
    common.scroll_element(driver, friends_list)
    friends_list_sr = friends_list.shadow_root
    friends_list_sr.find_element(By.CSS_SELECTOR, ".-r-umamusume-friends-list__search-wrap button").click()
    time.sleep(1)

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
    time.sleep(1)

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
    time.sleep(1)

    # 赤因子選択位置にスクロール
    red_element = friends_list_sr.find_element(By.CSS_SELECTOR,
        "div.-r-common-modal__container ul > li:nth-of-type(6)")
    common.scroll_element(driver, red_element)
    time.sleep(1)

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
    time.sleep(1)

    search_element = friends_list_sr.find_element(By.CSS_SELECTOR,
        "div.-r-common-modal__container .-r-umamusume-friends-button")
    common.scroll_element(driver, search_element)
    time.sleep(1)

    search_element.click()
    time.sleep(1)

    for i in range(max_next_count):
        if i!=0:
            try:
                result_next = friends_list_sr.find_element(By.CSS_SELECTOR, "div > div.-r-umamusume-friends-list__list-wrap > button.-r-umamusume-friends-button")
                common.scroll_element(driver, result_next)
                common.scroll(driver, 0, -100)
                time.sleep(1)
                result_next.click()
                time.sleep(1)
            except NoSuchElementException:
                break

        result_player_elements = friends_list_sr.find_elements(By.CSS_SELECTOR, "div > div.-r-umamusume-friends-list__list-wrap > ul > li > div.-r-umamusume-friends-list-item__contents")
        time.sleep(1)

        for result_player_element in result_player_elements:
            player_id_element = result_player_element.find_element(By.CSS_SELECTOR, "div > p")

            player_factor_elements = result_player_element.find_elements(By.CSS_SELECTOR, "ul > li > span")

            str = player_id_element.text

            for player_factor_element in player_factor_elements:
                str += ", " + player_factor_element.text

            print(str)



    return
    