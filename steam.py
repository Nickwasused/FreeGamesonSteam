#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Nickwasused
# version: 0.4.1

import json
import random
import re
import requests
import ctypes
import locale
import sqlite3
import steamconfig as config
from bs4 import BeautifulSoup
from googletrans import Translator
from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(3)
database = sqlite3.connect("freegames.db")
cur = database.cursor()
answerdata = 'success {}'

try:
    windll = ctypes.windll.kernel32
    windll.GetUserDefaultUILanguage()
    lang = locale.windows_locale[windll.GetUserDefaultUILanguage()]
    print('Detected Language: ' + lang)
except AttributeError:
    print('Cant detect language using: en_US')
    lang = 'en_US'

appids = []


def translate(text, lang):
    if config.translateoutput == "true":
        try:
            translator = Translator()
            text = translator.translate(text, dest=lang)
            return text.text
        except requests.exceptions.ConnectionError:
            return text
    else:
        return text


def cleanlist(appids):
    appids = list(dict.fromkeys(appids))
    return appids


def test_cleanlist():
    appids = []
    for _ in range(5):
        number = random.randint(1, 9) + random.randint(1, 9) + random.randint(1, 9)
        appids.append(number)
        appids.append(number)
    assert cleanlist(appids) != appids


def getfreegames(url):
    print(url)
    try:
        response = requests.get(url, headers=config.headers)
    except requests.exceptions.ConnectionError:
        print(translate('Cant connect to {}'.format(url), lang))
        exit()

    soup = BeautifulSoup(response.text, "html.parser")
    filterapps = soup.findAll("td")
    text = '{}'.format(filterapps)
    soup = BeautifulSoup(text, "html.parser")
    for link in soup.findAll('a', attrs={'href': re.compile("^/")}):
        appid = returnappid(link.get('href'))
        appids.append(appid)


def returnappid(s):
    templink = s.replace("/", "")
    templink = templink.replace("sub", "")
    appid = templink.replace("app", "")
    return appid


def test_returnappid():
    realappid = '{}'.format(random.randint(1, 1000))
    appid = '/app/{}'.format(realappid)
    assert returnappid(appid) == realappid


def redeemkey(bot, s):
    command = 'addlicense {} {}'.format(bot, s)
    data = {"Command": command}
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    try:
        redeem = requests.post(config.boturl, data=json.dumps(data), headers=headers)
        print(redeem)
        answer = answerdata.format(s)
        database.execute('INSERT INTO {} ("appids") VALUES ("{}")'.format(bot, s))
        return answer
    except requests.exceptions.ConnectionError:
        print(translate('Cant connect to Archisteamfarm Api. {}'.format(config.boturl), lang))
        answer = answerdata.format(s)
        return answer
    except ConnectionRefusedError:
        print(translate('Cant connect to Archisteamfarm Api. {}'.format(config.boturl), lang))
        answer = answerdata.format(s)
        return answer


def test_redeemkey():
    bot = 'test'
    key = '{}'.format(random.randint(1, 1000))
    assert redeemkey(bot, key) == answerdata.format(key)


def redeemhead(bot):
    print('Redeeming Keys for Bot:{}'.format(bot))
    for appid in appids:
        cur.execute("SELECT appids FROM {} WHERE appids={}".format(bot, appid))
        result = cur.fetchone()
        if result:
            print('Game is already redeemed: {}'.format(appid))
        else:
            print(translate('redeeming', lang) + ':  ' + appid)
            redeemkey(bot, appid)


def createbotprofile(bot):
    try:
        database.execute('''CREATE TABLE {}
                 (appids TEXT UNIQUE)'''.format(bot))
    except sqlite3.OperationalError:
        pass


def querygames():
    pool.submit(getfreegames(config.basedb))
    pool.submit(getfreegames(config.basedbpacks))

    cleanlist(appids)

    for _ in config.bot_names:
        createbotprofile(_)
        redeemhead(_)


querygames()
database.commit()
database.close()
