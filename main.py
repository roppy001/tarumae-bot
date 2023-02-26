import time
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome()
driver.get("https://gamewith.jp/uma-musume/article/show/260740")
time.sleep(1)
friends_list = driver.find_element(By.CSS_SELECTOR, "gds-umamusume-friends-list")
driver.execute_script("arguments[0].scrollIntoView(true);", friends_list)
friends_list_sr = friends_list.shadow_root
friends_list_sr.find_element(By.CSS_SELECTOR, ".-r-umamusume-friends-list__search-wrap button").click()
time.sleep(1)

blue_element = friends_list_sr.find_element(By.CSS_SELECTOR,
    "div.-r-common-modal__container ul > li:nth-of-type(5)")
driver.execute_script("arguments[0].scrollIntoView(true);", blue_element)
time.sleep(1)

blue2_select = Select(friends_list_sr.find_element(By.CSS_SELECTOR,
    "div.-r-common-modal__container ul > li:nth-of-type(5) > div > div:nth-of-type(2) select"))
blue2_select.select_by_visible_text("☆6")
time.sleep(1)


red_element = friends_list_sr.find_element(By.CSS_SELECTOR,
    "div.-r-common-modal__container ul > li:nth-of-type(6)")
driver.execute_script("arguments[0].scrollIntoView(true);", red_element)
time.sleep(1)

redb1_select = Select(friends_list_sr.find_element(By.CSS_SELECTOR,
    "div.-r-common-modal__container ul > li:nth-of-type(6) > div > div:nth-of-type(5) select"))
redb1_select.select_by_visible_text("☆9")
time.sleep(1)

search_element = friends_list_sr.find_element(By.CSS_SELECTOR,
    "div.-r-common-modal__container .-r-umamusume-friends-button")
driver.execute_script("arguments[0].scrollIntoView(true);", search_element)
time.sleep(1)

search_element.click()
time.sleep(1)

next_flag = True
while(next_flag):
    result_elements = friends_list_sr.find_elements(By.CSS_SELECTOR, "div > div.-r-umamusume-friends-list__list-wrap > ul > li > div.-r-umamusume-friends-list-item__contents > div > p")
    time.sleep(1)

    for result_element in result_elements:
        print(result_element.text)

    try:
        result_next = friends_list_sr.find_element(By.CSS_SELECTOR, "div > div.-r-umamusume-friends-list__list-wrap > button.-r-umamusume-friends-button")
        driver.execute_script("arguments[0].scrollIntoView(true);", result_next)
        driver.execute_script("window.scrollBy(0, -100);")
        time.sleep(5)
        result_next.click()
        time.sleep(5)
    except NoSuchElementException:
        next_flag = False



# div.-r-umamusume-friends-search-modallist-wrap ul > li:nth-of-type(5) > div > div:nth-of-type(2) select

time.sleep(5)
driver.quit()