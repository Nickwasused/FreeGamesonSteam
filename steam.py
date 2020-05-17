#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Nickwasused
# version: 0.3

from bs4 import BeautifulSoup
import steamconfig as config
import requests
import urllib.request
import random
import time
import os
import urllib.parse
import json
import re

appids = []

def getfreegames_1():
    response = requests.get(config.basedb, headers=config.headers)
    soup = BeautifulSoup(response.text, "html.parser")
    filterapps = soup.findAll("td", {"class": "applogo"})
    text = '{}'.format(filterapps)
    soup2 = BeautifulSoup(text, "html.parser")
    for link in soup2.findAll('a', attrs={'href': re.compile("^/")}):
        appid = returnappid(link.get('href'))
        appids.append(appid)

def getfreegames_2():
    response = requests.get(config.basedbpacks, headers=config.headers)
    soup = BeautifulSoup(response.text, "html.parser")
    filterapps = soup.findAll("td")
    text = '{}'.format(filterapps)
    soup3 = BeautifulSoup(text, "html.parser")
    for link in soup3.findAll('a', attrs={'href': re.compile("^/")}):
        appid = returnappid(link.get('href'))
        appids.append(appid)
    
def returnappid(s):
    templink = s.replace("/", "")
    templink = templink.replace("sub", "")
    appid = templink.replace("app", "")
    return appid

def test_returnappid():
    appid = '{}'.format(random.randint(1,1000))
    assert returnappid(appid) == appid

def redeemkey(s):
    command = 'addlicense {} {}'.format(config.bot_name, s)
    data = {"Command": command}
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    try:
        redeem = requests.post(config.boturl, data=json.dumps(data), headers=headers)
        print(redeem)
        print(redeem.text)
    except requests.exceptions.ConnectionError:
        print('Cant connect to Archisteamfarm Api.')
        return 'success ' + s

def test_redeemkey():
    key = '{}'.format(random.randint(1,1000))
    assert redeemkey(key) == 'success {}'.format(key)

def querygames():
    soup2 = getfreegames_1()
    soup3 = getfreegames_2()
    
    for appid in appids:
        print('Redeming: ' + appid)
        redeemkey(appid)

querygames()
