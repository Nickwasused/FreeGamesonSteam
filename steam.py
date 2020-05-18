#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Nickwasused
# version: 0.3.5

import json
import random
import re
import requests
import steamconfig as config
from bs4 import BeautifulSoup


appids = []


def cleanlist(appids):
    appids = list(dict.fromkeys(appids))
    return appids


def test_cleanlist():
    appids = []
    for x in range(5):
        number = random.randint(1, 9) + random.randint(1, 9) + random.randint(1, 9)
        appids.append(number)
        appids.append(number)
    assert cleanlist(appids) != appids


def getfreegames_1():
    response = requests.get(config.basedb, headers=config.headers)
    soup = BeautifulSoup(response.text, "html.parser")
    filterapps = soup.findAll("td", {"class": "applogo"})
    text = '{}'.format(filterapps)
    soup = BeautifulSoup(text, "html.parser")
    for link in soup.findAll('a', attrs={'href': re.compile("^/")}):
        appid = returnappid(link.get('href'))
        appids.append(appid)
    cleanlist(appids)


def getfreegames_2():
    response = requests.get(config.basedbpacks, headers=config.headers)
    soup = BeautifulSoup(response.text, "html.parser")
    filterapps = soup.findAll("td")
    text = '{}'.format(filterapps)
    soup = BeautifulSoup(text, "html.parser")
    for link in soup.findAll('a', attrs={'href': re.compile("^/")}):
        appid = returnappid(link.get('href'))
        appids.append(appid)
    cleanlist(appids)


def returnappid(s):
    templink = s.replace("/", "")
    templink = templink.replace("sub", "")
    appid = templink.replace("app", "")
    return appid


def test_returnappid():
    realappid = '{}'.format(random.randint(1, 1000))
    appid = '/app/{}'.format(realappid)
    assert returnappid(appid) == realappid


def redeemkey(s):
    command = 'addlicense {} {}'.format(config.bot_name, s)
    data = {"Command": command}
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    try:
        redeem = requests.post(config.boturl, data=json.dumps(data), headers=headers)
        print(redeem)
    except requests.exceptions.ConnectionError:
        print('Cant connect to Archisteamfarm Api.')
        return 'success ' + s
    except ConnectionRefusedError:
        print('Cant connect to Archisteamfarm Api.')
        return 'success ' + s


def test_redeemkey():
    key = '{}'.format(random.randint(1, 1000))
    assert redeemkey(key) == 'success {}'.format(key)


def querygames():
    getfreegames_1()
    getfreegames_2()

    for appid in appids:
        print('Redeming: ' + appid)
        redeemkey(appid)


querygames()
