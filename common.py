
CONFIG_PATH = "config/config.txt"
CONFIG_GW_KEY = "gw"
CONFIG_SEARCH_LIST_KEY = "search_list"

CONFIG_GW_MAX_NEXT_COUNT_KEY = "max_next_count"

SEARCH_TYPE_KEY = "type"
SEARCH_NAME_KEY = "name"

SEARCH_DAIHYO_KEY = "daihyo"

SEARCH_SPEED_KEY = "speed"
SEARCH_STAMINA_KEY = "stamina"
SEARCH_POWER_KEY = "power"
SEARCH_GUTS_KEY = "guts"
SEARCH_WISDOM_KEY = "wisdom"

SEARCH_TURF_KEY = "turf"
SEARCH_DIRT_KEY = "dirt"

SEARCH_SHORT_KEY = "short"
SEARCH_MILE_KEY = "mile"
SEARCH_MIDDLE_KEY = "middle"
SEARCH_LONG_KEY = "long"

SEARCH_NIGE_KEY = "nige"
SEARCH_SENKOU_KEY = "senkou"
SEARCH_SASHI_KEY = "sashi"
SEARCH_OIKOMI_KEY = "oikomi"

def scroll_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    return


def scroll(driver, x, y):
    driver.execute_script("window.scrollBy("+str(x)+", "+str(y)+");")
    return

