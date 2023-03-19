SHUTDOWN_PATH = "data/SHUTDOWN"

CONFIG_PATH = "config/config.txt"
CONFIG_SEARCH_INTERVAL_KEY = "search_interval"
CONFIG_ID_HISTORY_COUNT_MAX_KEY = "id_history_max_count"
CONFIG_GW_KEY = "gw"
CONFIG_UMADB_KEY = "umadb"
CONFIG_SEARCH_LIST_KEY = "search_list"

CONFIG_GW_MAX_NEXT_COUNT_KEY = "max_next_count"
CONFIG_UMADB_SEARCH_WAIT_KEY = "search_wait"

DATA_DIRECTORY = "data"

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

RESULT_TYPE_KEY = "type"
RESULT_ID_KEY = "id"
RESULT_MAIN_IMG_KEY = "main_img"
IMG_URL_KEY = "url"
RESULT_FACTOR_LIST_KEY = "factor_list"
FACTOR_NAME_KEY = "name"

TYPE_ALL = "all"
TYPE_GW = "gw"
TYPE_UMADB = "umadb"

def scroll_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    return


def scroll(driver, x, y):
    driver.execute_script("window.scrollBy("+str(x)+", "+str(y)+");")
    return

