#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Nickwasused

from bs4 import BeautifulSoup
import requests
import urllib.request
import time
import os
import urllib.parse
import json
import re

def getfreegames_1():
    response = requests.get(basedb, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    filterapps = soup.findAll("td", {"class": "applogo"})
    text = '{}'.format(filterapps)
    soup2 = BeautifulSoup(text, "html.parser")
    return soup2
    
def returnsteamlink(s):
    templink = s.replace("/", "")
    appid = templink.replace("app", "")
    return appid

def redeemkey(s):
    data = {"KeysToRedeem": [s]}
    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    try:
        redeem = requests.post(url, data=json.dumps(data), headers=headers)
        print(redeem)
        print(redeem.text)
    except requests.exceptions.ConnectionError:
        print('Cant connect to Archisteamfarm Api.')

def querygames():
    soup2 = getfreegames_1()
    for link in soup2.findAll('a', attrs={'href': re.compile("^/")}):
        appid = returnsteamlink(link.get('href'))
        print('Found free Game! App-ID: ' + appid)
        print('Redeming')
        redeemkey(appid)

# Config
bot_name = "PUT_YOU_BOT_NAME_HERE"

basesteam = 'https://store.steampowered.com/app/'
basedb = "https://steamdb.info/sales/?min_discount=95&min_rating=0"
url = "http://127.0.0.1:1242/Api/Bot/{}/Redeem".format(bot_name)

headers = {
    'User-Agent': 'Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail appname/appversion'
}

querygames()
