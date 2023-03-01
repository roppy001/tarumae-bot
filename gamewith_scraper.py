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

    blue2_select = Select(friends_list_sr.find_element(By.CSS_SELECTOR,
        "div.-r-common-modal__container ul > li:nth-of-type(5) > div > div:nth-of-type(4) select"))
    blue2_select.select_by_visible_text("☆3")
    time.sleep(1)


    red_element = friends_list_sr.find_element(By.CSS_SELECTOR,
        "div.-r-common-modal__container ul > li:nth-of-type(6)")
    common.scroll_element(driver, red_element)
    time.sleep(1)

    redb1_select = Select(friends_list_sr.find_element(By.CSS_SELECTOR,
        "div.-r-common-modal__container ul > li:nth-of-type(6) > div > div:nth-of-type(5) select"))
    redb1_select.select_by_visible_text("☆3")
    time.sleep(1)

    search_element = friends_list_sr.find_element(By.CSS_SELECTOR,
        "div.-r-common-modal__container .-r-umamusume-friends-button")
    common.scroll_element(driver, search_element)
    time.sleep(1)

    search_element.click()
    time.sleep(1)

    for i in range(max_next_count):
        result_player_elements = friends_list_sr.find_elements(By.CSS_SELECTOR, "div > div.-r-umamusume-friends-list__list-wrap > ul > li > div.-r-umamusume-friends-list-item__contents")
        time.sleep(1)

        for result_player_element in result_player_elements:
            player_id_element = result_player_element.find_element(By.CSS_SELECTOR, "div > p")

            player_factor_elements = result_player_element.find_elements(By.CSS_SELECTOR, "ul > li > span")

            str = player_id_element.text

            for player_factor_element in player_factor_elements:
                str += ", " + player_factor_element.text

            print(str)


        try:
            result_next = friends_list_sr.find_element(By.CSS_SELECTOR, "div > div.-r-umamusume-friends-list__list-wrap > button.-r-umamusume-friends-button")
            common.scroll_element(driver, result_next)
            common.scroll(driver, 0, -100)
            time.sleep(1)
            result_next.click()
            time.sleep(1)
        except NoSuchElementException:
            break

    return
    