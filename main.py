import time
import json
import hashlib
import os

import chromedriver_binary

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import discord

import common
import gamewith_scraper

BOT_TOKEN=os.getenv('TARUMAE_BOT_TOKEN')
HEADLESS_STR=os.getenv('TARUMAE_BOT_HEADLESS')
HEADLESS = HEADLESS_STR and HEADLESS_STR.lower() in ["on","yes"]

its = discord.Intents.default()
client = discord.Client(intents=its)

# 設定ファイル読込
def load_config():
    fp = open(common.CONFIG_PATH, 'r', encoding="utf-8")

    data =json.load(fp)

    fp.close()

    return data

# 検索済みのIDを読込 読み込めない場合は空文字列を返却
def load_id_history(search_hash):
    try:
        fp = open(common.DATA_DIRECTORY + "/" + search_hash + ".txt", 'r', encoding="utf-8")

        id_list = list(map(lambda x: x.replace("\n",""), fp.readlines()))

        fp.close()

        return id_list
    except FileNotFoundError:
        return []


# 検索したのIDを保存
def save_id_history(search_hash, id_list):
    fp = open(common.DATA_DIRECTORY + "/" + search_hash + ".txt", 'w', encoding="utf-8")

    fp.writelines(list(map(lambda x: x+"\n", id_list)))

    fp.close()

    return

# jsonからMD5ハッシュ値に変換
def get_json_md5(str):
    return hashlib.md5(json.dumps(str).encode('utf-8')).hexdigest()

# 起動時に動作する処理
@client.event
async def on_ready():
    while True:
        config = load_config()

        id_history_max_count = config[common.CONFIG_ID_HISTORY_COUNT_MAX_KEY]

        gw_config = config[common.CONFIG_GW_KEY]

        search_list = config[common.CONFIG_SEARCH_LIST_KEY]

        # Chromeを起動
        options = Options()
        if HEADLESS:
            options.add_argument('--headless')

        driver = webdriver.Chrome(chrome_options=options)

        for search in search_list:
            # 検索設定を保存するためのファイル名を決めるため、検索設定をMD5ハッシュ値に変換
            search_hash = get_json_md5(search)
            # ID履歴を取得
            id_history_list = load_id_history(search_hash)

            try:
                result_list = gamewith_scraper.scrape(gw_config, search, driver, id_history_list)

                print(json.dumps(result_list, indent=2, ensure_ascii=False ))

                # 検索した結果のIDリストを履歴の先頭に追加し、保存最大数を超えるIDを削除
                id_history_list = (list(map(lambda x: x[common.RESULT_ID_KEY], result_list)) + id_history_list)[: id_history_max_count]

                save_id_history(search_hash, id_history_list)
            except NoSuchElementException:
                pass

        driver.quit()

        time.sleep(config[common.CONFIG_SEARCH_INTERVAL_KEY])

    return

client.run(BOT_TOKEN)
