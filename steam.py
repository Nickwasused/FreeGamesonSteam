#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Nickwasused

import sys

if not sys.version_info > (3, 6):
    print('You need to use Python 3.6 or above')
    exit()


def unloader(s):
    del sys.modules[s]


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
        # Do not write log
        pass


def logwrite_false():
    # Do not write log
    pass


import steamconfig as config

if config.log == 'true':
    logwrite = logwrite_true
else:
    logwrite = logwrite_false

from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count

pool = ThreadPoolExecutor(cpu_count())
databaselocalfile = 'freegames.db'
answerdata = 'success {}'
success = 'success'

import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
databasefile = os.path.join(BASE_DIR, databaselocalfile)
logwrite('Database: {}'.format(databasefile))
unloader('os')

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

unloader('ctypes')

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
    if config.translateoutput == "true":
        from googletrans import Translator
        from requests import exceptions
        try:
            translator = Translator()
            text = translator.translate(text, dest=lang)
            return text.text
        except exceptions.ConnectionError:
            return text
        except:
            return text
        umodules = ["Translator", "exceptions"]
        map(unloader, umodules)
    else:
        return text


def cleanlist(appids):
    appids = list(dict.fromkeys(appids))
    logwrite('Cleaned appids')
    return appids


def test_cleanlist():
    from random import randint
    appids = []
    for _ in range(5):
        number = randint(1, 9) + randint(1, 9) + randint(1, 9)
        appids.append(number)
        appids.append(number)
    assert cleanlist(appids) != appids


def getfreegames(url):
    from requests import get, exceptions
    from bs4 import BeautifulSoup
    try:
        response = get(url, headers=config.headers)
        response = response.text
        logwrite('Got url: {}'.format(url))
    except exceptions.ConnectionError:
        print(translate('Cant connect to {}'.format(url), lang))
        exit()

    soup = BeautifulSoup(response, "html.parser")
    filterapps = soup.findAll("td")
    text = '{}'.format(filterapps)
    soup = BeautifulSoup(text, "html.parser")
    from re import compile
    appidfinder = compile("^[0-9]{6}$")
    link = compile("^/")
    for _ in soup.findAll('a', attrs={'href': link}):
        appid = returnappid(_.get('href'))
        appid = appidfinder.match(appid)
        if appid:
            appids.append(appid.string)
        else:
            break
    umodules = ["get", "exceptions", "BeautifulSoup"]
    map(unloader, umodules)


def returnappid(s):
    templink = s.replace("/", "")
    templink = templink.replace("sub", "")
    appid = templink.replace("app", "")
    logwrite('cleaned appid: {}'.format(appid))
    return appid


def test_returnappid():
    from random import randint
    realappid = '{}'.format(randint(1, 1000))
    appid = '/app/{}'.format(realappid)
    assert returnappid(appid) == realappid


def redeemkey(bot, s):
    from requests import post, exceptions
    from json import dumps
    command = 'addlicense {} {}'.format(bot, s)
    data = {"Command": command}
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    try:
        redeem = post(config.boturl, data=dumps(data), headers=headers)
        answer = answerdata.format(s)
        if redeem.status_code == 200:
            database.execute('INSERT INTO "{}" ("appids") VALUES ("{}")'.format(bot, s))
            logwrite('Redeemed appid: {} for bot: {}'.format(s, bot))
        elif redeem.status_code == 400:
            logwrite('Cant redeem appid: {} for bot: {}, because: "{}"'.format(s, bot, redeem.request))
        elif redeem.status_code == 401:
            print('Wrong IPC password/auth faliure')
            logwrite('Wrong IPC password/auth faliure')
        elif redeem.status_code == 403:
            print('Blocked by asf try again in a few hours')
            logwrite('Blocked by asf try again in a few hours')
        elif redeem.status_code == 500:
            print('unexpected error while redeeming appid: {}'.format(s))
            logwrite('unexpected error while redeeming appid: {}'.format(s))
        elif redeem.status_code == 503:
            print('third-party resource error while redeeming appid: {}'.format(s))
            logwrite('third-party resource error while redeeming appid: {}'.format(s))
        else:
            print(translate('Cant Reddem code: {} on bot: {}'.format(bot, s), lang))
            logwrite('Couldn´t Redeem appid: {} for bot: {}'.format(s, bot))
        return answer
    except exceptions.ConnectionError:
        print(translate('Cant connect to Archisteamfarm Api. {}'.format(config.boturl), lang))
        logwrite('Cant connect to Archisteamfarm Api. {}'.format(config.boturl))
        answer = answerdata.format(s)
        return answer
    except ConnectionRefusedError:
        print(translate('Cant connect to Archisteamfarm Api. {}'.format(config.boturl), lang))
        logwrite('Cant connect to Archisteamfarm Api. {}'.format(config.boturl))
        answer = answerdata.format(s)
        return answer

    umodules = ['post', 'exceptions', 'dumps']
    map(unloader, umodules)


def test_redeemkey():
    from random import randint
    bot = 'test'
    key = '{}'.format(randint(1, 1000))
    assert redeemkey(bot, key) == answerdata.format(key)


def redeemhead(bot):
    print('Redeeming Keys for Bot:{}'.format(bot))
    if not appids:
        print(translate('There are no ids in the list!', lang))
        return
    for _ in appids:
        cur = database.cursor()
        cur.execute('SELECT appids FROM "{}" WHERE appids="{}"'.format(bot, _))
        result = cur.fetchone()
        if result:
            print('Game is already redeemed: {}'.format(_))
            logwrite('Game already redeemed: {}'.format(_))
        else:
            print(translate('redeeming', lang) + ':  ' + _)
            redeemkey(bot, _)
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
