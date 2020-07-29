#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Nickwasused

def gettime():
    from datetime import datetime
    now = datetime.now()
    time = now.strftime("%d/%m/%Y %H:%M:%S")
    return time


def logwrite_true(s):
    if config.log == 'true':
        logtime = gettime()
        log = s
        with open(config.logfile, 'a+') as logfile:
            logmessage = '[{}] {}{}'.format(logtime, log, '\n')
            logfile.write(logmessage)
        logfile.close()
    else:
        pass

def logwrite_false(s):
    pass

import steamconfig as config

if config.log == 'true':
    logwrite = logwrite_true
else:
    logwrite = logwrite_true

from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(3)
databaselocalfile = 'freegames.db'
answerdata = 'success {}'
success = 'success'

import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
databasefile = os.path.join(BASE_DIR, databaselocalfile)
logwrite('Database: {}'.format(databasefile))

import sqlite3

database = sqlite3.connect(databasefile)

try:
    import ctypes

    windll = ctypes.windll.kernel32
    windll.GetUserDefaultUILanguage()
    import locale

    lang = locale.windows_locale[windll.GetUserDefaultUILanguage()]
    print('Detected Language: ' + lang)
except AttributeError:
    print('Cant detect language using: en_US')
    lang = 'en_US'

if config.proxy == "enabled":
    print('Using Proxy Server if available')
    logwrite('Using Proxy Server if available')
    pass
else:
    os.environ['NO_PROXY'] = config.botip
    print('Not using Proxy Servers')
    logwrite('Not using Proxy Servers')

appids = []


def translate(text, lang):
    from googletrans import Translator
    import requests
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
    logwrite('Cleaned appids')
    return appids


def test_cleanlist():
    import random
    appids = []
    for _ in range(5):
        number = random.randint(1, 9) + random.randint(1, 9) + random.randint(1, 9)
        appids.append(number)
        appids.append(number)
    assert cleanlist(appids) != appids


def getfreegames(url):
    import requests
    from bs4 import BeautifulSoup
    try:
        response = requests.get(url, headers=config.headers)
        logwrite('Got url: {}'.format(url))
    except requests.exceptions.ConnectionError:
        print(translate('Cant connect to {}'.format(url), lang))
        exit()

    soup = BeautifulSoup(response.text, "html.parser")
    filterapps = soup.findAll("td")
    text = '{}'.format(filterapps)
    soup = BeautifulSoup(text, "html.parser")
    import re
    for link in soup.findAll('a', attrs={'href': re.compile("^/")}):
        appid = returnappid(link.get('href'))
        appids.append(appid)


def returnappid(s):
    templink = s.replace("/", "")
    templink = templink.replace("sub", "")
    appid = templink.replace("app", "")
    logwrite('cleaned appid: {}'.format(appid))
    return appid


def test_returnappid():
    import random
    realappid = '{}'.format(random.randint(1, 1000))
    appid = '/app/{}'.format(realappid)
    assert returnappid(appid) == realappid


def redeemkey(bot, s):
    import requests
    import json
    command = 'addlicense {} {}'.format(bot, s)
    data = {"Command": command}
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    try:
        redeem = requests.post(config.boturl, data=json.dumps(data), headers=headers)
        answer = answerdata.format(s)
        if redeem.status_code == 200:
            database.execute('INSERT INTO "{}" ("appids") VALUES ("{}")'.format(bot, s))
            logwrite('Redeemed appid: {} for bot: {}'.format(s, bot))
        else:
            print(translate('Cant Reddem code: {} on bot: {}'.format(bot, s), lang))
            logwrite('Couldn´t Redeem appid: {} for bot: {}'.format(s, bot))
        return answer
    except requests.exceptions.ConnectionError:
        print(translate('Cant connect to Archisteamfarm Api. {}'.format(config.boturl), lang))
        logwrite('Cant connect to Archisteamfarm Api. {}'.format(config.boturl))
        answer = answerdata.format(s)
        return answer
    except ConnectionRefusedError:
        print(translate('Cant connect to Archisteamfarm Api. {}'.format(config.boturl), lang))
        logwrite('Cant connect to Archisteamfarm Api. {}'.format(config.boturl))
        answer = answerdata.format(s)
        return answer


def test_redeemkey():
    import random
    bot = 'test'
    key = '{}'.format(random.randint(1, 1000))
    assert redeemkey(bot, key) == answerdata.format(key)


def redeemhead(bot):
    print('Redeeming Keys for Bot:{}'.format(bot))
    if not appids:
        print(translate('There are no ids in the list!', lang))
        return
    for appid in appids:
        cur = database.cursor()
        cur.execute('SELECT appids FROM "{}" WHERE appids="{}"'.format(bot, appid))
        result = cur.fetchone()
        if result:
            print('Game is already redeemed: {}'.format(appid))
            logwrite('Game already redeemed: {}'.format(appid))
        else:
            print(translate('redeeming', lang) + ':  ' + appid)
            redeemkey(bot, appid)
        cur.close()


def createbotprofile(bot):
    logwrite('Checking Database for: {}'.format(bot))
    cur = database.cursor()
    cur.execute(
        'SELECT count(name) FROM sqlite_master WHERE type="table" AND name="{}"'.format(bot.replace('\'', '\'\'')))
    if cur.fetchone()[0] == 1:
        cur.close()
        pass
    else:
        try:
            database.execute('''CREATE TABLE "{}"
                 (appids TEXT UNIQUE)'''.format(bot))
            database.commit()
            logwrite('Created Database for Bot: {}'.format(bot))
        except sqlite3.OperationalError:
            logwrite('Cant Create Database for: {}'.format(bot))
            pass


def querygames():
    pool.submit(getfreegames(config.basedb))
    pool.submit(getfreegames(config.basedbpacks))

    cleanlist(appids)

    for _ in config.bot_names:
        createbotprofile(_)
        redeemhead(_)
        database.commit()
        logwrite('commited database')


querygames()
database.commit()
logwrite('commited database')
database.close()
logwrite('database closed')
logwrite('----------------------')
