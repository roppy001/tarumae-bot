import time
import json
import hashlib
import os
import datetime
import asyncio

import chromedriver_binary

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import discord

import common
import gamewith_scraper
import umadb_scraper

BOT_TOKEN=os.getenv('TARUMAE_BOT_TOKEN')
HEADLESS_STR=os.getenv('TARUMAE_BOT_HEADLESS')
CHANNEL_ID=os.getenv('TARUMAE_BOT_CHANNEL')
ROLE_ID=os.getenv('TARUMAE_BOT_ROLE_ID')

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

# 現在時刻のフォーマットを取得
def now_str():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 起動時に動作する処理
@client.event
async def on_ready():
    channel = await client.fetch_channel(CHANNEL_ID)

    while True:
        print("["+now_str()+ "] start searching")

        config = load_config()

        id_history_max_count = config[common.CONFIG_ID_HISTORY_COUNT_MAX_KEY]

        gw_config = config[common.CONFIG_GW_KEY]

        search_list = config[common.CONFIG_SEARCH_LIST_KEY]

        # Chromeを起動
        options = Options()
        if HEADLESS:
            options.add_argument('--headless')

        driver = webdriver.Chrome(options=options)

        for search in search_list:
            # 検索設定を保存するためのファイル名を決めるため、検索設定をMD5ハッシュ値に変換
            search_hash = get_json_md5(search)
            # ID履歴を取得
            id_history_list = load_id_history(search_hash)

            try:
                t = search[common.SEARCH_TYPE_KEY]

                result_list = []

                if t == common.TYPE_GW:
                    result_list = await gamewith_scraper.scrape(gw_config, search, driver, id_history_list)

                    for result in result_list:
                        await gamewith_scraper.send(gw_config, channel, ROLE_ID, result)
                elif t == common.TYPE_UMADB:
                    result_list = await umadb_scraper.scrape(gw_config, search, driver, id_history_list)

                    for result in result_list:
                        await gamewith_scraper.send(gw_config, channel, ROLE_ID, result)

                # 検索した結果のIDリストを履歴の先頭に追加し、保存最大数を超えるIDを削除
                id_history_list = (list(map(lambda x: x[common.RESULT_ID_KEY], result_list)) + id_history_list)[: id_history_max_count]

                save_id_history(search_hash, id_history_list)
            except NoSuchElementException:
                pass

        driver.quit()

        print("["+now_str()+ "] end searching")

        await asyncio.sleep(config[common.CONFIG_SEARCH_INTERVAL_KEY])

    return

client.run(BOT_TOKEN)
