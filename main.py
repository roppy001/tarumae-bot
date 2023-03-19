import time
import json
import hashlib
import os
import datetime
import asyncio
import sys
from functools import reduce

import chromedriver_binary

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import discord
from discord.ext import tasks

import common
import gamewith_scraper
import umadb_scraper

# BOTのトークン
BOT_TOKEN=os.getenv('TARUMAE_BOT_TOKEN')

# YESの場合、ヘッドレスモードで動作
HEADLESS_STR=os.getenv('TARUMAE_BOT_HEADLESS')

# 投稿先チャンネルのID
CHANNEL_ID=os.getenv('TARUMAE_BOT_CHANNEL')

# メンションを送る先のロールID
ROLE_ID=os.getenv('TARUMAE_BOT_ROLE_ID')

# ループ間隔 デフォルトは30分
LOOP_INTERVAL=os.getenv('TARUMAE_LOOP_INTERVAL', 1800)

HEADLESS = HEADLESS_STR and HEADLESS_STR.lower() in ["on","yes"]

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
async def main_loop():
    channel = await client.fetch_channel(CHANNEL_ID)
    print("["+now_str()+ "] start searching")

    config = load_config()

    id_history_max_count = config[common.CONFIG_ID_HISTORY_COUNT_MAX_KEY]

    gw_config = config[common.CONFIG_GW_KEY]

    umadb_config = config[common.CONFIG_UMADB_KEY]

    search_list = config[common.CONFIG_SEARCH_LIST_KEY]

    # typeがallに指定されている場合は全検索サイトを検索するよう、設定値を変換する。
    tmp_list =[]
    for elm in search_list:
        if elm[common.SEARCH_TYPE_KEY] == common.TYPE_ALL:
            tmp = elm.copy()
            tmp[common.SEARCH_TYPE_KEY] = common.TYPE_GW
            tmp_list.append(tmp)
            tmp = elm.copy()
            tmp[common.SEARCH_TYPE_KEY] = common.TYPE_UMADB
            tmp_list.append(tmp)
        else:
            tmp_list.append(elm)
    
    search_list = tmp_list

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
                result_list = await umadb_scraper.scrape(umadb_config, search, driver, id_history_list)

                for result in result_list:
                    await umadb_scraper.send(umadb_config, channel, ROLE_ID, result)

            # 検索した結果のIDリストを履歴の先頭に追加し、保存最大数を超えるIDを削除
            id_history_list = (list(map(lambda x: x[common.RESULT_ID_KEY], result_list)) + id_history_list)[: id_history_max_count]

            save_id_history(search_hash, id_history_list)
        except NoSuchElementException:
            print("searching failed:" + json.dumps(search), file=sys.stderr)

    driver.quit()

    print("["+now_str()+ "] end searching")

    return

class MainClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        self.background_task.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    @tasks.loop(seconds=LOOP_INTERVAL)  # task runs every 60 seconds
    async def background_task(self):
        await main_loop()

    @background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

    async def on_message(self, message):
        if message.content == '.shutdown':
            await client.close()

its = discord.Intents.default()
its.message_content = True
client = MainClient(intents=its)
client.run(BOT_TOKEN)
