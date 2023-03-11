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

    # ウマ娘DBを開く
    driver.get("https://uma.pure-db.com/#/search")

    await asyncio.sleep(100)

    return []

async def send(config, channel, role_id, elm):
    message = f'<@&{role_id}> \n'

    # await channel.send(message)

    return
