#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Nickwasused

import pprint
import sys
import json
from urllib3 import PoolManager, exceptions
from json import dumps
http = PoolManager()
pp = pprint.PrettyPrinter(indent=4)

if not sys.version_info > (3, 6):
    pp.pprint('You need to use Python 3.6 or above')
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
success = 'success'

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.exists(config.logfile):
    os.remove(config.logfile)
else:
    # Nothing to remove
    pass

if config.proxy == "enabled":
    pp.pprint('Using Proxy Server if available')
    logwrite('Using Proxy Server if available')
else:
    os.environ['NO_PROXY'] = config.botip
    pp.pprint('Not using Proxy Servers')
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
        pp.pprint('Cant connect to {}'.format(url))
        exit()

    soup = BeautifulSoup(response, 'html.parser')
    filterapps = soup.findAll('td')
    text = '{}'.format(filterapps)
    soup = BeautifulSoup(text, 'html.parser')
    from re import compile
    appidfinder = compile('^[0-9]{2,}$')
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
    errormessage = 'Cant redeem appid: {} for bot: {}, because: "{}"'
    data = {'Command': 'addlicense {} {}'.format(bot, s)}
    try:
        redeem = http.request('POST', config.boturl, body=dumps(data),
                              headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                              timeout=config.timeout)
        if redeem.status == 200:
            if "Fail" in redeem.data.decode('utf-8'):
                pp.pprint(errormessage.format(s, bot, redeem.data.decode('utf-8')))
                logwrite(errormessage.format(s, bot, redeem.data.decode('utf-8')))
            else:
                pp.pprint('Redeemed appid: {} for bot: {}'.format(s, bot))
                logwrite('Redeemed appid: {} for bot: {}'.format(s, bot))
        elif redeem.status == 400:
            pp.pprint(errormessage.format(s, bot, redeem.data.decode('utf-8')))
            logwrite(errormessage.format(s, bot, redeem.data.decode('utf-8')))
        elif redeem.status == 401:
            pp.pprint('Wrong IPC password/auth faliure')
            logwrite('Wrong IPC password/auth faliure')
        elif redeem.status == 403:
            pp.pprint('Blocked by asf try again in a few hours')
            logwrite('Blocked by asf try again in a few hours')
        elif redeem.status == 500:
            pp.pprint('unexpected error while redeeming appid: {}'.format(s))
            logwrite('unexpected error while redeeming appid: {}'.format(s))
        elif redeem.status == 503:
            pp.pprint('third-party resource error while redeeming appid: {}'.format(s))
            logwrite('third-party resource error while redeeming appid: {}'.format(s))
        else:
            pp.pprint('Cant Reddem code: {} on bot: {}'.format(bot, s))
            logwrite('Couldn´t Redeem appid: {} for bot: {}'.format(s, bot))
    except exceptions.ConnectionError:
        pp.pprint(emessage.format(config.boturl))
        logwrite(emessage.format(config.boturl))
    except exceptions.MaxRetryError:
        pp.pprint(emessage.format(config.boturl))
        logwrite(emessage.format(config.boturl))
    except exceptions.ConnectTimeoutError:
        pp.pprint(emessage.format(config.boturl))
        logwrite(emessage.format(config.boturl))
    except Exception as e:
        print(redeem.status)
        print(e)

def getaccountgames(steamid):
    accountappids = []
    link = config.getsteamapilink(steamid)
    games = http.request('GET', link)
    text = games.data.decode('utf-8')
    for _ in json.loads(text)["response"]["games"]:
        accountappids.append(_["appid"])

    return accountappids



def testownership(steamid, s):
    games = getaccountgames(steamid)
    for _ in games:
        if s in str(_):
            print("User has Game")
            return True
        else:
            print("User dosent´s has Game")
            return False


def redeemhead(bot):
    # Check for default Config
    if (bot["steamid"] == "YOUR_STEAM_ID_64"):
        pp.pprint('Please edit the Config file!')
        return

    pp.pprint('Redeeming Keys for Bot: {} With Steamid: {}'.format(bot["name"], bot["steamid"]))
    if not appids:
        pp.pprint('There are no ids in the list!')
        return
    for _ in appids:
        test = testownership(bot["steamid"], _)
        if test:
            pp.pprint('Game is already redeemed: {}'.format(_))
            logwrite('Game already redeemed: {}'.format(_))
        else:
            redeemkey(bot["name"], _)


def querygames():
    for _ in config.links:
        pool.submit(getfreegames(_))
    cleanlist(appids)

    for _ in config.bots:
        try:
            _ = json.loads(_)
        except json.decoder.JSONDecodeError:
            print("Your config seems to be broken!")
            continue

        redeemhead(_)
        
    logwrite_to_file()


querygames()

