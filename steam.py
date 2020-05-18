#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Nickwasused
# version: 0.3.6.1

import json
import random
import re
import requests
import ctypes
import locale
import steamconfig as config
from bs4 import BeautifulSoup
from googletrans import Translator

try:
    windll = ctypes.windll.kernel32
    windll.GetUserDefaultUILanguage()
    lang = locale.windows_locale[windll.GetUserDefaultUILanguage()]
    print('Detected Language: ' + lang)
except:
    print('Cant detect language using: en_US')
    lang = 'en_US'

appids = []


def translate(text, lang):
    try:
        translator = Translator()
        text = translator.translate(text, dest=lang)
        return text.text
    except requests.exceptions.ConnectionError:
        return text


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


def redeemkey(s):
    command = 'addlicense {} {}'.format(config.bot_name, s)
    data = {"Command": command}
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    try:
        redeem = requests.post(config.boturl, data=json.dumps(data), headers=headers)
        print(redeem)
    except requests.exceptions.ConnectionError:
        print(translate('Cant connect to Archisteamfarm Api. {}'.format(config.boturl), lang))
        return 'success ' + s
    except ConnectionRefusedError:
        print(translate('Cant connect to Archisteamfarm Api. {}'.format(config.boturl), lang))
        return 'success ' + s


def test_redeemkey():
    key = '{}'.format(random.randint(1, 1000))
    assert redeemkey(key) == 'success {}'.format(key)


def querygames():
    getfreegames(config.basedb)
    getfreegames(config.basedbpacks)
    cleanlist(appids)

    for appid in appids:
        print(translate('redeeming', lang) + ':  ' + appid)
        redeemkey(appid)


querygames()
