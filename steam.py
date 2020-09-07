#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Nickwasused

import sys

if not sys.version_info > (3, 6):
    print('You need to use Python 3.6 or above')
    exit()

from steamconfig import config


def gettime():
    from datetime import datetime
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')


logtemp = []


def logwrite_true(_):
    logtemp.append('[{}] {}{}'.format(gettime(), _, '\n'))


def logwrite_to_file():
    with open(config.logfile, 'a+') as logfile:
        for _ in logtemp:
            logfile.write(_)
    logfile.close()


def logwrite_false():
    # Do not write log
    pass


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

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
databasefile = os.path.join(BASE_DIR, databaselocalfile)
logwrite('Database: {}'.format(databasefile))

if os.path.exists(config.logfile):
    os.remove(config.logfile)
else:
    # Nothing to remove
    pass

import sqlite3

database = sqlite3.connect(databasefile)

if config.proxy == "enabled":
    print('Using Proxy Server if available')
    logwrite('Using Proxy Server if available')
else:
    os.environ['NO_PROXY'] = config.botip
    print('Not using Proxy Servers')
    logwrite('Not using Proxy Servers')

appids = []


def cleanlist(appids):
    appids = list(dict.fromkeys(appids))
    logwrite('Cleaned appids')
    return appids


def getfreegames(s):
    url = s
    from urllib3 import PoolManager, exceptions
    from bs4 import BeautifulSoup
    import certifi
    try:
        https = PoolManager(ca_certs=certifi.where())
        response = https.request('GET', url, headers=config.headers).data.decode('utf-8')
        logwrite('Got url: {}'.format(url))
    except exceptions.ConnectionError:
        print('Cant connect to {}'.format(url))
        exit()

    soup = BeautifulSoup(response, 'html.parser')
    filterapps = soup.findAll('td')
    text = '{}'.format(filterapps)
    soup = BeautifulSoup(text, 'html.parser')
    from re import compile
    appidfinder = compile('^[0-9]{6}$')
    link = compile('^/')
    for _ in soup.findAll('a', attrs={'href': link}):
        appid = returnappid(_.get('href'))
        appid = appidfinder.match(appid)
        if appid:
            appids.append(appid.string)
        else:
            break


def returnappid(s):
    templink = s.replace('/', '')
    templink = templink.replace('sub', '')
    appid = templink.replace('app', '')
    logwrite('cleaned appid: {}'.format(appid))
    return appid


def redeemkey(bot, s):
    emessage = 'Cant connect to Archisteamfarm Api. {}'
    from urllib3 import PoolManager, exceptions
    from json import dumps
    http = PoolManager()
    data = {'Command': 'addlicense {} {}'.format(bot, s)}
    try:
        redeem = http.request('POST', config.boturl, body=dumps(data),
                              headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                              timeout=config.timeout)
        answer = answerdata.format(s)
        if redeem.status == 200:
            database.execute('INSERT INTO "{}" ("appids") VALUES ("{}")'.format(bot, s))
            logwrite('Redeemed appid: {} for bot: {}'.format(s, bot))
        elif redeem.status == 400:
            logwrite('Cant redeem appid: {} for bot: {}, because: "{}"'.format(s, bot, redeem.request))
        elif redeem.status == 401:
            print('Wrong IPC password/auth faliure')
            logwrite('Wrong IPC password/auth faliure')
        elif redeem.status == 403:
            print('Blocked by asf try again in a few hours')
            logwrite('Blocked by asf try again in a few hours')
        elif redeem.status == 500:
            print('unexpected error while redeeming appid: {}'.format(s))
            logwrite('unexpected error while redeeming appid: {}'.format(s))
        elif redeem.status == 503:
            print('third-party resource error while redeeming appid: {}'.format(s))
            logwrite('third-party resource error while redeeming appid: {}'.format(s))
        else:
            print('Cant Reddem code: {} on bot: {}'.format(bot, s))
            logwrite('Couldn´t Redeem appid: {} for bot: {}'.format(s, bot))
        return answer
    except exceptions.ConnectionError:
        print(emessage.format(config.boturl))
        logwrite(emessage.format(config.boturl))
        answer = answerdata.format(s)
        return answer
    except ConnectionRefusedError:
        print(emessage.format(config.boturl))
        logwrite(emessage.format(config.boturl))
        answer = answerdata.format(s)
        return answer


def redeemhead(bot):
    print('Redeeming Keys for Bot:{}'.format(bot))
    if not appids:
        print('There are no ids in the list!')
        return
    for _ in appids:
        cur = database.cursor()
        cur.execute('SELECT appids FROM "{}" WHERE appids="{}"'.format(bot, _))
        result = cur.fetchone()
        if result:
            print('Game is already redeemed: {}'.format(_))
            logwrite('Game already redeemed: {}'.format(_))
        else:
            print('redeeming' + ':  ' + _)
            redeemkey(bot, _)
        cur.close()


def createbotprofile(bot):
    logwrite('Checking Database for: {}'.format(bot))
    cur = database.cursor()
    cur.execute(
        'SELECT count(name) FROM sqlite_master WHERE type="table" AND name="{}"'.format(bot.replace('\'', '\'\'')))
    if cur.fetchone()[0] == 1:
        cur.close()
    else:
        try:
            database.execute('''CREATE TABLE "{}"
                 (appids TEXT UNIQUE)'''.format(bot))
            database.commit()
            logwrite('Created Database for Bot: {}'.format(bot))
        except sqlite3.OperationalError:
            logwrite('Cant Create Database for: {}'.format(bot))


def querygames():
    for _ in config.links:
        pool.submit(getfreegames(_))
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
logwrite_to_file()
